import logging

from sqlalchemy.orm import Session

from app.models.document import Document
from app.models.document_chunk import DocumentChunk

from app.services.chunking_service import chunk_document
from app.services.document_chunk_service import (
    create_document_chunks,
)
from app.services.document_parser import parse_document
from app.services.embedding_service import (
    generate_embeddings,
)
from app.services.vector_service import (
    create_collection,
    upsert_chunks,
)

logger = logging.getLogger(__name__)

# =============================================================================
# Constants
# =============================================================================

STATUS_UPLOADED = "UPLOADED"
STATUS_PROCESSING = "PROCESSING"
STATUS_INDEXED = "INDEXED"
STATUS_FAILED = "FAILED"

# =============================================================================
# Document Ingestion
# =============================================================================


def process_document(
    db: Session,
    document_id: int,
) -> Document:
    """
    Processes a document through the complete ingestion pipeline.

    Pipeline:

        Upload
            ↓
        Parse
            ↓
        Chunk
            ↓
        Store Chunks
            ↓
        Generate Embeddings
            ↓
        Store Vectors
            ↓
        Indexed
    """

    document = (
        db.query(Document)
        .filter(
            Document.id == document_id,
        )
        .first()
    )

    if document is None:
        raise ValueError(
            f"Document {document_id} not found."
        )

    if document.status == STATUS_INDEXED:

        logger.info(
            "Document %d already indexed.",
            document_id,
        )

        return document

    logger.info(
        "Starting ingestion for document %d.",
        document_id,
    )

    try:

        _update_status(
            db,
            document,
            STATUS_PROCESSING,
        )

        _delete_existing_chunks(
            db,
            document.id,
        )

        parsed_document = parse_document(
            document.storage_path,
            document.file_type,
        )

        chunks = chunk_document(
            parsed_document,
        )

        chunk_records = create_document_chunks(
            db=db,
            document_id=document.id,
            chunks=chunks,
        )

        embeddings = generate_embeddings(
            chunks,
        )

        create_collection()

        upsert_chunks(
            chunk_records,
            embeddings,
        )

        _update_status(
            db,
            document,
            STATUS_INDEXED,
        )

        logger.info(
            "Successfully indexed document %d.",
            document_id,
        )

        return document

    except Exception:

        logger.exception(
            "Document ingestion failed: %d",
            document_id,
        )

        db.rollback()

        _update_status(
            db,
            document,
            STATUS_FAILED,
        )

        raise


# =============================================================================
# Helpers
# =============================================================================


def _update_status(
    db: Session,
    document: Document,
    status: str,
) -> None:
    """
    Updates the processing status of a document.
    """

    document.status = status

    db.commit()
    db.refresh(document)


def _delete_existing_chunks(
    db: Session,
    document_id: int,
) -> None:
    """
    Removes previously indexed chunks before re-indexing.
    """

    (
        db.query(DocumentChunk)
        .filter(
            DocumentChunk.document_id == document_id,
        )
        .delete()
    )

    db.commit()
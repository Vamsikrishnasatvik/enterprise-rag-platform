from sqlalchemy.orm import Session
import traceback

from app.models.document import Document
from app.models.document_chunk import DocumentChunk

from app.services.document_parser import parse_document
from app.services.chunking_service import chunk_document
from app.services.document_chunk_service import (
    create_document_chunks,
)
from app.services.embedding_service import (
    generate_embeddings,
)
from app.services.vector_service import (
    create_collection,
    upsert_chunks,
)
from app.services.metadata_extraction_service import (
    extract_metadata,
)


def process_document(
    db: Session,
    document_id: int,
):
    """
    Process a document through the ingestion pipeline.

    Pipeline:
    - Parse document
    - Extract metadata
    - Chunk document
    - Store chunks
    - Generate embeddings
    - Index into Qdrant
    """

    document = (
        db.query(Document)
        .filter(Document.id == document_id)
        .first()
    )

    if not document:
        raise ValueError(
            "Document not found"
        )

    if document.status == "INDEXED":
        return document

    try:

        document.status = "PROCESSING"
        db.commit()
        db.refresh(document)

        (
            db.query(DocumentChunk)
            .filter(
                DocumentChunk.document_id
                == document.id
            )
            .delete()
        )

        db.commit()

        # -----------------------------
        # Parse document
        # -----------------------------

        parsed = parse_document(
            document.storage_path,
            document.file_type,
        )

        # -----------------------------
        # Extract document metadata
        # -----------------------------

        metadata = extract_metadata(
            parsed.text
        )

        # -----------------------------
        # Chunk document
        # -----------------------------

        chunks = chunk_document(
            parsed
        )

        # -----------------------------
        # Persist chunks
        # -----------------------------

        chunk_records = (
            create_document_chunks(
                db=db,
                document_id=document.id,
                chunks=chunks,
                metadata=metadata,
            )
        )

        # -----------------------------
        # Generate embeddings
        # -----------------------------

        embeddings = generate_embeddings(
            chunks
        )

        # -----------------------------
        # Index into Qdrant
        # -----------------------------

        create_collection()

        upsert_chunks(
            chunk_records,
            embeddings,
        )

        document.status = "INDEXED"

        db.commit()
        db.refresh(document)

        return document

    except Exception:

        traceback.print_exc()

        db.rollback()

        document.status = "FAILED"

        db.commit()
        db.refresh(document)

        raise
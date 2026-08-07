import logging

from sqlalchemy.orm import Session

from app.models.document import Document
from app.models.document_chunk import DocumentChunk

logger = logging.getLogger(__name__)

# =============================================================================
# Document Chunk CRUD
# =============================================================================


def create_document_chunks(
    db: Session,
    document_id: int,
    chunks: list[str],
) -> list[DocumentChunk]:
    """
    Creates document chunk records for a document.

    Each chunk is assigned a sequential chunk index while
    inheriting the tenant ID from the parent document.
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

    if not chunks:

        logger.info(
            "No chunks generated for document %d.",
            document_id,
        )

        return []

    records = [
        DocumentChunk(
            tenant_id=document.tenant_id,
            document_id=document_id,
            chunk_index=index,
            content=chunk,
            chunk_metadata={},
        )
        for index, chunk in enumerate(chunks)
    ]

    db.add_all(records)
    db.commit()

    for record in records:
        db.refresh(record)

    logger.info(
        "Created %d chunk(s) for document %d.",
        len(records),
        document_id,
    )

    return records
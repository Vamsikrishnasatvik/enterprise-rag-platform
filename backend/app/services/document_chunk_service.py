from sqlalchemy.orm import Session

from app.models.document_chunk import DocumentChunk
from app.models.document import Document


def create_document_chunks(
    db: Session,
    document_id: int,
    chunks: list[str],
):
    document = (
        db.query(Document)
        .filter(Document.id == document_id)
        .first()
    )

    if not document:
        raise ValueError(
            "Document not found"
        )

    records = []

    for index, chunk in enumerate(chunks):
        record = DocumentChunk(
            tenant_id=document.tenant_id,
            document_id=document_id,
            chunk_index=index,
            content=chunk,
            chunk_metadata={},
        )

        records.append(record)

    db.add_all(records)
    db.commit()

    for record in records:
        db.refresh(record)

    return records
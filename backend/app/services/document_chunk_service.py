from sqlalchemy.orm import Session

from app.models.document_chunk import DocumentChunk


def create_document_chunks(
    db: Session,
    document_id: int,
    chunks: list[str],
):
    records = []

    for index, chunk in enumerate(chunks):
        record = DocumentChunk(
            document_id=document_id,
            chunk_index=index,
            content=chunk,
            chunk_metadata={},
        )

        records.append(record)

    db.add_all(records)
    db.commit()

    return records
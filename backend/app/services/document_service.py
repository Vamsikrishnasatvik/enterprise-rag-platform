from sqlalchemy.orm import Session

from app.models.document import Document


def create_document(
    db: Session,
    tenant_id: int,
    filename: str,
    storage_path: str,
    file_type: str,
    file_size: int,
):
    document = Document(
        tenant_id=tenant_id,
        filename=filename,
        storage_path=storage_path,
        file_type=file_type,
        file_size=file_size,
        status="UPLOADED",
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return document


def get_document_name(
    db: Session,
    document_id: int,
) -> str | None:
    """
    Return the filename for a document.
    """

    document = (
        db.query(Document)
        .filter(Document.id == document_id)
        .first()
    )

    if not document:
        return None

    return document.filename
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
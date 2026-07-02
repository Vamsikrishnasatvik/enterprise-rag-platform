from sqlalchemy.orm import Session

from app.models.document import Document


def create_document(
    db: Session,
    tenant_id: int,
    filename: str,
    storage_path: str,
    file_type: str,
    file_size: int,
    department: str | None = None,
    category: str | None = None,
    source: str | None = None,
    tags: list[str] | None = None,
):
    document = Document(
        tenant_id=tenant_id,
        filename=filename,
        storage_path=storage_path,
        file_type=file_type,
        file_size=file_size,
        status="UPLOADED",
        department=department,
        category=category,
        source=source,
        tags=tags,
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return document
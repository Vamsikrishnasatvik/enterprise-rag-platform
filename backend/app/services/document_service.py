from sqlalchemy.orm import Session

from app.models.document import Document


def create_document(
    db: Session,
    filename: str,
    storage_path: str,
    file_type: str,
    file_size: int,
):
    document = Document(
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
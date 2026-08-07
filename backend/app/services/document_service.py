import logging

from sqlalchemy.orm import Session

from app.models.document import Document

logger = logging.getLogger(__name__)

# =============================================================================
# Document CRUD
# =============================================================================


def create_document(
    db: Session,
    tenant_id: int,
    filename: str,
    storage_path: str,
    file_type: str,
    file_size: int,
) -> Document:
    """
    Creates a new document record.

    Newly uploaded documents are initialized with the
    'UPLOADED' processing status.
    """

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

    logger.info(
        "Created document | id=%d | tenant=%d | filename=%s",
        document.id,
        tenant_id,
        filename,
    )

    return document
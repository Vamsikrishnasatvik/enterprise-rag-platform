import logging

from sqlalchemy.orm import Session

from app.models.ingestion_job import (
    IngestionJob,
    IngestionJobStatus,
)

logger = logging.getLogger(__name__)

# =============================================================================
# Ingestion Job CRUD
# =============================================================================


def create_ingestion_job(
    db: Session,
    tenant_id: int,
    document_id: int,
) -> IngestionJob:
    """
    Creates a new ingestion job for a document.
    """

    job = IngestionJob(
        tenant_id=tenant_id,
        document_id=document_id,
        status=IngestionJobStatus.PENDING.value,
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    logger.info(
        "Created ingestion job | id=%d | document=%d",
        job.id,
        document_id,
    )

    return job


def get_ingestion_job(
    db: Session,
    job_id: int,
) -> IngestionJob | None:
    """
    Retrieves an ingestion job by its ID.
    """

    return (
        db.query(IngestionJob)
        .filter(
            IngestionJob.id == job_id,
        )
        .first()
    )


def update_ingestion_job_status(
    db: Session,
    job: IngestionJob,
    status: str,
    error_message: str | None = None,
) -> IngestionJob:
    """
    Updates the status of an ingestion job.

    Optionally stores an error message when processing fails.
    """

    job.status = status

    if error_message:
        job.error_message = error_message

    db.commit()
    db.refresh(job)

    logger.info(
        "Updated ingestion job | id=%d | status=%s",
        job.id,
        status,
    )

    return job
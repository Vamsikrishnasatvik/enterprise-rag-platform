from sqlalchemy.orm import Session

from app.models.ingestion_job import (
    IngestionJob,
    IngestionJobStatus,
)


def create_ingestion_job(
    db: Session,
    tenant_id: int,
    document_id: int,
) -> IngestionJob:
    job = IngestionJob(
        tenant_id=tenant_id,
        document_id=document_id,
        status=IngestionJobStatus.PENDING.value,
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    return job


def get_ingestion_job(
    db: Session,
    job_id: int,
) -> IngestionJob | None:
    return (
        db.query(IngestionJob)
        .filter(
            IngestionJob.id == job_id
        )
        .first()
    )


def update_ingestion_job_status(
    db: Session,
    job: IngestionJob,
    status: str,
    error_message: str | None = None,
):
    job.status = status

    if error_message:
        job.error_message = error_message

    db.commit()
    db.refresh(job)

    return job
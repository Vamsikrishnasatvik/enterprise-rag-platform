from datetime import datetime

from app.db.session import SessionLocal

from app.models.ingestion_job import (
    IngestionJob,
    IngestionJobStatus,
)

from app.services.ingestion_service import (
    process_document,
)


def process_ingestion_job(
    job_id: int,
):
    db = SessionLocal()

    try:
        job = (
            db.query(IngestionJob)
            .filter(
                IngestionJob.id == job_id
            )
            .first()
        )

        if not job:
            return

        job.status = (
            IngestionJobStatus.PROCESSING.value
        )
        job.started_at = (
            datetime.utcnow()
        )

        db.commit()

        process_document(
            db,
            job.document_id,
        )

        job.status = (
            IngestionJobStatus.COMPLETED.value
        )
        job.completed_at = (
            datetime.utcnow()
        )

        db.commit()

    except Exception as e:
        db.rollback()

        job = (
            db.query(IngestionJob)
            .filter(
                IngestionJob.id == job_id
            )
            .first()
        )

        if job:
            job.status = (
                IngestionJobStatus.FAILED.value
            )
            job.error_message = str(e)

            db.commit()

        raise

    finally:
        db.close()
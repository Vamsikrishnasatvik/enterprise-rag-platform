from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from sqlalchemy.orm import Session

from app.core.dependencies import (
    get_db,
    get_current_user,
)

from app.models.user import User

from app.services.ingestion_job_service import (
    get_ingestion_job,
)

router = APIRouter()


@router.get("/{job_id}")
def get_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    job = get_ingestion_job(
        db=db,
        job_id=job_id,
    )

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ingestion job not found",
        )

    if (
        job.tenant_id
        != current_user.tenant_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )

    return {
        "id": job.id,
        "tenant_id": job.tenant_id,
        "document_id": job.document_id,
        "status": job.status,
        "error_message": job.error_message,
        "created_at": job.created_at,
        "started_at": job.started_at,
        "completed_at": job.completed_at,
    }
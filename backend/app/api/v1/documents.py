from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends,
)
from sqlalchemy.orm import Session

from app.core.storage import (
    save_uploaded_file,
)
from app.core.dependencies import (
    get_db,
    get_current_user,
)
from app.models.user import User

from app.services.document_service import (
    create_document,
)
from app.services.ingestion_job_service import (
    create_ingestion_job,
)
from app.services.queue_service import (
    enqueue_ingestion_job,
)

router = APIRouter()


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    storage_path = save_uploaded_file(
        file
    )

    file_size = file.size or 0

    document = create_document(
        db=db,
        tenant_id=current_user.tenant_id,
        filename=file.filename,
        storage_path=storage_path,
        file_type=file.content_type
        or "application/octet-stream",
        file_size=file_size,
    )

    job = create_ingestion_job(
        db=db,
        tenant_id=current_user.tenant_id,
        document_id=document.id,
    )

    enqueue_ingestion_job(
        job.id
    )

    return {
        "document_id": document.id,
        "job_id": job.id,
        "status": job.status,
    }
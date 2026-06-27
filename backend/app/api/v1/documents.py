from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File
from fastapi import Depends
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.core.storage import save_uploaded_file
from app.services.document_service import create_document
from app.schemas.document import DocumentResponse

router = APIRouter()


@router.post(
    "/upload",
    response_model=DocumentResponse,
)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    storage_path = save_uploaded_file(file)

    file_size = file.size or 0

    document = create_document(
        db=db,
        filename=file.filename,
        storage_path=storage_path,
        file_type=file.content_type or "application/octet-stream",
        file_size=file_size,
    )

    return document
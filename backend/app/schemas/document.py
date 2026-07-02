from datetime import datetime

from pydantic import BaseModel


class DocumentResponse(BaseModel):
    id: int
    filename: str
    file_type: str
    file_size: int
    storage_path: str
    status: str

    department: str | None = None
    category: str | None = None
    source: str | None = None
    tags: list[str] | None = None

    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }
from datetime import datetime

from pydantic import BaseModel


class UserResponse(
    BaseModel
):
    id: int
    tenant_id: int
    email: str
    full_name: str
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
from datetime import datetime
from pydantic import BaseModel


class ConversationCreate(BaseModel):
    title: str | None = None


class ConversationResponse(BaseModel):
    id: int
    tenant_id: int
    title: str | None
    summary: str | None
    message_count: int
    last_message_at: datetime | None
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


class MessageResponse(BaseModel):
    id: int
    role: str
    content: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


class ConversationQueryRequest(BaseModel):
    query: str
from typing import Optional

from pydantic import BaseModel


class ChatRequest(BaseModel):
    query: str
    conversation_id: int | None = None


class SourceChunk(BaseModel):
    chunk_id: int
    document_id: int
    document_name: str | None = None
    page_number: int | None = None
    section: str | None = None
    content: str
    score: float


class ChatResponse(BaseModel):
    conversation_id: int
    answer: str
    sources: list[SourceChunk]
    execution_trace: list
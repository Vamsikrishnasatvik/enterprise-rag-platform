from typing import Optional

from pydantic import BaseModel


class ChatRequest(BaseModel):
    query: str


class SourceChunk(BaseModel):
    chunk_id: int
    document_id: int

    # Rich Citation Metadata
    document_name: Optional[str] = None
    page_number: Optional[int] = None
    section: Optional[str] = None

    content: str
    score: float


class ChatResponse(BaseModel):
    answer: str
    sources: list[SourceChunk]
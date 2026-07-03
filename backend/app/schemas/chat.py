from pydantic import BaseModel


class ChatRequest(BaseModel):
    query: str

    department: str | None = None
    category: str | None = None
    source: str | None = None
    tags: list[str] | None = None


class SourceChunk(BaseModel):
    chunk_id: int
    document_id: int
    content: str
    score: float


class ChatResponse(BaseModel):
    answer: str
    sources: list[SourceChunk]
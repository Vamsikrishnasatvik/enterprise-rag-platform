from pydantic import BaseModel


class ChatRequest(BaseModel):
    query: str


class SourceChunk(BaseModel):
    chunk_id: int
    document_id: int
    content: str
    score: float


class ChatResponse(BaseModel):
    answer: str
    sources: list[SourceChunk]
from fastapi import APIRouter

from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
)
from app.services.rag_service import (
    answer_question,
)

router = APIRouter()


@router.post(
    "/query",
    response_model=ChatResponse,
)
def query_documents(
    request: ChatRequest,
):
    return answer_question(
        request.query
    )
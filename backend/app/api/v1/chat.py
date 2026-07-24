from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db

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
    db: Session = Depends(get_db),
):
    return answer_question(
        db=db,
        conversation_id=request.conversation_id,
        question=request.query,
    )
from fastapi import (
    APIRouter,
    Depends,
)

from sqlalchemy.orm import Session

from app.core.dependencies import (
    get_db,
    get_current_user,
)

from app.models.user import User

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
    current_user: User = Depends(
        get_current_user,
    ),
):
    return answer_question(
        db=db,
        tenant_id=current_user.tenant_id,
        question=request.query,
        department=request.department,
        category=request.category,
        source=request.source,
        tags=request.tags,
    )
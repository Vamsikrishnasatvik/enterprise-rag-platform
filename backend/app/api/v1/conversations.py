from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.dependencies.db import get_db

from app.schemas.conversation import (
    ConversationCreate,
    ConversationResponse,
    MessageResponse,
    ConversationQueryRequest,
)

from app.services.conversation_service import (
    create_conversation,
    get_conversation,
)

from app.services.message_service import (
    get_messages,
    create_message,
)

from app.services.rag_service import (
    answer_conversation_question,
)

router = APIRouter()


@router.post(
    "",
    response_model=ConversationResponse,
)
def create_new_conversation(
    request: ConversationCreate,
    db: Session = Depends(get_db),
):
    return create_conversation(
        db,
        request.title,
    )


@router.get(
    "/{conversation_id}",
    response_model=ConversationResponse,
)
def get_conversation_by_id(
    conversation_id: int,
    db: Session = Depends(get_db),
):
    conversation = get_conversation(
        db,
        conversation_id,
    )

    if not conversation:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found",
        )

    return conversation


@router.get(
    "/{conversation_id}/messages",
    response_model=list[MessageResponse],
)
def get_conversation_messages(
    conversation_id: int,
    db: Session = Depends(get_db),
):
    conversation = get_conversation(
        db,
        conversation_id,
    )

    if not conversation:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found",
        )

    return get_messages(
        db,
        conversation_id,
    )


@router.post(
    "/{conversation_id}/query",
)
def query_conversation(
    conversation_id: int,
    request: ConversationQueryRequest,
    db: Session = Depends(get_db),
):
    conversation = get_conversation(
        db,
        conversation_id,
    )

    if not conversation:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found",
        )

    create_message(
        db=db,
        conversation_id=conversation_id,
        role="user",
        content=request.query,
    )

    result = answer_conversation_question(
        db=db,
        conversation_id=conversation_id,
        question=request.query,
    )

    create_message(
        db=db,
        conversation_id=conversation_id,
        role="assistant",
        content=result["answer"],
    )

    return result
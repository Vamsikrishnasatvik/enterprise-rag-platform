from sqlalchemy.orm import Session

from app.models.message import Message
from app.models.conversation import (
    Conversation,
)

from app.services.conversation_service import (
    increment_message_count,
)


def create_message(
    db: Session,
    tenant_id: int,
    conversation_id: int,
    role: str,
    content: str,
):
    message = Message(
        tenant_id=tenant_id,
        conversation_id=conversation_id,
        role=role,
        content=content,
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    increment_message_count(
        db,
        conversation_id,
    )

    return message


def get_messages(
    db: Session,
    conversation_id: int,
):
    return (
        db.query(Message)
        .filter(
            Message.conversation_id
            == conversation_id
        )
        .order_by(Message.created_at)
        .all()
    )


def build_chat_history(
    db: Session,
    conversation_id: int,
    max_messages: int = 10,
):
    messages = (
        db.query(Message)
        .filter(
            Message.conversation_id
            == conversation_id
        )
        .order_by(
            Message.created_at.desc()
        )
        .limit(max_messages)
        .all()
    )

    messages.reverse()

    history = []

    for message in messages:
        history.append(
            {
                "role": message.role,
                "content": message.content,
            }
        )

    return history
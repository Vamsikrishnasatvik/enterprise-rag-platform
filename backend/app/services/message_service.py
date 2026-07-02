from sqlalchemy.orm import Session

from app.models.message import Message

from app.services.conversation_service import (
    increment_message_count,
)

from app.services.summarization_service import (
    should_generate_summary,
    create_summary,
)


def estimate_tokens(
    text: str,
):
    return max(
        1,
        len(text) // 4,
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

    conversation = increment_message_count(
        db,
        conversation_id,
    )

    if (
        conversation
        and should_generate_summary(
            conversation
        )
    ):
        create_summary(
            db,
            conversation,
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
        .order_by(
            Message.created_at
        )
        .all()
    )


def build_chat_history(
    db: Session,
    conversation_id: int,
    max_tokens: int = 1500,
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
        .all()
    )

    history = []

    total_tokens = 0

    for message in messages:
        message_tokens = (
            estimate_tokens(
                message.content
            )
        )

        if (
            total_tokens
            + message_tokens
            > max_tokens
        ):
            break

        history.append(
            {
                "role": message.role,
                "content": message.content,
            }
        )

        total_tokens += (
            message_tokens
        )

    history.reverse()

    return history
import logging

from sqlalchemy.orm import Session

from app.models.message import Message

logger = logging.getLogger(__name__)

# =============================================================================
# Message CRUD
# =============================================================================


def create_message(
    db: Session,
    conversation_id: int,
    tenant_id: int,
    role: str,
    content: str,
) -> Message:
    """
    Creates a new message in a conversation.
    """

    message = Message(
        conversation_id=conversation_id,
        tenant_id=tenant_id,
        role=role,
        content=content,
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    logger.info(
        "Created message | conversation=%d | role=%s",
        conversation_id,
        role,
    )

    return message


def get_messages(
    db: Session,
    conversation_id: int,
) -> list[Message]:
    """
    Returns all messages for a conversation in chronological order.
    """

    return (
        db.query(Message)
        .filter(
            Message.conversation_id == conversation_id,
        )
        .order_by(
            Message.created_at,
        )
        .all()
    )


# =============================================================================
# Chat History
# =============================================================================


def get_chat_history(
    db: Session,
    conversation_id: int,
) -> list[dict]:
    """
    Returns the complete chat history formatted for LLM consumption.
    """

    messages = get_messages(
        db=db,
        conversation_id=conversation_id,
    )

    return _format_messages(messages)


def get_recent_messages(
    db: Session,
    conversation_id: int,
    limit: int = 10,
) -> list[dict]:
    """
    Returns the most recent messages in chronological order.
    """

    messages = (
        db.query(Message)
        .filter(
            Message.conversation_id == conversation_id,
        )
        .order_by(
            Message.created_at.desc(),
        )
        .limit(limit)
        .all()
    )

    messages.reverse()

    return _format_messages(messages)


# =============================================================================
# Helpers
# =============================================================================


def _format_messages(
    messages: list[Message],
) -> list[dict]:
    """
    Converts Message ORM objects into chat history format.
    """

    return [
        {
            "role": message.role,
            "content": message.content,
        }
        for message in messages
    ]
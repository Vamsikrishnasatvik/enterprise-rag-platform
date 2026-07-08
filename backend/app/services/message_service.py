from sqlalchemy.orm import Session

from app.models.message import Message

from app.services.conversation_service import (
    touch_conversation,
    get_conversation,
    update_summary,
)


def create_message(
    db: Session,
    conversation_id: int,
    role: str,
    content: str,
    tenant_id: int,
):
    """
    Create a new message.
    """

    message = Message(
        conversation_id=conversation_id,
        role=role,
        content=content,
        tenant_id=tenant_id,
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    touch_conversation(
        db,
        conversation_id,
    )

    conversation = get_conversation(
        db,
        conversation_id,
    )

    if (
        conversation is not None
        and conversation.message_count > 0
        and conversation.message_count % 20 == 0
    ):
        update_summary(
            db,
            conversation_id,
        )

    return message


def get_messages(
    db: Session,
    conversation_id: int,
):
    """
    Return all messages in chronological order.
    """

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
):
    """
    Build the complete conversation history.
    """

    messages = get_messages(
        db,
        conversation_id,
    )

    history = []

    for message in messages:
        history.append(
            {
                "role": message.role,
                "content": message.content,
            }
        )

    return history


def build_recent_history(
    db: Session,
    conversation_id: int,
    limit: int = 6,
):
    """
    Build the most recent conversation history.

    Returns the last N messages in
    chronological order.
    """

    messages = (
        db.query(Message)
        .filter(
            Message.conversation_id
            == conversation_id
        )
        .order_by(
            Message.created_at.desc()
        )
        .limit(limit)
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


def save_user_message(
    db: Session,
    conversation_id: int,
    content: str,
    tenant_id: int,
):
    """
    Save a user message.
    """

    return create_message(
        db=db,
        conversation_id=conversation_id,
        role="user",
        content=content,
        tenant_id=tenant_id,
    )


def save_assistant_message(
    db: Session,
    conversation_id: int,
    content: str,
    tenant_id: int,
):
    """
    Save an assistant message.
    """

    return create_message(
        db=db,
        conversation_id=conversation_id,
        role="assistant",
        content=content,
        tenant_id=tenant_id,
    )
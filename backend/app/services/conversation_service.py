from datetime import datetime

from sqlalchemy.orm import Session

from app.models.conversation import Conversation

from app.services.summary_service import (
    summarize_conversation,
)


def create_conversation(
    db: Session,
    tenant_id: int,
    title: str | None = None,
):
    """
    Create a new conversation.
    """

    conversation = Conversation(
        tenant_id=tenant_id,
        title=title,
        message_count=0,
        summary=None,
        last_message_at=datetime.utcnow(),
        conversation_metadata={},
    )

    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    return conversation


def get_conversation(
    db: Session,
    conversation_id: int,
):
    """
    Get a conversation by ID.
    """

    return (
        db.query(Conversation)
        .filter(
            Conversation.id == conversation_id
        )
        .first()
    )

def get_conversation_summary(
    db: Session,
    conversation_id: int,
) -> str | None:
    """
    Return the stored conversation summary.
    """

    conversation = get_conversation(
        db,
        conversation_id,
    )

    if conversation is None:
        return None

    return conversation.summary


def touch_conversation(
    db: Session,
    conversation_id: int,
):
    """
    Update conversation statistics after
    a new message is stored.
    """

    conversation = get_conversation(
        db,
        conversation_id,
    )

    if conversation is None:
        return

    conversation.message_count += 1
    conversation.last_message_at = datetime.utcnow()
    conversation.updated_at = datetime.utcnow()

    db.commit()


def update_summary(
    db: Session,
    conversation_id: int,
):
    """
    Generate and store a conversation summary.
    """

    from app.services.message_service import (
        build_chat_history,
    )

    conversation = get_conversation(
        db,
        conversation_id,
    )

    if conversation is None:
        return

    history = build_chat_history(
        db,
        conversation_id,
    )

    summary = summarize_conversation(
        history,
    )

    conversation.summary = summary
    conversation.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(conversation)
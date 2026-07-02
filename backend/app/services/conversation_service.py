from datetime import datetime

from sqlalchemy.orm import Session

from app.models.conversation import (
    Conversation,
)
from app.models.conversation_summary import (
    ConversationSummary,
)


def create_conversation(
    db: Session,
    tenant_id: int,
    title: str | None = None,
):
    conversation = Conversation(
        tenant_id=tenant_id,
        title=title,
        message_count=0,
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
    return (
        db.query(Conversation)
        .filter(
            Conversation.id == conversation_id
        )
        .first()
    )


def increment_message_count(
    db: Session,
    conversation_id: int,
):
    conversation = get_conversation(
        db,
        conversation_id,
    )

    if conversation is None:
        return None

    conversation.message_count += 1
    conversation.last_message_at = (
        datetime.utcnow()
    )

    db.commit()
    db.refresh(conversation)

    return conversation


def get_latest_summary(
    db: Session,
    conversation_id: int,
):
    return (
        db.query(ConversationSummary)
        .filter(
            ConversationSummary.conversation_id
            == conversation_id
        )
        .order_by(
            ConversationSummary.id.desc()
        )
        .first()
    )
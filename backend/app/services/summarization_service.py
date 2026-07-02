from sqlalchemy.orm import Session

from app.models.message import Message
from app.models.conversation_summary import (
    ConversationSummary,
)


def create_summary(
    db: Session,
    tenant_id: int,
    conversation_id: int,
    summary: str,
    start_message_id: int,
    end_message_id: int,
):
    record = ConversationSummary(
        tenant_id=tenant_id,
        conversation_id=conversation_id,
        summary=summary,
        message_start_id=start_message_id,
        message_end_id=end_message_id,
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return record


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
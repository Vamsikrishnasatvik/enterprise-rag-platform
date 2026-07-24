from datetime import datetime

from sqlalchemy.orm import Session

from app.models.conversation import Conversation


def create_conversation(
    db: Session,
    tenant_id: int,
    title: str | None = None,
):
    conversation = Conversation(
        tenant_id=tenant_id,
        title=title,
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


def get_summary(
    db: Session,
    conversation_id: int,
) -> str:

    conversation = get_conversation(
        db=db,
        conversation_id=conversation_id,
    )

    if not conversation:
        return ""

    return conversation.summary or ""


def update_summary(
    db: Session,
    conversation_id: int,
    summary: str,
):
    conversation = get_conversation(
        db=db,
        conversation_id=conversation_id,
    )

    if not conversation:
        return None

    conversation.summary = summary
    conversation.summary_updated_at = datetime.utcnow()

    db.commit()
    db.refresh(conversation)

    return conversation
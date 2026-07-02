from sqlalchemy.orm import Session

from app.models.message import Message
from app.models.conversation import (
    Conversation,
)
from app.models.conversation_summary import (
    ConversationSummary,
)

from app.services.memory_service import (
    generate_conversation_summary,
)

SUMMARY_TRIGGER_MESSAGES = 4


def should_generate_summary(
    conversation: Conversation,
):
    if conversation.message_count == 0:
        return False

    return (
        conversation.message_count
        % SUMMARY_TRIGGER_MESSAGES
        == 0
    )


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


def get_messages_for_summary(
    db: Session,
    conversation_id: int,
):
    latest_summary = get_latest_summary(
        db,
        conversation_id,
    )

    query = (
        db.query(Message)
        .filter(
            Message.conversation_id
            == conversation_id
        )
    )

    if latest_summary:
        query = query.filter(
            Message.id
            > latest_summary.message_end_id
        )

    return (
        query.order_by(
            Message.id
        )
        .all()
    )


def generate_summary_text(
    messages: list[Message],
):
    if not messages:
        return None

    lines = []

    for message in messages:
        lines.append(
            f"{message.role}: {message.content}"
        )

    summary = "\n".join(lines)

    if len(summary) > 4000:
        summary = summary[-4000:]

    return summary


def create_summary(
    db: Session,
    conversation: Conversation,
):
    messages = (
        get_messages_for_summary(
            db,
            conversation.id,
        )
    )

    if not messages:
        return None

    raw_text = (
        generate_summary_text(
            messages
        )
    )

    if raw_text is None:
        return None

    try:
        summary_text = (
            generate_conversation_summary(
                raw_text
            )
        )
    except Exception:
        summary_text = raw_text

    record = ConversationSummary(
        tenant_id=conversation.tenant_id,
        conversation_id=conversation.id,
        summary=summary_text,
        message_start_id=messages[0].id,
        message_end_id=messages[-1].id,
    )

    db.add(record)

    conversation.summary = summary_text

    db.commit()
    db.refresh(record)

    return record
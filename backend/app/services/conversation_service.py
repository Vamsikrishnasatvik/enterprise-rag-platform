import logging
from datetime import datetime

from sqlalchemy.orm import Session

from app.models.conversation import Conversation

logger = logging.getLogger(__name__)

# =============================================================================
# Conversation CRUD
# =============================================================================


def create_conversation(
    db: Session,
    tenant_id: int,
    title: str | None = None,
) -> Conversation:
    """
    Creates a new conversation.
    """

    conversation = Conversation(
        tenant_id=tenant_id,
        title=title,
    )

    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    logger.info(
        "Created conversation | id=%d | tenant=%d",
        conversation.id,
        tenant_id,
    )

    return conversation


def get_conversation(
    db: Session,
    conversation_id: int,
) -> Conversation | None:
    """
    Retrieves a conversation by its ID.
    """

    return (
        db.query(Conversation)
        .filter(
            Conversation.id == conversation_id,
        )
        .first()
    )


# =============================================================================
# Conversation Summary
# =============================================================================


def get_summary(
    db: Session,
    conversation_id: int,
) -> str:
    """
    Returns the stored conversation summary.
    """

    conversation = get_conversation(
        db=db,
        conversation_id=conversation_id,
    )

    if conversation is None:
        return ""

    return conversation.summary or ""


def update_summary(
    db: Session,
    conversation_id: int,
    summary: str,
) -> Conversation | None:
    """
    Updates the conversation summary.
    """

    conversation = get_conversation(
        db=db,
        conversation_id=conversation_id,
    )

    if conversation is None:
        return None

    conversation.summary = summary
    conversation.summary_updated_at = datetime.utcnow()

    db.commit()
    db.refresh(conversation)

    logger.info(
        "Updated conversation summary | id=%d",
        conversation_id,
    )

    return conversation
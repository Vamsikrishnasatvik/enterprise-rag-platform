from sqlalchemy.orm import Session

from app.services.message_service import (
    build_recent_history,
)


def load_conversation_memory(
    db: Session,
    conversation_id: int | None,
    limit: int = 6,
) -> list[dict]:
    """
    Phase 3.7.3

    Load the recent conversation history.

    Returns:
        [
            {
                "role": "user",
                "content": "..."
            },
            ...
        ]
    """

    if conversation_id is None:
        return []

    return build_recent_history(
        db=db,
        conversation_id=conversation_id,
        limit=limit,
    )
from sqlalchemy.orm import Session

from app.services.conversation_service import (
    get_summary,
)
from app.services.message_service import (
    get_chat_history,
    get_recent_messages,
)


class MemoryService:
    """
    Responsible for preparing conversation memory
    for the agent workflow.

    Version 2:
    - Load conversation summary
    - Load recent messages
    - Build memory context

    Future versions:
    - Semantic memory retrieval
    - Long-term memory
    """

    def get_memory_context(
        self,
        db: Session,
        conversation_id: int,
    ) -> dict:

        summary = get_summary(
            db=db,
            conversation_id=conversation_id,
        )

        recent_messages = get_recent_messages(
            db=db,
            conversation_id=conversation_id,
            limit=10,
        )

        # Keep temporarily for backward compatibility
        conversation_history = get_chat_history(
            db=db,
            conversation_id=conversation_id,
        )

        memory_context = self._build_memory_context(
            summary=summary,
            recent_messages=recent_messages,
        )

        return {
            "conversation_summary": summary,
            "recent_messages": recent_messages,
            "conversation_history": conversation_history,
            "memory_context": memory_context,
        }

    def _build_memory_context(
        self,
        summary: str | None,
        recent_messages: list[dict],
    ) -> str:

        sections = []

        if summary:
            sections.append(
                f"Conversation Summary:\n{summary}"
            )

        if recent_messages:

            lines = []

            for message in recent_messages:

                role = message["role"].capitalize()

                lines.append(
                    f"{role}: {message['content']}"
                )

            sections.append(
                "Recent Messages:\n"
                + "\n".join(lines)
            )

        return "\n\n".join(sections)


memory_service = MemoryService()
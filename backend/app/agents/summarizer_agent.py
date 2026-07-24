from app.agents.base import BaseAgent

from app.services.conversation_service import (
    update_summary,
)
from app.services.llm_service import (
    generate_summary,
)
from app.services.message_service import (
    get_chat_history,
)


class SummarizerAgent(BaseAgent):
    """
    Generates and updates the conversation summary.
    """

    def __init__(self):
        super().__init__("SummarizerAgent")

    def run(
        self,
        db,
        conversation_id: int,
    ) -> str:

        history = get_chat_history(
            db=db,
            conversation_id=conversation_id,
        )

        if not history:
            return ""

        conversation = self._format_conversation(
            history
        )

        summary = generate_summary(
            conversation
        )

        update_summary(
            db=db,
            conversation_id=conversation_id,
            summary=summary,
        )

        return summary

    def _format_conversation(
        self,
        history: list[dict],
    ) -> str:

        lines = []

        for message in history:

            role = message["role"].capitalize()

            lines.append(
                f"{role}: {message['content']}"
            )

        return "\n".join(lines)
from sqlalchemy.orm import Session

from app.prompts.memory_prompt import MEMORY_PROMPT

from app.services.conversation_service import (
    get_summary,
)

from app.services.llm_service import call_llm

from app.services.message_service import (
    get_chat_history,
    get_recent_messages,
)


class MemoryService:
    """
    Responsible for preparing conversation memory
    for the agent workflow.

    Version 3:
    - Load conversation summary
    - Load recent messages
    - Load full history
    - Generate intelligent memory using the LLM
    - Fall back to deterministic memory if LLM fails

    Future versions:
    - Semantic memory retrieval
    - Long-term memory
    """

    def get_memory_context(
        self,
        db: Session,
        conversation_id: int,
        question: str,
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

        conversation_history = get_chat_history(
            db=db,
            conversation_id=conversation_id,
        )

        memory_context = self.generate_memory_context(
            summary=summary,
            history=conversation_history,
            question=question,
        )

        return {
            "conversation_summary": summary,
            "recent_messages": recent_messages,
            "conversation_history": conversation_history,
            "memory_context": memory_context,
        }

    def generate_memory_context(
        self,
        summary: str | None,
        history: list[dict],
        question: str,
    ) -> str:
        """
        Uses the LLM to create an intelligent memory summary
        for downstream agents.
        """

        history_text = "\n".join(
            f"{message['role'].capitalize()}: {message['content']}"
            for message in history
        )

        prompt = MEMORY_PROMPT.format(
            summary=summary or "",
            history=history_text,
            question=question,
        )

        try:
            return call_llm(prompt).strip()

        except Exception:
            return self._build_memory_context(
                summary=summary,
                recent_messages=history[-10:],
            )

    def _build_memory_context(
        self,
        summary: str |None,
        recent_messages: list[dict],
    ) -> str:
        """
        Deterministic fallback if the Memory LLM fails.
        """

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
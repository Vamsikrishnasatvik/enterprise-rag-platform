import logging

from sqlalchemy.orm import Session

from app.prompts.memory_prompt import MEMORY_PROMPT
from app.services.conversation_service import get_summary
from app.services.llm_service import call_llm
from app.services.message_service import (
    get_chat_history,
    get_recent_messages,
)

logger = logging.getLogger(__name__)

# =============================================================================
# Constants
# =============================================================================

RECENT_MESSAGE_LIMIT = 10


# =============================================================================
# Memory Service
# =============================================================================


class MemoryService:
    """
    Responsible for preparing conversation memory for the
    Agentic RAG workflow.

    Responsibilities:
        - Load conversation summary
        - Load recent messages
        - Load conversation history
        - Generate intelligent memory context using the LLM
        - Fall back to deterministic memory if the LLM fails

    Future Enhancements:
        - Semantic memory retrieval
        - Long-term memory
        - Personalized memory ranking
    """

    def get_memory_context(
        self,
        db: Session,
        conversation_id: int,
        question: str,
    ) -> dict:
        """
        Builds the complete memory package consumed by downstream agents.
        """

        logger.info(
            "Loading conversation memory | conversation=%s",
            conversation_id,
        )

        summary = get_summary(
            db=db,
            conversation_id=conversation_id,
        )

        recent_messages = get_recent_messages(
            db=db,
            conversation_id=conversation_id,
            limit=RECENT_MESSAGE_LIMIT,
        )

        conversation_history = get_chat_history(
            db=db,
            conversation_id=conversation_id,
        )

        memory_context = self.generate_memory_context(
            summary=summary,
            history=conversation_history,
            question=question,
            recent_messages=recent_messages,
        )

        logger.info(
            "Memory prepared | summary=%s | recent_messages=%d | history=%d",
            "yes" if summary else "no",
            len(recent_messages),
            len(conversation_history),
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
        recent_messages: list[dict],
    ) -> str:
        """
        Generates an intelligent memory summary using the LLM.

        Falls back to deterministic memory generation if the
        LLM request fails.
        """

        history_text = self._format_messages(history)

        prompt = MEMORY_PROMPT.format(
            summary=summary or "",
            history=history_text,
            question=question,
        )

        logger.info("Generating memory context using LLM.")

        try:
            return call_llm(prompt).strip()

        except Exception:

            logger.exception(
                "Memory generation failed. Using deterministic fallback."
            )

            return self._build_memory_context(
                summary=summary,
                recent_messages=recent_messages,
            )

    def _build_memory_context(
        self,
        summary: str | None,
        recent_messages: list[dict],
    ) -> str:
        """
        Builds a deterministic memory context when the LLM
        is unavailable.
        """

        sections = []

        if summary:
            sections.append(
                f"Conversation Summary:\n{summary}"
            )

        if recent_messages:
            sections.append(
                "Recent Messages:\n"
                + self._format_messages(recent_messages)
            )

        return "\n\n".join(sections)

    @staticmethod
    def _format_messages(
        messages: list[dict],
    ) -> str:
        """
        Formats conversation messages into a readable transcript.
        """

        return "\n".join(
            f"{message['role'].capitalize()}: {message['content']}"
            for message in messages
        )


memory_service = MemoryService()
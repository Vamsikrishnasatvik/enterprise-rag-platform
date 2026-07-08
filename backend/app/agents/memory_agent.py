import logging

from app.agents.base import BaseAgent
from app.graph.state import GraphState

from app.db.session import SessionLocal

from app.services.message_service import (
    build_recent_history,
)

from app.services.conversation_service import (
    get_conversation_summary,
)

from app.services.memory_rewrite_service import (
    rewrite_query,
)

logger = logging.getLogger(__name__)


class MemoryAgent(BaseAgent):
    """
    Phase 3.8

    Loads the conversation summary and recent history,
    then rewrites follow-up questions into standalone queries.
    """

    def run(
        self,
        state: GraphState,
    ) -> GraphState:

        logger.info("MemoryAgent started")

        state.setdefault("execution_trace", [])

        conversation_id = state.get(
            "conversation_id"
        )

        # New conversation
        if not conversation_id:

            logger.info(
                "No conversation history."
            )

            state["chat_history"] = []
            state["rewritten_query"] = (
                state["question"]
            )

            state["execution_trace"].append(
                {
                    "agent": "MemoryAgent",
                    "status": "completed",
                    "summary": False,
                    "recent_messages": 0,
                    "rewritten": False,
                }
            )

            return state

        db = SessionLocal()

        try:

            summary = get_conversation_summary(
                db,
                conversation_id,
            )

            recent_history = build_recent_history(
                db,
                conversation_id,
                limit=6,
            )

        finally:
            db.close()

        state["chat_history"] = recent_history

        rewritten = rewrite_query(
            question=state["question"],
            summary=summary,
            recent_history=recent_history,
        )

        state["rewritten_query"] = rewritten

        logger.info(
            "Original Question: %s",
            state["question"],
        )

        logger.info(
            "Rewritten Question: %s",
            rewritten,
        )

        state["execution_trace"].append(
            {
                "agent": "MemoryAgent",
                "status": "completed",
                "summary": summary is not None,
                "recent_messages": len(
                    recent_history
                ),
                "rewritten": (
                    rewritten
                    != state["question"]
                ),
            }
        )

        logger.info(
            "MemoryAgent completed"
        )

        return state
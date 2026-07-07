import logging

from app.agents.base import BaseAgent
from app.graph.state import GraphState

from app.services.llm_service import (
    generate_answer,
)

logger = logging.getLogger(__name__)


class AnswerAgent(BaseAgent):

    def run(
        self,
        state: GraphState,
    ) -> GraphState:

        logger.info("AnswerAgent started")

        # Initialize runtime state if missing
        state.setdefault("execution_trace", [])

        answer = generate_answer(
            question=state["question"],
            context=state["context"],
        )

        state["answer"] = answer

        state["execution_trace"].append(
            {
                "agent": "AnswerAgent",
                "status": "completed",
            }
        )

        logger.info("AnswerAgent completed")

        return state
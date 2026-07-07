import logging

from app.agents.base import BaseAgent
from app.graph.state import GraphState

from app.services.verifier_service import (
    verify_retrieval,
)

logger = logging.getLogger(__name__)


class VerifierAgent(BaseAgent):

    def run(
        self,
        state: GraphState,
    ) -> GraphState:

        logger.info("VerifierAgent started")

        state.setdefault("execution_trace", [])

        result = verify_retrieval(
            retrieved_chunks=state["retrieved_chunks"],
            context=state["context"],
        )

        state["confidence_score"] = (
            result.confidence_score
        )

        state["needs_retry"] = (
            result.needs_retry
        )

        state["verification_reason"] = (
            result.verification_reason
        )

        state["execution_trace"].append(
            {
                "agent": "VerifierAgent",
                "status": "completed",
                "confidence": result.confidence_score,
            }
        )

        logger.info(
            "VerifierAgent completed (confidence %.2f)",
            result.confidence_score,
        )

        return state
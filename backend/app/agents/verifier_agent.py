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
        state.setdefault("retrieval_attempts", 1)
        state.setdefault("max_retrieval_attempts", 2)

        result = verify_retrieval(
            retrieved_chunks=state["reranked_chunks"],
            context=state["context"],
        )

        logger.info(
            "Confidence %.2f | Retry %s | %s",
            result.confidence_score,
            result.needs_retry,
            result.verification_reason,
        )

        state["confidence_score"] = result.confidence_score
        state["needs_retry"] = result.needs_retry
        state["verification_reason"] = (
            result.verification_reason
        )

        state["execution_trace"].append(
            {
                "agent": "VerifierAgent",
                "status": "completed",
                "confidence": result.confidence_score,
                "retry": result.needs_retry,
                "reason": result.verification_reason,
                "attempt": state["retrieval_attempts"],
            }
        )

        # Only stop retrying if we've already used
        # all allowed retrieval attempts.
        if (
            state["needs_retry"]
            and state["retrieval_attempts"]
            >= state["max_retrieval_attempts"]
        ):
            logger.info(
                "Maximum retrieval attempts reached."
            )

            state["needs_retry"] = False

            state["verification_reason"] = (
                "Maximum retrieval attempts reached."
            )

        # Increment AFTER the routing decision has been recorded.
        state["retrieval_attempts"] += 1

        logger.info(
            "VerifierAgent completed (confidence %.2f)",
            result.confidence_score,
        )

        return state
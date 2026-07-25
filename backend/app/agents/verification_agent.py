import logging

from app.agents.base import BaseAgent
from app.graph.state import GraphState

from app.services.verification_service import verify_answer

logger = logging.getLogger(__name__)


class VerificationAgent(BaseAgent):

    def __init__(self):
        super().__init__("VerificationAgent")

    def run(
        self,
        state: GraphState,
    ) -> GraphState:

        # ---------------------------------------------------------
        # Skip if no retrieval happened
        # ---------------------------------------------------------

        if not state.get("retrieved_chunks"):

            logger.info(
                "Verification skipped (no retrieved chunks)."
            )

            return state

        # ---------------------------------------------------------
        # Verify Answer
        # ---------------------------------------------------------

        verification = verify_answer(
            question=state["question"],
            answer=state["answer"],
            context=state.get(
                "retrieval_context",
                "",
            ),
        )

        # ---------------------------------------------------------
        # Store Verification
        # ---------------------------------------------------------

        state["verification"] = verification

        state["verification_passed"] = verification.get(
            "supported",
            False,
        )

        state["verification_reason"] = verification.get(
            "reason",
            "",
        )

        # ---------------------------------------------------------
        # Retry Decision
        # ---------------------------------------------------------

        confidence = verification.get(
            "confidence",
            0.0,
        )

        retry = (
            not verification.get(
                "supported",
                False,
            )
            or confidence < 0.60
        )

        state["retry_required"] = retry

        # ---------------------------------------------------------
        # Execution Trace
        # ---------------------------------------------------------

        state.setdefault(
            "execution_trace",
            [],
        ).append(
            {
                "agent": "VerificationAgent",
                "supported": verification.get(
                    "supported",
                    False,
                ),
                "confidence": confidence,
                "retry": retry,
            }
        )

        logger.info(
            "Verification Result: %s",
            verification,
        )

        return state
import logging

from app.agents.base import BaseAgent
from app.graph.state import GraphState
from app.services.verification_service import verify_answer

logger = logging.getLogger(__name__)

# =============================================================================
# Constants
# =============================================================================

LOW_RETRIEVAL_THRESHOLD = 0.55
VERIFICATION_CONFIDENCE_THRESHOLD = 0.60

FALLBACK_ANSWER = (
    "I couldn't find this information in the retrieved documents."
)


class VerificationAgent(BaseAgent):
    """
    Verifies that the generated answer is fully supported by the
    retrieved context and determines whether another retrieval
    attempt is required.
    """

    def __init__(self):
        super().__init__("VerificationAgent")

    def run(
        self,
        state: GraphState,
    ) -> GraphState:
        """
        Verify the generated answer against the retrieved context.
        """

        retrieved_chunks = state.get("retrieved_chunks", [])
        retrieval_score = state.get("retrieval_score", 0.0)
        retrieved_documents = state.get(
            "retrieved_document_count",
            0,
        )
        answer = state.get("answer", "")
        context = state.get("retrieval_context", "")

        # ---------------------------------------------------------
        # Skip Verification
        # ---------------------------------------------------------

        if not retrieved_chunks:

            logger.info(
                "Verification skipped | no retrieved chunks."
            )

            return state

        # ---------------------------------------------------------
        # Deterministic Pass
        # ---------------------------------------------------------

        if (
            retrieval_score < LOW_RETRIEVAL_THRESHOLD
            and retrieved_documents > 0
            and answer.strip() == FALLBACK_ANSWER
        ):

            logger.info(
                "Low-confidence retrieval with fallback answer. "
                "Skipping LLM verification."
            )

            verification = {
                "supported": True,
                "confidence": 0.92,
                "missing_information": (
                    "The retrieved documents do not contain the requested information."
                ),
                "hallucinations": [],
                "reason": (
                    "Fallback response is fully supported because the "
                    "retrieved documents do not contain the requested information."
                ),
            }

            state.update(
                {
                    "verification": verification,
                    "verification_passed": True,
                    "verification_reason": verification["reason"],
                    "retry_required": False,
                }
            )

            state.setdefault(
                "execution_trace",
                [],
            ).append(
                {
                    "agent": self.name,
                    "supported": True,
                    "confidence": 0.92,
                    "retry": False,
                    "reason": "low_confidence_fallback",
                }
            )

            return state

        # ---------------------------------------------------------
        # LLM Verification
        # ---------------------------------------------------------

        verification = verify_answer(
            question=state["question"],
            answer=answer,
            context=context,
        )

        try:
            confidence = float(
                verification.get(
                    "confidence",
                    0.0,
                )
            )
        except (TypeError, ValueError):

            logger.warning(
                "Invalid verification confidence received."
            )

            confidence = 0.0

        supported = verification.get(
            "supported",
            False,
        )

        retry = (
            not supported
            or confidence < VERIFICATION_CONFIDENCE_THRESHOLD
        )

        state.update(
            {
                "verification": verification,
                "verification_passed": supported,
                "verification_reason": verification.get(
                    "reason",
                    "",
                ),
                "retry_required": retry,
            }
        )

        logger.info(
            "Verification | supported=%s | confidence=%.2f | retry=%s",
            supported,
            confidence,
            retry,
        )

        # ---------------------------------------------------------
        # Execution Trace
        # ---------------------------------------------------------

        state.setdefault(
            "execution_trace",
            [],
        ).append(
            {
                "agent": self.name,
                "supported": supported,
                "confidence": confidence,
                "retry": retry,
            }
        )

        return state
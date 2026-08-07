import logging

from app.agents.base import BaseAgent
from app.graph.state import GraphState
from app.services.reflection_service import evaluate_answer

logger = logging.getLogger(__name__)

# =============================================================================
# Constants
# =============================================================================

LOW_RETRIEVAL_THRESHOLD = 0.55
REFLECTION_CONFIDENCE_THRESHOLD = 0.60

FALLBACK_ANSWER = (
    "I couldn't find this information in the retrieved documents."
)


class ReflectionAgent(BaseAgent):
    """
    Evaluates the generated answer for grounding,
    completeness, and confidence.

    Determines whether another retrieval attempt
    should be performed before verification.
    """

    def __init__(self):
        super().__init__("ReflectionAgent")

    def run(self, state: GraphState) -> GraphState:
        """
        Evaluate the generated answer using the Reflection LLM.
        """

        retrieved_chunks = state.get("retrieved_chunks", [])
        retrieval_score = state.get("retrieval_score", 0.0)
        answer = state.get("answer", "")
        context = state.get("retrieval_context", "")

        # ---------------------------------------------------------
        # Skip Reflection
        # ---------------------------------------------------------

        if not retrieved_chunks:
            logger.info(
                "Reflection skipped | no retrieved chunks."
            )
            return state

        # ---------------------------------------------------------
        # Deterministic Pass
        # ---------------------------------------------------------

        if (
            retrieval_score < LOW_RETRIEVAL_THRESHOLD
            and answer.strip() == FALLBACK_ANSWER
        ):

            logger.info(
                "Low-confidence retrieval with fallback answer. "
                "Skipping LLM reflection."
            )

            reflection = {
                "passed": True,
                "confidence": 0.92,
                "grounded": True,
                "retry": False,
                "issues": [],
                "feedback": (
                    "Retrieved documents do not contain the requested "
                    "information. Fallback response is correct."
                ),
            }

            state.update(
                {
                    "reflection": reflection,
                    "confidence_score": reflection["confidence"],
                    "needs_retry": False,
                    "retry_required": False,
                    "retry_reason": "",
                }
            )

            state.setdefault(
                "execution_trace",
                [],
            ).append(
                {
                    "agent": self.name,
                    "passed": True,
                    "confidence": 0.92,
                    "retry": False,
                    "reason": "low_confidence_fallback",
                }
            )

            return state

        # ---------------------------------------------------------
        # Log Context
        # ---------------------------------------------------------

        logger.info(
            "Reflection Context:\n%s",
            context,
        )

        logger.info(
            "Reflection Answer:\n%s",
            answer,
        )

        # ---------------------------------------------------------
        # Evaluate Answer
        # ---------------------------------------------------------

        reflection = evaluate_answer(
            question=state["question"],
            answer=answer,
            context=context,
        )

        # ---------------------------------------------------------
        # Normalize Confidence
        # ---------------------------------------------------------

        try:
            confidence = float(
                reflection.get(
                    "confidence",
                    0.0,
                )
            )
        except (TypeError, ValueError):

            logger.warning(
                "Invalid reflection confidence received."
            )

            confidence = 0.0

        # ---------------------------------------------------------
        # Retry Decision
        # ---------------------------------------------------------

        needs_retry = (
            reflection.get("retry", False)
            or confidence < REFLECTION_CONFIDENCE_THRESHOLD
        )

        # ---------------------------------------------------------
        # Store Reflection
        # ---------------------------------------------------------

        state.update(
            {
                "reflection": reflection,
                "confidence_score": confidence,
                "needs_retry": needs_retry,
                "retry_required": needs_retry,
                "retry_reason": reflection.get(
                    "feedback",
                    "",
                ),
            }
        )

        logger.info(
            "Reflection | passed=%s | confidence=%.2f | retry=%s",
            reflection.get("passed", False),
            confidence,
            needs_retry,
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
                "passed": reflection.get(
                    "passed",
                    False,
                ),
                "confidence": confidence,
                "retry": needs_retry,
            }
        )

        return state
import logging

from app.agents.base import BaseAgent
from app.graph.state import GraphState

from app.services.reflection_service import evaluate_answer

logger = logging.getLogger(__name__)


class ReflectionAgent(BaseAgent):

    def __init__(self):
        super().__init__("ReflectionAgent")

    def run(self, state: GraphState) -> GraphState:

        # ---------------------------------------------------------
        # Skip Reflection if no retrieval occurred
        # ---------------------------------------------------------

        if not state.get("retrieved_chunks"):
            logger.info(
                "Reflection skipped (no retrieved chunks)."
            )
            return state

        # ---------------------------------------------------------
        # Log Context
        # ---------------------------------------------------------

        logger.info(
            "Reflection Context:\n%s",
            state.get(
                "retrieval_context",
                "",
            ),
        )

        logger.info(
            "Reflection Answer:\n%s",
            state.get(
                "answer",
                "",
            ),
        )

        # ---------------------------------------------------------
        # Evaluate Answer
        # ---------------------------------------------------------

        reflection = evaluate_answer(
            question=state["question"],
            answer=state["answer"],
            context=state.get(
                "retrieval_context",
                "",
            ),
        )

        # ---------------------------------------------------------
        # Log Reflection Result
        # ---------------------------------------------------------

        logger.info(
            "Reflection Result: %s",
            reflection,
        )

        # ---------------------------------------------------------
        # Store Reflection
        # ---------------------------------------------------------

        state["reflection"] = reflection

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
            confidence = 0.0

        state["confidence_score"] = confidence

        # ---------------------------------------------------------
        # Retry Decision
        # ---------------------------------------------------------

        needs_retry = (
            reflection.get("retry", False)
            or confidence < 0.60
        )

        state["needs_retry"] = needs_retry
        state["retry_required"] = needs_retry

        state["retry_reason"] = reflection.get(
            "feedback",
            "",
        )

        # ---------------------------------------------------------
        # Execution Trace
        # ---------------------------------------------------------

        state.setdefault(
            "execution_trace",
            [],
        ).append(
            {
                "agent": "ReflectionAgent",
                "passed": reflection.get(
                    "passed",
                    False,
                ),
                "confidence": confidence,
                "retry": needs_retry,
            }
        )

        return state
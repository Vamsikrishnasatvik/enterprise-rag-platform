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
        # Deterministic Pass:
        # Low retrieval score + fallback answer
        # ---------------------------------------------------------

        if (
            state.get("retrieval_score", 0.0) < 0.55
            and state.get("answer", "").strip()
            == "I couldn't find this information in the retrieved documents."
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

            state["reflection"] = reflection
            state["confidence_score"] = reflection["confidence"]
            state["needs_retry"] = False
            state["retry_required"] = False
            state["retry_reason"] = ""

            state.setdefault(
                "execution_trace",
                [],
            ).append(
                {
                    "agent": "ReflectionAgent",
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
        # Evaluate Answer using LLM
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
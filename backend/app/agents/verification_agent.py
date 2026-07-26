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
        # Deterministic Pass
        # Low retrieval confidence + fallback answer
        # ---------------------------------------------------------

        if (
            state.get("retrieval_score", 0.0) < 0.55
            and state.get("retrieved_document_count", 0) > 0
            and state.get("answer", "").strip()
            == "I couldn't find this information in the retrieved documents."
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
                    "Fallback response is fully supported because the retrieved "
                    "documents do not contain the requested information."
                ),
            }

            state["verification"] = verification
            state["verification_passed"] = True
            state["verification_reason"] = verification["reason"]
            state["retry_required"] = False

            state.setdefault(
                "execution_trace",
                [],
            ).append(
                {
                    "agent": "VerificationAgent",
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
            answer=state["answer"],
            context=state.get(
                "retrieval_context",
                "",
            ),
        )

        logger.info(
            "Verification Result: %s",
            verification,
        )

        # ---------------------------------------------------------
        # Store Verification
        # ---------------------------------------------------------

        state["verification"] = verification

        supported = verification.get(
            "supported",
            False,
        )

        confidence = float(
            verification.get(
                "confidence",
                0.0,
            )
        )

        state["verification_passed"] = supported

        state["verification_reason"] = verification.get(
            "reason",
            "",
        )

        retry = (
            not supported
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
                "supported": supported,
                "confidence": confidence,
                "retry": retry,
            }
        )

        return state
import logging

from app.agents.base import BaseAgent
from app.answer_generators.factory import AnswerFactory
from app.graph.state import GraphState

logger = logging.getLogger(__name__)

# =============================================================================
# Constants
# =============================================================================

RETRIEVAL_THRESHOLDS = {
    "semantic": 0.55,
    "keyword": 0.30,
    "hybrid": 0.55,
}

DEFAULT_QUERY_TYPE = "knowledge"


class AnswerAgent(BaseAgent):
    """
    Generates the final answer using the appropriate answer generator.

    This agent selects the answer generation strategy based on the query type,
    validates retrieval quality, and falls back to a safe response when
    insufficient evidence is available.
    """

    def __init__(self):
        super().__init__("AnswerAgent")

    def run(
        self,
        state: GraphState,
    ) -> GraphState:

        query_type = (
            state.get(
                "query_type",
                DEFAULT_QUERY_TYPE,
            )
            .strip()
            .lower()
        )

        retrieval_strategy = (
            state.get(
                "retrieval_strategy",
                "semantic",
            )
            .strip()
            .lower()
        )

        retrieval_score = float(
            state.get(
                "retrieval_score",
                0.0,
            )
        )

        threshold = RETRIEVAL_THRESHOLDS.get(
            retrieval_strategy,
            RETRIEVAL_THRESHOLDS["semantic"],
        )

        retrieved_documents = state.get(
            "retrieved_document_count",
            0,
        )

        # ---------------------------------------------------------
        # Select Generator
        # ---------------------------------------------------------

        try:
            generator = AnswerFactory.get(query_type)

        except Exception:

            logger.warning(
                "Unknown query type '%s'. Falling back to '%s'.",
                query_type,
                DEFAULT_QUERY_TYPE,
            )

            query_type = DEFAULT_QUERY_TYPE
            generator = AnswerFactory.get(query_type)

        # ---------------------------------------------------------
        # Debug Logging
        # ---------------------------------------------------------

        logger.info("=" * 70)
        logger.info("AnswerAgent")
        logger.info("Query Type      : %s", query_type)
        logger.info("Generator       : %s", generator.__class__.__name__)
        logger.info("Strategy        : %s", retrieval_strategy)
        logger.info("Retrieval Score : %.4f", retrieval_score)
        logger.info("Threshold       : %.4f", threshold)
        logger.info("Retrieved Docs  : %d", retrieved_documents)
        logger.info(
            "Retrieved Chunks: %d",
            len(state.get("retrieved_chunks", [])),
        )
        logger.info("=" * 70)

        # ---------------------------------------------------------
        # No Supporting Documents
        # ---------------------------------------------------------

        if retrieved_documents == 0:

            logger.warning(
                "No supporting documents retrieved."
            )

            state.update(
                {
                    "answer": self._fallback_answer(),
                }
            )

            state.setdefault(
                "execution_trace",
                [],
            ).append(
                {
                    "agent": self.name,
                    "strategy": "LowConfidenceFallback",
                    "retrieval_strategy": retrieval_strategy,
                    "retrieval_score": retrieval_score,
                    "threshold": threshold,
                }
            )

            return state

        # ---------------------------------------------------------
        # Generate Answer
        # ---------------------------------------------------------

        logger.info(
            "Generating answer using %s",
            generator.__class__.__name__,
        )

        try:

            answer = generator.generate(state)

        except Exception as exc:

            logger.exception(
                "Answer generation failed using %s.",
                generator.__class__.__name__,
            )

            answer = self._fallback_answer()

        state.update(
            {
                "answer": answer,
            }
        )

        state.setdefault(
            "execution_trace",
            [],
        ).append(
            {
                "agent": self.name,
                "query_type": query_type,
                "strategy": generator.__class__.__name__,
                "retrieval_strategy": retrieval_strategy,
                "retrieval_score": retrieval_score,
                "threshold": threshold,
            }
        )

        return state

    @staticmethod
    def _fallback_answer() -> str:
        """
        Return a safe fallback response when answer generation
        cannot produce a grounded answer.
        """

        return (
            "I couldn't find this information in the retrieved documents."
        )
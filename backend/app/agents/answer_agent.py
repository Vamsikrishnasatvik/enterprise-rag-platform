import logging

from app.agents.base import BaseAgent
from app.answer_generators.factory import AnswerFactory
from app.graph.state import GraphState

logger = logging.getLogger(__name__)

MIN_RETRIEVAL_SCORE = 0.55


class AnswerAgent(BaseAgent):

    def __init__(self):
        super().__init__("AnswerAgent")

    def run(
        self,
        state: GraphState,
    ) -> GraphState:

        # ---------------------------------------------------------
        # Select Answer Generation Strategy
        # ---------------------------------------------------------

        query_type = state.get(
            "query_type",
            "knowledge",
        )

        retrieval_score = float(
            state.get(
                "retrieval_score",
                0.0,
            )
        )

        next_node = state.get("next_node")

        generator = AnswerFactory.get(query_type)

        # ---------------------------------------------------------
        # Debug Logging
        # ---------------------------------------------------------

        logger.info("=" * 70)
        logger.info("AnswerAgent")
        logger.info("Query Type      : %s", query_type)
        logger.info("Next Node       : %s", next_node)
        logger.info("Retrieval Score : %.4f", retrieval_score)
        logger.info("Threshold       : %.4f", MIN_RETRIEVAL_SCORE)
        logger.info(
            "Retrieved Chunks: %d",
            len(state.get("retrieved_chunks", [])),
        )
        logger.info("=" * 70)

        # ---------------------------------------------------------
        # Low Retrieval Confidence Guard
        # ---------------------------------------------------------

        if (
            next_node == "retriever"
            and retrieval_score < MIN_RETRIEVAL_SCORE
        ):

            logger.warning(
                "Using fallback answer because retrieval score %.4f "
                "is below threshold %.4f",
                retrieval_score,
                MIN_RETRIEVAL_SCORE,
            )

            state["answer"] = self._fallback_answer()

            state.setdefault(
                "execution_trace",
                [],
            ).append(
                {
                    "agent": "AnswerAgent",
                    "strategy": "LowConfidenceFallback",
                    "retrieval_score": retrieval_score,
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

        state["answer"] = generator.generate(state)

        state.setdefault(
            "execution_trace",
            [],
        ).append(
            {
                "agent": "AnswerAgent",
                "query_type": query_type,
                "strategy": generator.__class__.__name__,
                "retrieval_score": retrieval_score,
            }
        )

        return state

    @staticmethod
    def _fallback_answer() -> str:
        return (
            "I couldn't find this information in the retrieved documents."
        )
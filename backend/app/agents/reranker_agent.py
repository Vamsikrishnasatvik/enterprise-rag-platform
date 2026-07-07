import logging

from app.agents.base import BaseAgent
from app.graph.state import GraphState

from app.services.reranker_service import (
    rerank_chunks,
)

from app.services.context_service import (
    build_context,
)

logger = logging.getLogger(__name__)


class RerankerAgent(BaseAgent):
    """
    Phase 3.5.2

    Semantic reranks retrieved chunks before verification.
    """

    def run(
        self,
        state: GraphState,
    ) -> GraphState:

        logger.info("RerankerAgent started")

        state.setdefault("execution_trace", [])
        state.setdefault("retrieved_chunks", [])
        state.setdefault("reranked_chunks", [])

        reranked = rerank_chunks(
            query=(
                state["rewritten_query"]
                or state["question"]
            ),
            chunks=state["retrieved_chunks"],
        )

        logger.info(
            "Top reranked score: %.4f",
            reranked[0]["rerank_score"]
            if reranked else 0,
        )

        state["reranked_chunks"] = reranked

        state["context"] = build_context(
            reranked
        )

        state["execution_trace"].append(
            {
                "agent": "RerankerAgent",
                "status": "completed",
                "chunks_reranked": len(reranked),
            }
        )

        logger.info(
            "RerankerAgent completed - %d chunks reranked",
            len(reranked),
        )

        return state
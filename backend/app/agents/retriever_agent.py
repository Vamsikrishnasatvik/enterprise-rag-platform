import logging

from app.agents.base import BaseAgent
from app.graph.state import GraphState

from app.services.retrieval_service import (
    search_chunks,
)

logger = logging.getLogger(__name__)


class RetrieverAgent(BaseAgent):
    """
    Retrieves relevant chunks only.

    Phase 3.5:
    Context construction is handled by the RerankerAgent.
    """

    def run(
        self,
        state: GraphState,
    ) -> GraphState:

        logger.info("RetrieverAgent started")

        state.setdefault("execution_trace", [])
        state.setdefault("metadata_filters", {})
        state.setdefault("retrieved_chunks", [])
        state.setdefault("execution_plan", {})
        state.setdefault("search_limit", 3)
        state.setdefault("retrieval_strategy", "semantic")
        state.setdefault("retrieval_attempts", 0)

        query = (
            state["rewritten_query"]
            or state["question"]
        )

        execution_plan = state["execution_plan"]

        limit = execution_plan.get(
            "retrieval_count",
            state["search_limit"],
        )

        # Adaptive retry
        if state["retrieval_attempts"] >= 1:
            limit += 2 * state["retrieval_attempts"]

            logger.info(
                "Retry retrieval detected. Increasing limit to %d",
                limit,
            )

        filters = state["metadata_filters"]

        strategy = execution_plan.get(
            "search_strategy",
            state["retrieval_strategy"],
        )

        logger.info(
            "Retrieval strategy: %s | limit: %d",
            strategy,
            limit,
        )

        results = search_chunks(
            query=query,
            limit=limit,
            metadata_filters=filters,
        )

        retrieved_chunks = []

        for result in results:
            retrieved_chunks.append(
                {
                    "chunk_id": result.payload["chunk_id"],
                    "document_id": result.payload["document_id"],
                    "content": result.payload["content"],
                    "score": result.score,
                }
            )

        state["retrieved_chunks"] = retrieved_chunks

        state["execution_trace"].append(
            {
                "agent": "RetrieverAgent",
                "status": "completed",
                "chunks_retrieved": len(retrieved_chunks),
                "retrieval_attempt": state[
                    "retrieval_attempts"
                ],
                "search_limit": limit,
            }
        )

        logger.info(
            "RetrieverAgent completed - %d chunks retrieved",
            len(retrieved_chunks),
        )

        return state
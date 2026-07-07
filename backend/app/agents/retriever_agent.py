import logging

from app.agents.base import BaseAgent
from app.graph.state import GraphState

from app.services.retrieval_service import (
    search_chunks,
)

from app.services.context_service import (
    build_context,
)

logger = logging.getLogger(__name__)


class RetrieverAgent(BaseAgent):
    """
    Retrieves relevant chunks and builds context.
    """

    def run(
        self,
        state: GraphState,
    ) -> GraphState:

        logger.info("RetrieverAgent started")

        # Initialize runtime state if missing
        state.setdefault("execution_trace", [])
        state.setdefault("metadata_filters", {})
        state.setdefault("retrieved_chunks", [])
        state.setdefault("execution_plan", {})
        state.setdefault("search_limit", 3)
        state.setdefault("retrieval_strategy", "semantic")

        query = (
            state["rewritten_query"]
            or state["question"]
        )

        execution_plan = state["execution_plan"]

        limit = execution_plan.get(
            "retrieval_count",
            state["search_limit"],
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

        context = build_context(results)

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
        state["context"] = context

        state["execution_trace"].append(
            {
                "agent": "RetrieverAgent",
                "status": "completed",
                "chunks_retrieved": len(
                    retrieved_chunks
                ),
            }
        )

        logger.info(
            "RetrieverAgent completed - %d chunks retrieved",
            len(retrieved_chunks),
        )

        return state
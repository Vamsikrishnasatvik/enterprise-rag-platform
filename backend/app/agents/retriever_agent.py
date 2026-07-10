import logging

from app.agents.base import BaseAgent
from app.graph.state import GraphState

from app.services.retrieval_orchestrator import (
    retrieve_documents,
)

from app.services.context_compression_service import (
    compress_context,
)

logger = logging.getLogger(__name__)


class RetrieverAgent(BaseAgent):
    """
    Phase 4

    Retrieves relevant chunks using the strategy
    selected by the PlannerAgent.

    Supports:
    - Semantic Search
    - BM25 Search
    - Hybrid Search
    - Multi Query Search

    Automatically performs Context Compression.
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
        state.setdefault(
            "retrieval_strategy",
            "semantic",
        )
        state.setdefault(
            "retrieval_attempts",
            0,
        )

        query = (
            state.get("rewritten_query")
            or state["question"]
        )

        execution_plan = state["execution_plan"]

        limit = execution_plan.get(
            "retrieval_count",
            state["search_limit"],
        )

        # ----------------------------------------
        # Adaptive Retry
        # ----------------------------------------

        if state["retrieval_attempts"] >= 1:

            limit += (
                2
                * state["retrieval_attempts"]
            )

            logger.info(
                "Retry retrieval detected. "
                "Increasing limit to %d",
                limit,
            )

        strategy = execution_plan.get(
            "search_strategy",
            state["retrieval_strategy"],
        )

        logger.info(
            "Retriever query: %s",
            query,
        )

        logger.info(
            "Retrieval strategy: %s | limit: %d",
            strategy,
            limit,
        )

        # ----------------------------------------
        # Retrieve Documents
        # ----------------------------------------

        results = retrieve_documents(
            question=query,
            tenant_id=state["tenant_id"],
            limit=limit,
            strategy=strategy,
            metadata_filters=state[
                "metadata_filters"
            ],
        )

        retrieved_count = len(results)

        logger.info(
            "Retrieved %d chunks before compression",
            retrieved_count,
        )

        # ----------------------------------------
        # Context Compression
        # ----------------------------------------

        compressed_results = compress_context(
            chunks=results,
            max_chunks=limit,
        )

        compressed_count = len(
            compressed_results
        )

        logger.info(
            "Compressed context from %d to %d chunks",
            retrieved_count,
            compressed_count,
        )

        # ----------------------------------------
        # Store Results
        # ----------------------------------------

        state["retrieved_chunks"] = (
            compressed_results
        )

        # ----------------------------------------
        # Execution Trace
        # ----------------------------------------

        state["execution_trace"].append(
            {
                "agent": "RetrieverAgent",
                "status": "completed",
                "query": query,
                "strategy": strategy,
                "retrieval_attempt": state[
                    "retrieval_attempts"
                ],
                "search_limit": limit,
                "chunks_before_compression": retrieved_count,
                "chunks_after_compression": compressed_count,
            }
        )

        logger.info(
            "RetrieverAgent completed"
        )

        return state
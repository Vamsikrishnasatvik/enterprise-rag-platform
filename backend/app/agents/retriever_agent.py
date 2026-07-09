import logging

from app.agents.base import BaseAgent
from app.graph.state import GraphState

from app.services.retrieval_orchestrator import (
    retrieve_documents,
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

        results = retrieve_documents(
            question=query,
            tenant_id=state["tenant_id"],
            limit=limit,
            strategy=strategy,
            metadata_filters=state[
                "metadata_filters"
            ],
        )

        # Results are already normalized
        state["retrieved_chunks"] = results

        state["execution_trace"].append(
            {
                "agent": "RetrieverAgent",
                "status": "completed",
                "query": query,
                "chunks_retrieved": len(
                    results
                ),
                "retrieval_attempt": state[
                    "retrieval_attempts"
                ],
                "search_limit": limit,
                "strategy": strategy,
            }
        )

        logger.info(
            "RetrieverAgent completed - %d chunks retrieved",
            len(results),
        )

        return state
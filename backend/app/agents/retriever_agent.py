from app.agents.base import BaseAgent
from app.graph.state import GraphState

from app.services.context_service import build_context
from app.services.retrieval import HybridRetriever

import logging

logger = logging.getLogger(__name__)


class RetrieverAgent(BaseAgent):

    def __init__(self):
        super().__init__("RetrieverAgent")

    def run(self, state: GraphState) -> GraphState:

        retrieval_query = state.get(
            "retrieval_query",
            state["question"],
        )

        logger.info(
            "Retriever | retry=%d | strategy=%s | top_k=%d",
            state.get("retry_count", 0),
            state.get("retrieval_strategy", "semantic"),
            state.get("retrieval_limit", 3),
        )

        retriever = HybridRetriever()

        results = retriever.retrieve(
            query=retrieval_query,
            limit=state["retrieval_limit"],
            strategy=state.get(
                "retrieval_strategy",
                "semantic",
            ),
        )

        retrieval_context = build_context(results)

        state["retrieval_query"] = retrieval_query
        state["retrieved_chunks"] = results
        state["retrieval_context"] = retrieval_context

        unique_documents = {
            chunk.payload["document_id"]
            for chunk in results
        }

        state["retrieved_document_count"] = len(unique_documents)

        raw_score = max(
            (chunk.score for chunk in results),
            default=0.0,
        )

        logger.info(
            "Retriever raw score = %.4f",
            raw_score,
        )

        state["retrieval_score"] = raw_score

        state.setdefault(
            "execution_trace",
            [],
        ).append(
            {
                "agent": "RetrieverAgent",
                "query": retrieval_query,
                "strategy": state.get(
                    "retrieval_strategy",
                    "semantic",
                ),
                "retry": state.get("retry_count", 0),
                "top_k": state["retrieval_limit"],
                "chunks": len(results),
                "documents": state["retrieved_document_count"],
                "max_score": raw_score,
            }
        )

        return state
import logging

from app.agents.base import BaseAgent
from app.graph.state import GraphState

from app.services.context_service import build_context
from app.services.retrieval import HybridRetriever
from app.services.retrieval.dynamic_topk import DynamicTopKSelector

logger = logging.getLogger(__name__)


class RetrieverAgent(BaseAgent):
    """
    Retrieves enterprise knowledge using the configured retrieval strategy.

    Responsible for:
    - Dynamic Top-K selection
    - Document retrieval
    - Context construction
    - Retrieval statistics
    """

    def __init__(self):
        super().__init__("RetrieverAgent")
        self.retriever = HybridRetriever()
        self.selector = DynamicTopKSelector()

    def run(
        self,
        state: GraphState,
    ) -> GraphState:

        retrieval_query = (
            state.get("retrieval_query")
            or state.get("question", "")
        ).strip()

        if not retrieval_query:
            state.update(
                {
                    "retrieved_chunks": [],
                    "retrieval_context": "",
                    "retrieval_score": 0.0,
                    "retrieved_document_count": 0,
                    "reranker_score": None,
                }
            )
            return state

        retrieval_strategy = (
            state.get(
                "retrieval_strategy",
                "semantic",
            )
            .strip()
            .lower()
        )

        retry_count = state.get(
            "retry_count",
            0,
        )

        # ---------------------------------------------------------
        # Dynamic Top-K
        # ---------------------------------------------------------

        dynamic_top_k = self.selector.select(
            retrieval_query,
        )

        logger.info(
            "Retriever | retry=%d | strategy=%s | top_k=%d",
            retry_count,
            retrieval_strategy,
            dynamic_top_k,
        )

        # ---------------------------------------------------------
        # Retrieval
        # ---------------------------------------------------------

        results = self.retriever.retrieve(
            query=retrieval_query,
            limit=dynamic_top_k,
            strategy=retrieval_strategy,
        )

        retrieval_context = build_context(results)

        # ---------------------------------------------------------
        # Statistics
        # ---------------------------------------------------------

        unique_documents = {
            chunk.payload.get("document_id")
            for chunk in results
            if chunk.payload.get("document_id") is not None
        }

        semantic_score = max(
            (
                chunk.payload.get(
                    "semantic_score",
                    0.0,
                )
                for chunk in results
            ),
            default=0.0,
        )

        rerank_score = (
            results[0].payload.get(
                "rerank_score"
            )
            if results
            else None
        )

        state.update(
            {
                "retrieval_query": retrieval_query,
                "retrieval_limit": dynamic_top_k,
                "retrieved_chunks": results,
                "retrieval_context": retrieval_context,
                "retrieved_document_count": len(unique_documents),
                "retrieval_score": semantic_score,
                "reranker_score": rerank_score,
            }
        )

        logger.info(
            "Retriever | retrieved=%d chunks | documents=%d | semantic_score=%.4f | rerank_score=%s",
            len(results),
            len(unique_documents),
            semantic_score,
            (
                f"{rerank_score:.4f}"
                if rerank_score is not None
                else "None"
            ),
        )

        state.setdefault(
            "execution_trace",
            [],
        ).append(
            {
                "agent": self.name,
                "query": retrieval_query,
                "strategy": retrieval_strategy,
                "retry": retry_count,
                "top_k": dynamic_top_k,
                "chunks": len(results),
                "documents": len(unique_documents),
                "semantic_score": semantic_score,
                "rerank_score": rerank_score,
            }
        )

        return state
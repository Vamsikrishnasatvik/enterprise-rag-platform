import logging

from app.agents.base import BaseAgent
from app.graph.state import GraphState

from app.services.context_service import build_context
from app.services.retrieval import HybridRetriever
from app.services.retrieval.dynamic_topk import DynamicTopKSelector

logger = logging.getLogger(__name__)


class RetrieverAgent(BaseAgent):

    def __init__(self):
        super().__init__("RetrieverAgent")
        self.retriever = HybridRetriever()
        self.selector = DynamicTopKSelector()

    def run(
        self,
        state: GraphState,
    ) -> GraphState:

        # ---------------------------------------------------------
        # Retrieval Configuration
        # ---------------------------------------------------------

        retrieval_query = state.get(
            "retrieval_query",
            state["question"],
        )

        retrieval_strategy = state.get(
            "retrieval_strategy",
            "semantic",
        )

        retry_count = state.get(
            "retry_count",
            0,
        )

        # ---------------------------------------------------------
        # Dynamic Top-K Selection
        # ---------------------------------------------------------

        dynamic_top_k = self.selector.select(
            retrieval_query,
        )

        state["retrieval_limit"] = dynamic_top_k

        logger.info(
            "Retriever | retry=%d | strategy=%s | top_k=%d",
            retry_count,
            retrieval_strategy,
            dynamic_top_k,
        )

        # ---------------------------------------------------------
        # Retrieve Documents
        # ---------------------------------------------------------

        results = self.retriever.retrieve(
            query=retrieval_query,
            limit=dynamic_top_k,
            strategy=retrieval_strategy,
        )

        # ---------------------------------------------------------
        # Build Context
        # ---------------------------------------------------------

        retrieval_context = build_context(results)

        # ---------------------------------------------------------
        # Store Retrieval Results
        # ---------------------------------------------------------

        state["retrieval_query"] = retrieval_query
        state["retrieved_chunks"] = results
        state["retrieval_context"] = retrieval_context

        # ---------------------------------------------------------
        # Retrieval Statistics
        # ---------------------------------------------------------

        unique_documents = {
            chunk.payload["document_id"]
            for chunk in results
        }

        state["retrieved_document_count"] = len(
            unique_documents
        )

        raw_score = max(
            (chunk.score for chunk in results),
            default=0.0,
        )

        state["retrieval_score"] = raw_score

        logger.info(
            "Retriever | retrieved=%d chunks | documents=%d | max_score=%.4f",
            len(results),
            state["retrieved_document_count"],
            raw_score,
        )

        # ---------------------------------------------------------
        # Execution Trace
        # ---------------------------------------------------------

        state.setdefault(
            "execution_trace",
            [],
        ).append(
            {
                "agent": "RetrieverAgent",
                "query": retrieval_query,
                "strategy": retrieval_strategy,
                "retry": retry_count,
                "top_k": dynamic_top_k,
                "chunks": len(results),
                "documents": state["retrieved_document_count"],
                "max_score": raw_score,
            }
        )

        return state
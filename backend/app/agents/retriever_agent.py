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
    Phase 3.1

    Retrieves relevant chunks and builds context.
    """

    def run(
        self,
        state: GraphState,
    ) -> GraphState:

        logger.info("RetrieverAgent started")

        query = (
            state["rewritten_query"]
            or state["question"]
        )

        results = search_chunks(query)

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
                "chunks_retrieved": len(retrieved_chunks),
            }
        )

        logger.info(
            "RetrieverAgent completed - %d chunks retrieved",
            len(retrieved_chunks),
        )

        return state
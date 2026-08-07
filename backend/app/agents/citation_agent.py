import logging

from app.agents.base import BaseAgent
from app.graph.state import GraphState
from app.services.citation_service import add_citations

logger = logging.getLogger(__name__)


class CitationAgent(BaseAgent):
    """
    Adds inline citations to the generated answer and
    prepares citation metadata for the API response.
    """

    def __init__(self):
        super().__init__("CitationAgent")

    def run(self, state: GraphState) -> GraphState:
        """
        Build citation metadata from retrieved chunks and
        inject inline citations into the generated answer.
        """

        retrieved_chunks = state.get("retrieved_chunks", [])
        answer = state.get("answer", "")

        # ---------------------------------------------------------
        # Nothing to Cite
        # ---------------------------------------------------------

        if not retrieved_chunks or not answer:
            logger.info(
                "Citation skipped | chunks=%d | answer_present=%s",
                len(retrieved_chunks),
                bool(answer),
            )
            return state

        logger.info(
            "Adding citations | retrieved_chunks=%d",
            len(retrieved_chunks),
        )

        # ---------------------------------------------------------
        # Build Citation Metadata
        # ---------------------------------------------------------

        citations = []

        for index, chunk in enumerate(retrieved_chunks, start=1):

            payload = getattr(chunk, "payload", {})

            citations.append(
                {
                    "index": index,
                    "document_id": payload.get("document_id"),
                    "chunk_id": payload.get("chunk_id"),
                    "content": payload.get("content", ""),
                }
            )

        document_count = len(
            {
                citation["document_id"]
                for citation in citations
            }
        )

        # ---------------------------------------------------------
        # Add Inline Citations
        # ---------------------------------------------------------

        state.update(
            {
                "answer": add_citations(
                    answer=answer,
                    sources=citations,
                ),
                "citations": citations,
            }
        )

        logger.info(
            "Citation complete | citations=%d | documents=%d",
            len(citations),
            document_count,
        )

        # ---------------------------------------------------------
        # Execution Trace
        # ---------------------------------------------------------

        state.setdefault(
            "execution_trace",
            [],
        ).append(
            {
                "agent": self.name,
                "citations_added": len(citations),
                "documents": document_count,
            }
        )

        return state
from app.agents.base import BaseAgent
from app.graph.state import GraphState

from app.services.citation_service import add_citations


class CitationAgent(BaseAgent):

    def __init__(self):
        super().__init__("CitationAgent")

    def run(self, state: GraphState) -> GraphState:

        # ---------------------------------------------------------
        # Skip if no retrieved documents
        # ---------------------------------------------------------

        retrieved_chunks = state.get("retrieved_chunks", [])

        if not retrieved_chunks:
            return state

        # ---------------------------------------------------------
        # Build Citation Sources
        # ---------------------------------------------------------

        sources = []

        for i, chunk in enumerate(retrieved_chunks, start=1):

            payload = chunk.payload

            sources.append(
                {
                    "index": i,
                    "document_id": payload.get("document_id"),
                    "chunk_id": payload.get("chunk_id"),
                    "content": payload.get("content", ""),
                }
            )

        # ---------------------------------------------------------
        # Add Inline Citations
        # ---------------------------------------------------------

        state["answer"] = add_citations(
            answer=state["answer"],
            sources=sources,
        )

        state["citations"] = sources

        # ---------------------------------------------------------
        # Execution Trace
        # ---------------------------------------------------------

        state.setdefault(
            "execution_trace",
            [],
        ).append(
            {
                "agent": "CitationAgent",
                "citations_added": len(sources),
                "documents": len(
                    {
                        source["document_id"]
                        for source in sources
                    }
                ),
            }
        )

        return state
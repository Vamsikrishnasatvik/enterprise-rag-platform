from app.agents.base import BaseAgent
from app.graph.state import GraphState

from app.services.context_service import build_context
from app.services.retrieval_service import search_chunks


class RetrieverAgent(BaseAgent):

    def __init__(self):
        super().__init__("RetrieverAgent")

    def run(self, state: GraphState) -> GraphState:

        # ---------------------------------------------------------
        # Build Retrieval Query
        # ---------------------------------------------------------

        retrieval_query = self._build_retrieval_query(state)

        # ---------------------------------------------------------
        # Search Vector Store
        # ---------------------------------------------------------

        results = search_chunks(
            query=retrieval_query,
            limit=state["retrieval_limit"],
            strategy=state.get(
                "retrieval_strategy",
                "semantic",
            ),
        )

        # ---------------------------------------------------------
        # Build Retrieval Context
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

        state["retrieved_document_count"] = len(unique_documents)

        state["retrieval_score"] = max(
            (chunk.score for chunk in results),
            default=0.0,
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
                "strategy": state.get(
                    "retrieval_strategy",
                    "semantic",
                ),
                "top_k": state["retrieval_limit"],
                "chunks": len(results),
                "documents": state["retrieved_document_count"],
                "max_score": state["retrieval_score"],
            }
        )

        return state

    def _build_retrieval_query(
        self,
        state: GraphState,
    ) -> str:
        """
        Build a retrieval query using conversation memory
        and the current user question.
        """

        memory = (
            state.get("memory_context", "")
            .strip()
        )

        question = state["question"].strip()

        if not memory:
            return question

        return f"""
Conversation Context:

{memory}

Current Question:

{question}
""".strip()
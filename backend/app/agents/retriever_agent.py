from app.agents.base import BaseAgent
from app.graph.state import GraphState
from app.services.retrieval_service import search_chunks
from app.services.context_service import build_context


class RetrieverAgent(BaseAgent):
    def __init__(self):
        super().__init__("RetrieverAgent")

    def run(self, state: GraphState) -> GraphState:

        retrieval_query = self._build_retrieval_query(state)

        results = search_chunks(
            query=retrieval_query,
            limit=state["retrieval_limit"],
        )

        state["retrieval_query"] = retrieval_query
        state["retrieved_chunks"] = results
        state["compressed_context"] = build_context(results)

        return state

    def _build_retrieval_query(
        self,
        state: GraphState,
    ) -> str:
        """
        Build a retrieval query using conversation memory
        and the current user question.
        """

        memory = state.get(
            "memory_context",
            "",
        ).strip()

        question = state["question"]

        if not memory:
            return question

        return f"""
Conversation Context:

{memory}

Current Question:

{question}
""".strip()
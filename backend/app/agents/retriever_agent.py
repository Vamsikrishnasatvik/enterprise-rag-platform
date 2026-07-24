from app.agents.base import BaseAgent
from app.graph.state import GraphState
from app.services.retrieval_service import search_chunks
from app.services.context_service import build_context


class RetrieverAgent(BaseAgent):
    def __init__(self):
        super().__init__("RetrieverAgent")

    def run(self, state: GraphState) -> GraphState:
        results = search_chunks(
            query=state["question"],
            limit=state["retrieval_limit"],
        )

        state["retrieved_chunks"] = results
        state["compressed_context"] = build_context(results)

        return state
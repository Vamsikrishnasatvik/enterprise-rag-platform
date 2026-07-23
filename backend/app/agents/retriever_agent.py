from app.agents.base import BaseAgent
from app.graph.state import GraphState
from app.services.retrieval_service import search_chunks


class RetrieverAgent(BaseAgent):
    def __init__(self):
        super().__init__("RetrieverAgent")

    def run(self, state: GraphState) -> GraphState:
        question = state["question"]

        results = search_chunks(question)

        state["retrieved_chunks"] = results

        return state
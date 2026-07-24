from app.agents.base import BaseAgent
from app.graph.state import GraphState


class RetryAgent(BaseAgent):
    def __init__(self):
        super().__init__("RetryAgent")

    def run(self, state: GraphState) -> GraphState:
        state["retry_count"] += 1
        state["retrieval_limit"] += 5

        return state
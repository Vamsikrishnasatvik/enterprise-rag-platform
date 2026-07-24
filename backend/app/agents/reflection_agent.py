from app.agents.base import BaseAgent
from app.graph.state import GraphState


class ReflectionAgent(BaseAgent):
    def __init__(self):
        super().__init__("ReflectionAgent")

    def run(self, state: GraphState) -> GraphState:
        answer = state.get("answer", "")
        retrieved_chunks = state.get("retrieved_chunks", [])

        confidence = 1.0

        if len(answer) < 100:
            confidence -= 0.3

        if not retrieved_chunks:
            confidence -= 0.2

        confidence = max(confidence, 0.0)

        state["confidence_score"] = confidence

        state["needs_retry"] = confidence < 0.5

        state["reflection"] = {
            "answer_length": len(answer),
            "retrieved_chunks": len(retrieved_chunks),
            "confidence": confidence,
            "needs_retry": state["needs_retry"],
        }

        return state
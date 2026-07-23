from app.agents.base import BaseAgent
from app.graph.state import GraphState

from app.services.context_service import build_context
from app.services.llm_service import generate_answer


class AnswerAgent(BaseAgent):
    def __init__(self):
        super().__init__("AnswerAgent")

    def run(self, state: GraphState) -> GraphState:
        context = build_context(
            state["retrieved_chunks"]
        )

        answer = generate_answer(
            state["question"],
            context,
        )

        state["compressed_context"] = context
        state["answer"] = answer

        return state
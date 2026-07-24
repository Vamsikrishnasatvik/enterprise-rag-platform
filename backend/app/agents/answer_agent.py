from app.agents.base import BaseAgent
from app.graph.state import GraphState

from app.services.context_service import build_context
from app.services.llm_service import generate_answer


class AnswerAgent(BaseAgent):
    def __init__(self):
        super().__init__("AnswerAgent")

    def run(self, state: GraphState) -> GraphState:
        retrieved_chunks = state.get("retrieved_chunks", [])

        if retrieved_chunks:
            context = build_context(retrieved_chunks)
        else:
            context = ""

        answer = generate_answer(
            question=state["question"],
            context=context,
            memory_context=state.get(
                "memory_context",
                "",
            ),
        )

        state["compressed_context"] = context
        state["answer"] = answer

        return state
from app.agents.base import BaseAgent
from app.graph.state import GraphState

from app.services.llm_service import (
    generate_answer,
)


class AnswerAgent(BaseAgent):
    async def run(
        self,
        state: GraphState,
    ) -> GraphState:

        state["execution_trace"].append(
            "AnswerAgent"
        )

        answer = generate_answer(
            question=state["question"],
            context=state["context"],
        )

        state["answer"] = answer

        return state
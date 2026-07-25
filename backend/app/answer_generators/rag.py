from app.answer_generators.base import BaseAnswerGenerator
from app.graph.state import GraphState

from app.services.llm_service import generate_answer


class RAGAnswerGenerator(BaseAnswerGenerator):
    """
    Generate answers using enterprise knowledge.
    """

    def generate(
        self,
        state: GraphState,
    ) -> str:

        return generate_answer(
            question=state["question"],
            context=state.get(
                "retrieval_context",
                "",
            ),
            memory_context=state.get(
                "memory_context",
                "",
            ),
        )
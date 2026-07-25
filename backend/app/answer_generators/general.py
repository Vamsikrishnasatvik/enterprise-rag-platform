from app.answer_generators.base import BaseAnswerGenerator
from app.graph.state import GraphState

from app.services.llm_service import generate_general_answer


class GeneralAnswerGenerator(BaseAnswerGenerator):
    """
    Generates answers that do not require enterprise retrieval.
    Examples:
    - Greetings
    - Chit-chat
    - General reasoning
    """

    def generate(
        self,
        state: GraphState,
    ) -> str:

        return generate_general_answer(
            question=state["question"],
            memory_context=state.get(
                "memory_context",
                "",
            ),
        )
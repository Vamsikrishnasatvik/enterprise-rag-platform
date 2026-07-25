from app.answer_generators.general import GeneralAnswerGenerator
from app.answer_generators.rag import RAGAnswerGenerator


class AnswerFactory:
    """
    Factory responsible for selecting the appropriate
    answer generation strategy based on the planner's
    query classification.
    """

    @staticmethod
    def get(query_type: str):

        # ---------------------------------------------------------
        # Conversational Queries
        # ---------------------------------------------------------

        if query_type in {
            "greeting",
            "chit_chat",
        }:
            return GeneralAnswerGenerator()

        # ---------------------------------------------------------
        # Enterprise Knowledge Queries
        # ---------------------------------------------------------

        if query_type in {
            "knowledge",
            "follow_up",
            "reasoning",
        }:
            return RAGAnswerGenerator()

        # ---------------------------------------------------------
        # Future Tool Calling
        # ---------------------------------------------------------

        # if query_type == "tool":
        #     return ToolAnswerGenerator()

        # ---------------------------------------------------------
        # Default Strategy
        # ---------------------------------------------------------

        return GeneralAnswerGenerator()
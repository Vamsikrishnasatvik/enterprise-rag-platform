from app.agents.base import BaseAgent
from app.answer_generators.factory import AnswerFactory
from app.graph.state import GraphState


class AnswerAgent(BaseAgent):

    def __init__(self):
        super().__init__("AnswerAgent")

    def run(self, state: GraphState) -> GraphState:

        # ---------------------------------------------------------
        # Select Answer Generation Strategy
        # ---------------------------------------------------------

        query_type = state.get(
            "query_type",
            "knowledge",
        )

        generator = AnswerFactory.get(query_type)

        # ---------------------------------------------------------
        # Generate Answer
        # ---------------------------------------------------------

        state["answer"] = generator.generate(state)

        # ---------------------------------------------------------
        # Execution Trace
        # ---------------------------------------------------------

        state.setdefault(
            "execution_trace",
            [],
        ).append(
            {
                "agent": "AnswerAgent",
                "query_type": state.get("query_type"),
                "strategy": generator.__class__.__name__,
            }
        )

        return state
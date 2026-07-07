from app.agents.base import BaseAgent
from app.graph.state import GraphState


class QueryAgent(BaseAgent):
    """
    Phase 3.1

    Initial Query Agent.

    Future responsibilities:
    - Intent Detection
    - Query Rewriting
    - Entity Extraction
    - Metadata Extraction
    """

    async def run(
        self,
        state: GraphState,
    ) -> GraphState:

        state["execution_trace"].append(
            "QueryAgent"
        )

        # No processing in v3.1
        state["rewritten_query"] = state["question"]

        return state
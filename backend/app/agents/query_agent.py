import logging

from app.agents.base import BaseAgent
from app.graph.state import GraphState

logger = logging.getLogger(__name__)


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

    def run(
        self,
        state: GraphState,
    ) -> GraphState:

        logger.info("QueryAgent started")

        state["execution_trace"].append(
            {
                "agent": "QueryAgent",
                "status": "completed",
            }
        )

        state["rewritten_query"] = state["question"]

        logger.info("QueryAgent completed")

        return state
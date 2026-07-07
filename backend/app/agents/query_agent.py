import logging

from app.agents.base import BaseAgent
from app.graph.state import GraphState

from app.services.query_understanding_service import (
    understand_query,
)

logger = logging.getLogger(__name__)


class QueryAgent(BaseAgent):

    def run(
        self,
        state: GraphState,
    ) -> GraphState:

        logger.info("QueryAgent started")

        # Initialize runtime state if missing
        state.setdefault("execution_trace", [])
        state.setdefault("metadata_filters", {})
        state.setdefault("entities", [])

        result = understand_query(
            state["question"]
        )

        state["intent"] = result.intent

        state["rewritten_query"] = (
            result.rewritten_query
        )

        state["entities"] = [
            entity.model_dump()
            for entity in result.entities
        ]

        state["metadata_filters"] = (
            result.metadata_filters
        )

        # Retrieval configuration
        state["search_limit"] = 3

        state["use_metadata_filters"] = bool(
            result.metadata_filters
        )

        state["retrieval_strategy"] = (
            "semantic"
        )

        state["execution_trace"].append(
            {
                "agent": "QueryAgent",
                "status": "completed",
            }
        )

        logger.info("QueryAgent completed")

        return state
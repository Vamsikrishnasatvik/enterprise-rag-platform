import logging

from app.agents.base import BaseAgent
from app.graph.state import GraphState

from app.services.planning_service import (
    create_execution_plan,
)

logger = logging.getLogger(__name__)


class PlannerAgent(BaseAgent):

    def run(
        self,
        state: GraphState,
    ) -> GraphState:

        logger.info("PlannerAgent started")

        # Initialize runtime state if missing
        state.setdefault("execution_trace", [])
        state.setdefault("execution_plan", {})
        state.setdefault("metadata_filters", {})

        plan = create_execution_plan(
            question=state["question"],
            intent=state["intent"],
            metadata_filters=state["metadata_filters"],
        )

        state["execution_plan"] = plan.model_dump()

        state["search_limit"] = plan.retrieval_count

        state["use_metadata_filters"] = (
            plan.use_metadata_filters
        )

        state["retrieval_strategy"] = (
            plan.search_strategy
        )

        state["execution_trace"].append(
            {
                "agent": "PlannerAgent",
                "status": "completed",
            }
        )

        logger.info("PlannerAgent completed")

        return state
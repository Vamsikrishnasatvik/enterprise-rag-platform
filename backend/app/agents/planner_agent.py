import logging

from app.agents.base import BaseAgent
from app.graph.state import GraphState

from app.services.planning_service import (
    create_execution_plan,
)
from app.services.planner_rules import (
    apply_planner_rules,
)

logger = logging.getLogger(__name__)


class PlannerAgent(BaseAgent):
    """
    Phase 3

    Creates the execution plan for retrieval.
    """

    def run(
        self,
        state: GraphState,
    ) -> GraphState:

        logger.info("PlannerAgent started")

        state.setdefault("execution_trace", [])

        query = (
            state["rewritten_query"]
            or state["question"]
        )

        plan = create_execution_plan(
            question=query,
            intent=state.get("intent"),
            metadata_filters=state.get(
                "metadata_filters"
            ),
            conversation_summary=state.get(
                "conversation_summary"
            ),
        )

        plan = apply_planner_rules(
            plan=plan,
            question=query,
            history_length=len(
                state.get(
                    "chat_history",
                    [],
                )
            ),
        )

        # Store the complete execution plan
        state["execution_plan"] = (
            plan.model_dump()
        )

        # Update graph state from planner decisions
        state["intent"] = plan.intent

        state["search_limit"] = (
            plan.retrieval_count
        )

        state["use_metadata_filters"] = (
            plan.use_metadata_filters
        )

        state["metadata_filters"] = (
            plan.metadata_filters
        )

        state["retrieval_strategy"] = (
            plan.search_strategy
        )

        logger.info(
            "Planner using query: %s",
            query,
        )

        logger.info(
            "Execution Plan: %s",
            plan.model_dump(),
        )

        state["execution_trace"].append(
            {
                "agent": "PlannerAgent",
                "status": "completed",
                "query": query,
                "plan": plan.model_dump(),
            }
        )

        logger.info(
            "PlannerAgent completed"
        )

        return state
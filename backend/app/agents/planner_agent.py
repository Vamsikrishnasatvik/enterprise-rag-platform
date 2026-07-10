import logging

from app.agents.base import BaseAgent
from app.graph.state import GraphState

from app.services.planning_service import (
    create_execution_plan,
)
from app.services.planner_rules import (
    apply_planner_rules,
)
from app.services.self_query_service import (
    generate_self_query,
)

logger = logging.getLogger(__name__)


class PlannerAgent(BaseAgent):
    """
    Planner Agent

    Responsible for creating the execution plan
    used by the retrieval pipeline.
    """

    def run(
        self,
        state: GraphState,
    ) -> GraphState:

        logger.info("PlannerAgent started")

        state.setdefault(
            "execution_trace",
            [],
        )

        # --------------------------------------------------
        # Start with rewritten query if available
        # --------------------------------------------------

        query = (
            state.get("rewritten_query")
            or state["question"]
        )

        # --------------------------------------------------
        # Self Query Retrieval
        # --------------------------------------------------

        self_query = generate_self_query(
            question=query,
        )

        query = self_query.get(
            "query",
            query,
        )

        state.setdefault(
            "metadata_filters",
            {},
        )

        state["metadata_filters"].update(
            self_query.get(
                "metadata_filters",
                {},
            )
        )

        logger.info(
            "Self Query Result: %s",
            self_query,
        )

        # --------------------------------------------------
        # Create execution plan
        # --------------------------------------------------

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

        # --------------------------------------------------
        # Apply deterministic planner rules
        # --------------------------------------------------

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

        # --------------------------------------------------
        # Store execution plan
        # --------------------------------------------------

        state["execution_plan"] = (
            plan.model_dump()
        )

        # --------------------------------------------------
        # Update graph state
        # --------------------------------------------------

        state["intent"] = plan.intent

        state["search_limit"] = (
            plan.retrieval_count
        )

        state["use_metadata_filters"] = (
            plan.use_metadata_filters
        )

        # Merge planner filters with self-query filters
        planner_filters = (
            plan.metadata_filters or {}
        )

        state["metadata_filters"].update(
            planner_filters
        )

        state["retrieval_strategy"] = (
            plan.search_strategy
        )

        # --------------------------------------------------
        # Logging
        # --------------------------------------------------

        logger.info(
            "Planner using query: %s",
            query,
        )

        logger.info(
            "Execution Plan: %s",
            plan.model_dump(),
        )

        # --------------------------------------------------
        # Execution trace
        # --------------------------------------------------

        state["execution_trace"].append(
            {
                "agent": "PlannerAgent",
                "status": "completed",
                "query": query,
                "self_query": self_query,
                "plan": plan.model_dump(),
            }
        )

        logger.info(
            "PlannerAgent completed"
        )

        return state
from app.agents.base import BaseAgent
from app.graph.state import GraphState
from app.services.planner_service import create_execution_plan


class PlannerAgent(BaseAgent):

    def __init__(self):
        super().__init__("PlannerAgent")

    def run(self, state: GraphState) -> GraphState:

        plan = create_execution_plan(
            question=state["question"],
            memory_context=state.get(
                "memory_context",
                "",
            ),
        )

        # ---------------------------------------------------------
        # Store Planner Output
        # ---------------------------------------------------------

        state["query_type"] = plan.get(
            "query_type",
            "knowledge",
        )

        execution_plan = plan.get(
            "execution_plan",
            {
                "route": "retriever",
                "reflect": True,
                "verify": False,
            },
        )

        state["execution_plan"] = execution_plan

        state["planning_reason"] = plan.get(
            "reason",
            "",
        )

        # ---------------------------------------------------------
        # Execution Trace
        # ---------------------------------------------------------

        state.setdefault(
            "execution_trace",
            [],
        ).append(
            {
                "agent": "PlannerAgent",
                "query_type": state["query_type"],
                "route": execution_plan.get(
                    "route",
                    "retriever",
                ),
            }
        )

        return state
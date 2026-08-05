from app.agents.base import BaseAgent
from app.graph.state import GraphState


class SupervisorAgent(BaseAgent):
    """
    Validates the execution plan produced by the PlannerAgent.

    The Supervisor no longer performs routing.
    It simply ensures that a valid execution plan exists and
    records metadata for downstream agents.
    """

    DEFAULT_PLAN = [
        {
            "tool": "rag",
            "inputs": {},
        }
    ]

    def __init__(self):
        super().__init__("SupervisorAgent")

    def run(
        self,
        state: GraphState,
    ) -> GraphState:

        execution_plan = state.get(
            "execution_plan",
            self.DEFAULT_PLAN,
        )

        # ---------------------------------------------------------
        # Validate Execution Plan
        # ---------------------------------------------------------

        if (
            not isinstance(execution_plan, list)
            or len(execution_plan) == 0
        ):
            execution_plan = self.DEFAULT_PLAN.copy()

        normalized_plan = []

        for step in execution_plan:

            if not isinstance(step, dict):
                continue

            normalized_plan.append(
                {
                    "tool": step.get(
                        "tool",
                        "rag",
                    ),
                    "inputs": step.get(
                        "inputs",
                        {},
                    ),
                }
            )

        if not normalized_plan:
            normalized_plan = self.DEFAULT_PLAN.copy()

        state["execution_plan"] = normalized_plan

        # ---------------------------------------------------------
        # Metadata
        # ---------------------------------------------------------

        state["tool_count"] = len(normalized_plan)

        state["routing_reason"] = state.get(
            "planning_reason",
            "Planner execution plan validated.",
        )

        # ---------------------------------------------------------
        # Execution Trace
        # ---------------------------------------------------------

        state.setdefault(
            "execution_trace",
            [],
        ).append(
            {
                "agent": "SupervisorAgent",
                "tools": [
                    step["tool"]
                    for step in normalized_plan
                ],
                "count": len(normalized_plan),
                "reason": state["routing_reason"],
            }
        )

        return state
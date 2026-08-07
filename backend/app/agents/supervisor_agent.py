from app.agents.base import BaseAgent
from app.graph.state import GraphState


class SupervisorAgent(BaseAgent):
    """
    Validates and normalizes the execution plan produced by the PlannerAgent.

    The Supervisor no longer performs routing. Its responsibility is to
    ensure a valid execution plan exists and expose metadata required by
    downstream agents.
    """

    DEFAULT_PLAN = (
        {
            "tool": "rag",
            "inputs": {},
        },
    )

    def __init__(self):
        super().__init__("SupervisorAgent")

    def run(
        self,
        state: GraphState,
    ) -> GraphState:

        execution_plan = state.get(
            "execution_plan",
            [dict(step) for step in self.DEFAULT_PLAN],
        )

        if (
            not isinstance(execution_plan, list)
            or not execution_plan
        ):
            execution_plan = [
                dict(step)
                for step in self.DEFAULT_PLAN
            ]

        normalized_plan = []

        for step in execution_plan:

            if not isinstance(step, dict):
                continue

            normalized_plan.append(
                {
                    "tool": str(
                        step.get(
                            "tool",
                            "rag",
                        )
                    ).strip().lower(),
                    "inputs": step.get(
                        "inputs",
                        {},
                    ),
                }
            )

        if not normalized_plan:
            normalized_plan = [
                dict(step)
                for step in self.DEFAULT_PLAN
            ]

        state.update(
            {
                "execution_plan": normalized_plan,
                "tool_count": len(normalized_plan),
                "routing_reason": state.get(
                    "planning_reason",
                    "Planner execution plan validated.",
                ),
            }
        )

        state.setdefault(
            "execution_trace",
            [],
        ).append(
            {
                "agent": self.name,
                "tools": [
                    step["tool"]
                    for step in normalized_plan
                ],
                "count": len(normalized_plan),
                "reason": state["routing_reason"],
            }
        )

        return state
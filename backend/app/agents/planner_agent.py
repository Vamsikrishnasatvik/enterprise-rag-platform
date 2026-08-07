from app.agents.base import BaseAgent
from app.graph.state import GraphState
from app.services.planner_service import create_execution_plan


DEFAULT_EXECUTION_PLAN = [
    {
        "tool": "rag",
        "inputs": {},
    }
]


class PlannerAgent(BaseAgent):
    """
    Generates an execution plan for the user's request.
    """

    def __init__(self):
        super().__init__("PlannerAgent")

    def run(
        self,
        state: GraphState,
    ) -> GraphState:

        plan = create_execution_plan(
            question=state.get("question", ""),
            memory_context=state.get(
                "memory_context",
                "",
            ),
        )

        query_type = plan.get(
            "query_type",
            "knowledge",
        )

        execution_plan = plan.get(
            "execution_plan",
            DEFAULT_EXECUTION_PLAN.copy(),
        )

        if isinstance(execution_plan, dict):
            execution_plan = DEFAULT_EXECUTION_PLAN.copy()

        normalized_plan = []

        for step in execution_plan:

            if not isinstance(step, dict):
                continue

            normalized_plan.append(
                {
                    "tool": step.get("tool", "rag"),
                    "inputs": step.get("inputs", {}),
                }
            )

        if not normalized_plan:
            normalized_plan = DEFAULT_EXECUTION_PLAN.copy()

        state.update(
            {
                "query_type": query_type,
                "execution_plan": normalized_plan,
                "tool_name": normalized_plan[0]["tool"],  # Backward compatibility
                "planning_reason": plan.get("reason", ""),
            }
        )

        state.setdefault(
            "execution_trace",
            [],
        ).append(
            {
                "agent": self.name,
                "query_type": query_type,
                "steps": len(normalized_plan),
                "tools": [
                    step["tool"]
                    for step in normalized_plan
                ],
                "reason": state["planning_reason"],
            }
        )

        return state
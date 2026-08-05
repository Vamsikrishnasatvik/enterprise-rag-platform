from app.agents.base import BaseAgent
from app.graph.state import GraphState
from app.services.planner_service import create_execution_plan


class PlannerAgent(BaseAgent):

    def __init__(self):
        super().__init__("PlannerAgent")

    def run(
        self,
        state: GraphState,
    ) -> GraphState:

        plan = create_execution_plan(
            question=state["question"],
            memory_context=state.get(
                "memory_context",
                "",
            ),
        )

        # ---------------------------------------------------------
        # Query Type
        # ---------------------------------------------------------

        state["query_type"] = plan.get(
            "query_type",
            "knowledge",
        )

        # ---------------------------------------------------------
        # Execution Plan
        # ---------------------------------------------------------

        execution_plan = plan.get(
            "execution_plan",
            [
                {
                    "tool": "rag",
                    "inputs": {},
                }
            ],
        )

        # ---------------------------------------------------------
        # Backward Compatibility
        # ---------------------------------------------------------

        if isinstance(execution_plan, dict):
            execution_plan = [
                {
                    "tool": "rag",
                    "inputs": {},
                }
            ]

        # ---------------------------------------------------------
        # Validate Execution Plan
        # ---------------------------------------------------------

        normalized_plan = []

        for step in execution_plan:

            tool = step.get(
                "tool",
                "rag",
            )

            inputs = step.get(
                "inputs",
                {},
            )

            normalized_plan.append(
                {
                    "tool": tool,
                    "inputs": inputs,
                }
            )

        execution_plan = normalized_plan

        state["execution_plan"] = execution_plan

        # Backward compatibility for components
        # that still read tool_name.
        state["tool_name"] = execution_plan[0]["tool"]

        # ---------------------------------------------------------
        # Planning Reason
        # ---------------------------------------------------------

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
                "steps": len(execution_plan),
                "tools": [
                    step["tool"]
                    for step in execution_plan
                ],
                "reason": state["planning_reason"],
            }
        )

        return state
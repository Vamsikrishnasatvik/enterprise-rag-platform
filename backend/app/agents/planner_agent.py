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

        state["execution_plan"] = plan["execution_plan"]
        state["query_type"] = plan["query_type"]
        state["planning_reason"] = plan["reason"]

        return state
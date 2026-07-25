from app.agents.base import BaseAgent
from app.graph.state import GraphState


class SupervisorAgent(BaseAgent):

    def __init__(self):
        super().__init__("SupervisorAgent")

    def run(self, state: GraphState) -> GraphState:

        execution_plan = state.get("execution_plan", {})

        # ---------------------------------------------------------
        # Planner decides the execution route
        # ---------------------------------------------------------

        route = execution_plan.get(
            "route",
            "retriever",
        )

        # Safety fallback
        if route not in {
            "answer",
            "retriever",
            "tool",
        }:
            route = "retriever"

        state["next_node"] = route

        # ---------------------------------------------------------
        # Optional execution flags
        # ---------------------------------------------------------

        state["needs_retrieval"] = (
            route == "retriever"
        )

        state["needs_verification"] = execution_plan.get(
            "verify",
            False,
        )

        # ---------------------------------------------------------
        # Logging / Monitoring
        # ---------------------------------------------------------

        state["routing_reason"] = state.get(
            "planning_reason",
            "",
        )

        state.setdefault(
            "execution_trace",
            [],
        ).append(
            {
                "agent": "SupervisorAgent",
                "route": route,
                "reason": state["routing_reason"],
            }
        )

        return state
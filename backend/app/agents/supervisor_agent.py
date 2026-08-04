from app.agents.base import BaseAgent
from app.graph.state import GraphState


class SupervisorAgent(BaseAgent):
    """
    Executes the workflow plan produced by the PlannerAgent.

    The Supervisor does not make decisions itself.
    It simply validates and applies the planner's execution plan.
    """

    VALID_ROUTES = {
        "answer",
        "retriever",
        "tool",
    }

    def __init__(self):
        super().__init__("SupervisorAgent")

    def run(self, state: GraphState) -> GraphState:

        execution_plan = state.get("execution_plan", {})

        # ---------------------------------------------------------
        # Execute planner decision
        # ---------------------------------------------------------

        route = execution_plan.get("route", "retriever")

        if route not in self.VALID_ROUTES:
            route = "retriever"

        state["next_node"] = route

        # ---------------------------------------------------------
        # Execution Flags
        # ---------------------------------------------------------

        state["needs_retrieval"] = route == "retriever"

        state["needs_verification"] = execution_plan.get(
            "verify",
            False,
        )

        state["needs_reflection"] = execution_plan.get(
            "reflect",
            False,
        )

        # ---------------------------------------------------------
        # Trace
        # ---------------------------------------------------------

        state["routing_reason"] = state.get(
            "planning_reason",
            "Planner decision executed.",
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
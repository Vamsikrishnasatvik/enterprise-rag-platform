from app.agents.base import BaseAgent
from app.graph.state import GraphState


class SupervisorAgent(BaseAgent):

    def __init__(self):
        super().__init__("SupervisorAgent")

    def run(self, state: GraphState) -> GraphState:
        """
        Entry point for the agent workflow.

        For now, simply initialize the execution plan.
        """

        state["execution_plan"] = {
            "retrieve": True,
            "reflect": False,
            "verify": False,
        }

        return state
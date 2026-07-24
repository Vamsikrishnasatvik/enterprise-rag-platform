from app.agents.base import BaseAgent
from app.graph.state import GraphState


class SupervisorAgent(BaseAgent):
    def __init__(self):
        super().__init__("SupervisorAgent")

    def run(self, state: GraphState) -> GraphState:
        plan = state["execution_plan"]

        state["needs_retrieval"] = plan["retrieve"]
        state["needs_verification"] = plan["verify"]

        if plan["retrieve"]:
            state["next_node"] = "retriever"
        else:
            state["next_node"] = "answer"

        state["routing_reason"] = state["planning_reason"]

        return state
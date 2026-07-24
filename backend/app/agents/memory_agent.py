from app.agents.base import BaseAgent
from app.graph.state import GraphState
from app.services.memory_service import memory_service


class MemoryAgent(BaseAgent):
    """
    Loads conversation memory and prepares
    memory context for downstream agents.
    """

    def __init__(self):
        super().__init__("MemoryAgent")

    def run(self, state: GraphState) -> GraphState:

        conversation_id = state.get("conversation_id")
        db = state.get("db")

        if not conversation_id:
            state["conversation_summary"] = ""
            state["recent_messages"] = []
            state["conversation_history"] = []
            state["memory_context"] = ""
            return state

        memory = memory_service.get_memory_context(
            db=db,
            conversation_id=conversation_id,
        )

        state["conversation_summary"] = memory["conversation_summary"]
        state["recent_messages"] = memory["recent_messages"]
        state["conversation_history"] = memory["conversation_history"]   # Temporary
        state["memory_context"] = memory["memory_context"]

        return state
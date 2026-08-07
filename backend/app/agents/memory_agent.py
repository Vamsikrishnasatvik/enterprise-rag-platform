from app.agents.base import BaseAgent
from app.graph.state import GraphState
from app.services.memory_service import memory_service


class MemoryAgent(BaseAgent):
    """
    Loads conversation memory and prepares the
    memory context for downstream agents.
    """

    def __init__(self):
        super().__init__("MemoryAgent")

    def run(self, state: GraphState) -> GraphState:

        conversation_id = state.get("conversation_id")
        db = state.get("db")

        if not conversation_id or db is None:
            state.update(
                {
                    "conversation_summary": "",
                    "recent_messages": [],
                    "conversation_history": [],
                    "memory_context": "",
                }
            )
            return state

        memory: dict = memory_service.get_memory_context(
            db=db,
            conversation_id=conversation_id,
            question=state.get("question", ""),
        )

        state.update(
            {
                "conversation_summary": memory.get(
                    "conversation_summary",
                    "",
                ),
                "recent_messages": memory.get(
                    "recent_messages",
                    [],
                ),
                "conversation_history": memory.get(
                    "conversation_history",
                    [],
                ),
                "memory_context": memory.get(
                    "memory_context",
                    "",
                ),
            }
        )

        return state
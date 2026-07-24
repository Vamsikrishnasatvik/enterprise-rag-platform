from app.agents.base import BaseAgent
from app.graph.state import GraphState
from app.services.verification_service import verify_answer


class VerificationAgent(BaseAgent):
    def __init__(self):
        super().__init__("VerificationAgent")

    def run(
        self,
        state: GraphState,
    ) -> GraphState:

        verification = verify_answer(
            question=state["question"],
            context=state["compressed_context"],
            answer=state["answer"],
        )

        state["verification"] = {
            "verified": False,
            "reason": "Testing retry loop"
        }

        state["verification_passed"] = False
        state["verification_reason"] = "Testing retry loop"

        if state["retry_count"] < state["max_retries"]:
            state["retry_required"] = True
        else:
            state["retry_required"] = False

        return state
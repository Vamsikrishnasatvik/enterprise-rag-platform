from app.agents.base import BaseAgent
from app.graph.state import GraphState


class RetryAgent(BaseAgent):

    def __init__(self):
        super().__init__("RetryAgent")

    def run(self, state: GraphState) -> GraphState:

        # ---------------------------------------------------------
        # Increment Retry Count
        # ---------------------------------------------------------

        retry_count = state.get("retry_count", 0) + 1
        state["retry_count"] = retry_count

        # ---------------------------------------------------------
        # Progressive Retrieval Strategy
        # ---------------------------------------------------------

        if retry_count == 1:

            state["retrieval_limit"] = 5
            state["retrieval_strategy"] = "semantic"

        elif retry_count == 2:

            state["retrieval_limit"] = 8
            state["retrieval_strategy"] = "hybrid"

        else:

            state["retrieval_limit"] = 10
            state["retrieval_strategy"] = "keyword"

        # ---------------------------------------------------------
        # Rebuild Retrieval Query
        # ---------------------------------------------------------

        state["retrieval_query"] = state["question"]

        # ---------------------------------------------------------
        # Clear Previous Results
        # ---------------------------------------------------------

        state["retrieved_chunks"] = []
        state["retrieval_context"] = ""
        state["answer"] = ""
        state["reflection"] = {}
        state["verification"] = {}

        # ---------------------------------------------------------
        # Execution Trace
        # ---------------------------------------------------------

        state.setdefault(
            "execution_trace",
            [],
        ).append(
            {
                "agent": "RetryAgent",
                "retry": retry_count,
                "strategy": state["retrieval_strategy"],
                "top_k": state["retrieval_limit"],
                "reason": state.get(
                    "retry_reason",
                    "Low confidence answer.",
                ),
            }
        )

        return state
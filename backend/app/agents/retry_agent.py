from app.agents.base import BaseAgent
from app.graph.state import GraphState


class RetryAgent(BaseAgent):

    def __init__(self):
        super().__init__("RetryAgent")

    def run(
        self,
        state: GraphState,
    ) -> GraphState:

        # ---------------------------------------------------------
        # Increment Retry Count
        # ---------------------------------------------------------

        retry_count = state.get(
            "retry_count",
            0,
        ) + 1

        state["retry_count"] = retry_count

        # ---------------------------------------------------------
        # Reset Retry Flags
        # Prevent stale retry state from causing infinite loops
        # ---------------------------------------------------------

        state["needs_retry"] = False
        state["retry_required"] = False
        state["retry_reason"] = ""

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
        # Reset Retrieval Query
        # QueryRewriterAgent will improve it again
        # ---------------------------------------------------------

        state["retrieval_query"] = state["question"]

        # ---------------------------------------------------------
        # Clear Previous Results
        # ---------------------------------------------------------

        state["retrieved_chunks"] = []
        state["retrieval_context"] = ""

        state["answer"] = ""
        state["citations"] = []

        state["reflection"] = {}
        state["verification"] = {}

        state["confidence_score"] = 0.0
        state["retrieval_score"] = 0.0
        state["retrieved_document_count"] = 0

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
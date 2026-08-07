import logging

from app.agents.base import BaseAgent
from app.graph.state import GraphState

logger = logging.getLogger(__name__)

# =============================================================================
# Retry Configuration
# =============================================================================

FIRST_RETRY_TOP_K = 5
SECOND_RETRY_TOP_K = 8
FINAL_RETRY_TOP_K = 10


class RetryAgent(BaseAgent):
    """
    Prepares the workflow for another retrieval attempt by
    resetting transient state and progressively expanding
    the retrieval strategy.
    """

    def __init__(self):
        super().__init__("RetryAgent")

    def run(
        self,
        state: GraphState,
    ) -> GraphState:
        """
        Reset workflow state and configure the next retry.
        """

        # ---------------------------------------------------------
        # Increment Retry Counter
        # ---------------------------------------------------------

        retry_count = state.get(
            "retry_count",
            0,
        ) + 1

        retry_reason = state.get(
            "retry_reason",
            "Low confidence answer.",
        )

        # ---------------------------------------------------------
        # Progressive Retrieval Strategy
        # ---------------------------------------------------------

        if retry_count == 1:

            retrieval_limit = FIRST_RETRY_TOP_K
            retrieval_strategy = "semantic"

        elif retry_count == 2:

            retrieval_limit = SECOND_RETRY_TOP_K
            retrieval_strategy = "hybrid"

        else:

            retrieval_limit = FINAL_RETRY_TOP_K
            retrieval_strategy = "keyword"

        logger.info(
            "Retry #%d | strategy=%s | top_k=%d",
            retry_count,
            retrieval_strategy,
            retrieval_limit,
        )

        # ---------------------------------------------------------
        # Reset Workflow State
        # ---------------------------------------------------------

        state.update(
            {
                "retry_count": retry_count,
                "needs_retry": False,
                "retry_required": False,
                "retry_reason": "",
                "retrieval_limit": retrieval_limit,
                "retrieval_strategy": retrieval_strategy,
                "retrieval_query": state["question"],
                "retrieved_chunks": [],
                "retrieval_context": "",
                "answer": "",
                "citations": [],
                "reflection": {},
                "verification": {},
                "confidence_score": 0.0,
                "retrieval_score": 0.0,
                "retrieved_document_count": 0,
            }
        )

        # ---------------------------------------------------------
        # Execution Trace
        # ---------------------------------------------------------

        state.setdefault(
            "execution_trace",
            [],
        ).append(
            {
                "agent": self.name,
                "retry": retry_count,
                "strategy": retrieval_strategy,
                "top_k": retrieval_limit,
                "reason": retry_reason,
            }
        )

        return state
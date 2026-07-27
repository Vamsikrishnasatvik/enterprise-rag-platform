import logging

logger = logging.getLogger(__name__)


class DynamicTopKSelector:
    """
    Selects the number of chunks to retrieve based on
    query complexity.

    Phase 6.1.3:
        - Rule-based heuristic

    Future:
        - Planner-guided Top-K
        - Confidence-based adaptation
        - Token-budget optimization
    """

    def select(self, question: str) -> int:
        """
        Determine the optimal retrieval depth.
        """

        words = len(question.split())

        # ---------------------------------------------------------
        # Very Simple Question
        # ---------------------------------------------------------

        if words <= 5:
            top_k = 2

        # ---------------------------------------------------------
        # Medium Question
        # ---------------------------------------------------------

        elif words <= 12:
            top_k = 4

        # ---------------------------------------------------------
        # Complex Question
        # ---------------------------------------------------------

        else:
            top_k = 6

        logger.info(
            "DynamicTopK | words=%d | selected_top_k=%d",
            words,
            top_k,
        )

        return top_k
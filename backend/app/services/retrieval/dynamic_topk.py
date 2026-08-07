import logging

logger = logging.getLogger(__name__)

# =============================================================================
# Constants
# =============================================================================

SIMPLE_QUERY_MAX_WORDS = 5
MEDIUM_QUERY_MAX_WORDS = 12

SIMPLE_QUERY_TOP_K = 2
MEDIUM_QUERY_TOP_K = 4
COMPLEX_QUERY_TOP_K = 6

# =============================================================================
# Dynamic Top-K Selector
# =============================================================================


class DynamicTopKSelector:
    """
    Selects the retrieval depth based on query complexity.

    Current implementation:
        • Rule-based heuristic

    Future improvements:
        • Planner-guided Top-K
        • Confidence-aware retrieval
        • Token-budget optimization
        • Adaptive retrieval using historical performance
    """

    def select(
        self,
        question: str,
    ) -> int:
        """
        Determines the optimal number of chunks to retrieve.

        Args:
            question:
                User retrieval query.

        Returns:
            Recommended Top-K value.
        """

        words = len(question.split())

        if words <= SIMPLE_QUERY_MAX_WORDS:

            top_k = SIMPLE_QUERY_TOP_K

        elif words <= MEDIUM_QUERY_MAX_WORDS:

            top_k = MEDIUM_QUERY_TOP_K

        else:

            top_k = COMPLEX_QUERY_TOP_K

        logger.info(
            (
                "DynamicTopK | "
                "words=%d | "
                "top_k=%d"
            ),
            words,
            top_k,
        )

        return top_k
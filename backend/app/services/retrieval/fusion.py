import logging
from collections import defaultdict

logger = logging.getLogger(__name__)

# =============================================================================
# Constants
# =============================================================================

DEFAULT_RRF_K = 60

# =============================================================================
# Reciprocal Rank Fusion
# =============================================================================


def reciprocal_rank_fusion(
    result_sets: list[list],
    k: int = DEFAULT_RRF_K,
) -> list:
    """
    Combines multiple ranked retrieval result sets using
    Reciprocal Rank Fusion (RRF).

    Args:
        result_sets:
            Ranked retrieval result lists.

        k:
            RRF smoothing constant.

    Returns:
        A single fused ranking.
    """

    if not result_sets:

        logger.info(
            "RRF skipped (no result sets)."
        )

        return []

    fused_scores: defaultdict[int, float] = defaultdict(float)
    unique_results: dict[int, object] = {}

    for results in result_sets:

        if not results:
            continue

        for rank, chunk in enumerate(results, start=1):

            chunk_id = chunk.payload.get("chunk_id")

            if chunk_id is None:
                continue

            unique_results[chunk_id] = chunk

            fused_scores[chunk_id] += (
                1.0 / (k + rank)
            )

    fused_results = [
        unique_results[chunk_id]
        for chunk_id, _ in sorted(
            fused_scores.items(),
            key=lambda item: item[1],
            reverse=True,
        )
    ]

    logger.info(
        (
            "RRF | result_sets=%d | "
            "unique_chunks=%d"
        ),
        len(result_sets),
        len(fused_results),
    )

    return fused_results
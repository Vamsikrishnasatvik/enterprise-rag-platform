from collections import defaultdict
import logging

logger = logging.getLogger(__name__)


def reciprocal_rank_fusion(
    result_sets: list[list],
    k: int = 60,
):
    """
    Fuse multiple ranked result lists using Reciprocal Rank Fusion (RRF).

    Args:
        result_sets: List of ranked retrieval result lists.
        k: RRF constant (default = 60).

    Returns:
        One ranked list.
    """

    fused_scores = defaultdict(float)
    unique_results = {}

    for results in result_sets:

        for rank, chunk in enumerate(results, start=1):

            chunk_id = chunk.payload["chunk_id"]

            unique_results[chunk_id] = chunk

            fused_scores[chunk_id] += 1 / (k + rank)

    ranked = sorted(
        fused_scores.items(),
        key=lambda item: item[1],
        reverse=True,
    )

    fused_results = [
        unique_results[chunk_id]
        for chunk_id, _ in ranked
    ]

    logger.info(
        "RRF fused %d result sets into %d unique chunks",
        len(result_sets),
        len(fused_results),
    )

    return fused_results
from collections import defaultdict


def reciprocal_rank_fusion(
    result_sets: list[list],
    k: int = 60,
):
    """
    Reciprocal Rank Fusion (RRF).

    Combines multiple ranked retrieval lists into a
    single ranking.

    Input:
        [
            semantic_results,
            bm25_results,
        ]

    Each result is a normalized dictionary.
    """

    scores = defaultdict(float)

    documents = {}

    for results in result_sets:

        for rank, chunk in enumerate(
            results,
            start=1,
        ):

            chunk_id = chunk["chunk_id"]

            scores[chunk_id] += 1 / (
                k + rank
            )

            documents[chunk_id] = chunk

    ranked = sorted(
        scores.items(),
        key=lambda x: x[1],
        reverse=True,
    )

    return [
        documents[chunk_id]
        for chunk_id, _ in ranked
    ]
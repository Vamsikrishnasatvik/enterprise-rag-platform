from typing import List


def hit_rate(
    retrieved_ids: List[int],
    expected_ids: List[int],
) -> float:
    """
    Returns 1 if any expected document
    appears in the retrieved list.
    """

    return float(
        any(
            doc in retrieved_ids
            for doc in expected_ids
        )
    )


def precision_at_k(
    retrieved_ids: List[int],
    expected_ids: List[int],
) -> float:

    if not retrieved_ids:
        return 0.0

    hits = sum(
        1
        for doc in retrieved_ids
        if doc in expected_ids
    )

    return hits / len(retrieved_ids)


def recall_at_k(
    retrieved_ids: List[int],
    expected_ids: List[int],
) -> float:

    if not expected_ids:
        return 0.0

    hits = sum(
        1
        for doc in expected_ids
        if doc in retrieved_ids
    )

    return hits / len(expected_ids)


def reciprocal_rank(
    retrieved_ids: List[int],
    expected_ids: List[int],
) -> float:

    for index, doc in enumerate(
        retrieved_ids,
        start=1,
    ):

        if doc in expected_ids:
            return 1 / index

    return 0.0
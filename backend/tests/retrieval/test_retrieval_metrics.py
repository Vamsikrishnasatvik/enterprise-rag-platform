from app.services.retrieval_evaluation_service import (
    hit_rate,
    precision_at_k,
    recall_at_k,
    reciprocal_rank,
)


def test_hit_rate():
    retrieved = [12, 44, 91, 150]
    expected = [91]

    assert hit_rate(retrieved, expected) == 1.0


def test_precision():
    retrieved = [12, 44, 91, 150]
    expected = [91]

    assert precision_at_k(retrieved, expected) == 0.25


def test_recall():
    retrieved = [12, 44, 91, 150]
    expected = [91]

    assert recall_at_k(retrieved, expected) == 1.0


def test_reciprocal_rank():
    retrieved = [12, 44, 91, 150]
    expected = [91]

    assert reciprocal_rank(retrieved, expected) == (1 / 3)
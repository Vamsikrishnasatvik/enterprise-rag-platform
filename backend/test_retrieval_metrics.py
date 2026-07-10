from app.services.retrieval_evaluation_service import (
    hit_rate,
    precision_at_k,
    recall_at_k,
    reciprocal_rank,
)

retrieved = [
    12,
    44,
    91,
    150,
]

expected = [
    91,
]

print("=" * 80)

print(
    "Hit Rate:",
    hit_rate(
        retrieved,
        expected,
    ),
)

print(
    "Precision:",
    precision_at_k(
        retrieved,
        expected,
    ),
)

print(
    "Recall:",
    recall_at_k(
        retrieved,
        expected,
    ),
)

print(
    "MRR:",
    reciprocal_rank(
        retrieved,
        expected,
    ),
)
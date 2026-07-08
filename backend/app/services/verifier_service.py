from pydantic import BaseModel


class VerificationResult(BaseModel):
    confidence_score: float
    needs_retry: bool
    verification_reason: str


def verify_retrieval(
    retrieved_chunks: list,
    context: str | None,
) -> VerificationResult:
    """
    Rule-based retrieval verifier.

    Confidence is based on:
    - retrieval scores
    - number of retrieved chunks
    - context size

    This produces a more realistic confidence than
    simply checking context length.
    """

    if not retrieved_chunks:
        return VerificationResult(
            confidence_score=0.0,
            needs_retry=True,
            verification_reason="No chunks retrieved.",
        )

    if not context or not context.strip():
        return VerificationResult(
            confidence_score=0.05,
            needs_retry=True,
            verification_reason="Context is empty.",
        )

    chunk_count = len(retrieved_chunks)
    context_length = len(context.strip())

    scores = [
        chunk.get("score", 0.0)
        for chunk in retrieved_chunks
    ]

    average_score = (
        sum(scores) / len(scores)
        if scores
        else 0.0
    )

    top_score = max(scores) if scores else 0.0

    retrieval_component = average_score

    chunk_component = min(
        chunk_count / 5,
        1.0,
    )

    context_component = min(
        context_length / 2500,
        1.0,
    )

    confidence = (
        retrieval_component * 0.60
        + chunk_component * 0.20
        + context_component * 0.20
    )

    confidence = round(confidence, 3)

    if confidence >= 0.90:
        return VerificationResult(
            confidence_score=confidence,
            needs_retry=False,
            verification_reason="Excellent retrieval quality.",
        )

    if confidence >= 0.80:
        return VerificationResult(
            confidence_score=confidence,
            needs_retry=False,
            verification_reason="Context appears sufficient.",
        )

    if (
        top_score >= 0.85
        and chunk_count >= 3
    ):
        return VerificationResult(
            confidence_score=confidence,
            needs_retry=False,
            verification_reason="Strong top match found.",
        )

    return VerificationResult(
        confidence_score=confidence,
        needs_retry=True,
        verification_reason="Low retrieval confidence. Retry recommended.",
    )
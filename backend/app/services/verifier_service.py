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
    Rule-based verifier.

    Later this will become an LLM-based verifier.
    """

    # No retrieval
    if not retrieved_chunks:
        return VerificationResult(
            confidence_score=0.0,
            needs_retry=True,
            verification_reason="No chunks retrieved.",
        )

    # Empty context
    if not context:
        return VerificationResult(
            confidence_score=0.1,
            needs_retry=True,
            verification_reason="Context is empty.",
        )

    chunk_count = len(retrieved_chunks)
    context_length = len(context.strip())

    confidence = min(
        1.0,
        (
            chunk_count / 5
            + min(context_length / 3000, 1.0)
        )
        / 2,
    )

    if confidence < 0.80:
        return VerificationResult(
            confidence_score=confidence,
            needs_retry=True,
            verification_reason="Low confidence. Retry retrieval.",
        )

    return VerificationResult(
        confidence_score=confidence,
        needs_retry=False,
        verification_reason="Context appears sufficient.",
    )
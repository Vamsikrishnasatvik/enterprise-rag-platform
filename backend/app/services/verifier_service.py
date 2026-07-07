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
    Initial heuristic verifier.

    Later versions will use an LLM.
    """

    if not retrieved_chunks:
        return VerificationResult(
            confidence_score=0.0,
            needs_retry=True,
            verification_reason="No chunks retrieved.",
        )

    if not context or len(context.strip()) < 100:
        return VerificationResult(
            confidence_score=0.2,
            needs_retry=True,
            verification_reason="Insufficient context.",
        )

    confidence = min(
        1.0,
        len(retrieved_chunks) / 5,
    )

    return VerificationResult(
        confidence_score=confidence,
        needs_retry=False,
        verification_reason="Context appears sufficient.",
    )
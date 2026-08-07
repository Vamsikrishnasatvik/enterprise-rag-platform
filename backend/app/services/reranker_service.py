import logging

from sentence_transformers import CrossEncoder

logger = logging.getLogger(__name__)

# =============================================================================
# Constants
# =============================================================================

MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"

# =============================================================================
# Model Singleton
# =============================================================================

_model: CrossEncoder | None = None


def get_model() -> CrossEncoder:
    """
    Returns the shared CrossEncoder instance.

    The model is loaded lazily and reused for all reranking requests.
    """

    global _model

    if _model is None:

        logger.info(
            "Loading reranker model: %s",
            MODEL_NAME,
        )

        _model = CrossEncoder(MODEL_NAME)

    return _model


# =============================================================================
# Reranking
# =============================================================================


def rerank_results(
    query: str,
    chunks: list,
) -> list:
    """
    Reranks retrieved chunks using a CrossEncoder model.

    The reranker score becomes the primary ranking score.
    """

    if not chunks:

        logger.info(
            "Reranker skipped (no chunks)."
        )

        return []

    logger.info(
        "Reranking %d chunk(s).",
        len(chunks),
    )

    model = get_model()

    pairs = [
        (
            query,
            chunk.payload.get("content", ""),
        )
        for chunk in chunks
    ]

    scores = model.predict(pairs)

    for chunk, score in zip(chunks, scores):

        score = float(score)

        chunk.payload["rerank_score"] = score
        chunk.score = score

    reranked = sorted(
        chunks,
        key=lambda chunk: chunk.score,
        reverse=True,
    )

    logger.info(
        "Reranking completed."
    )

    return reranked
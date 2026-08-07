import logging

from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

# =============================================================================
# Constants
# =============================================================================

MODEL_NAME = "BAAI/bge-small-en-v1.5"

# =============================================================================
# Model Singleton
# =============================================================================

_model: SentenceTransformer | None = None


def get_model() -> SentenceTransformer:
    """
    Returns the shared SentenceTransformer instance.

    The model is loaded lazily and reused for all embedding requests.
    """

    global _model

    if _model is None:

        logger.info(
            "Loading embedding model: %s",
            MODEL_NAME,
        )

        _model = SentenceTransformer(
            MODEL_NAME,
        )

    return _model


# =============================================================================
# Embedding Generation
# =============================================================================


def generate_embeddings(
    texts: list[str],
) -> list[list[float]]:
    """
    Generates normalized embeddings for the provided texts.
    """

    if not texts:
        return []

    logger.info(
        "Generating embeddings | texts=%d",
        len(texts),
    )

    model = get_model()

    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
    )

    return embeddings.tolist()
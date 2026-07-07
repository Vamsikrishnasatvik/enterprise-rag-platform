import logging

logger = logging.getLogger(__name__)


def build_context(results):
    """
    Build context from retrieved or reranked chunks.

    Supports both:
    - Qdrant ScoredPoint objects
    - Graph chunk dictionaries
    """

    context_parts = []

    for result in results:

        # Graph chunk dictionary
        if isinstance(result, dict):
            context_parts.append(
                result["content"]
            )

        # Qdrant ScoredPoint
        else:
            context_parts.append(
                result.payload["content"]
            )

    context = "\n\n".join(context_parts)

    MAX_CONTEXT_CHARS = 4000

    logger.info(
        "Context built (%d characters)",
        len(context),
    )

    return context[:MAX_CONTEXT_CHARS]
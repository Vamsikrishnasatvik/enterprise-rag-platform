import logging

logger = logging.getLogger(__name__)

# =============================================================================
# Constants
# =============================================================================

MAX_CONTEXT_CHARS = 4000

# =============================================================================
# Context Builder
# =============================================================================


def build_context(results: list) -> str:
    """
    Builds a single context string from retrieved chunks.

    The returned context is truncated to the maximum size
    accepted by downstream LLM prompts.
    """

    if not results:

        logger.info(
            "Context builder received no retrieval results."
        )

        return ""

    context = "\n\n".join(
        result.payload.get("content", "")
        for result in results
        if result.payload.get("content")
    )

    logger.info(
        "Built retrieval context | chunks=%d | length=%d",
        len(results),
        len(context),
    )

    return context[:MAX_CONTEXT_CHARS]
import logging

from app.prompts.compression_prompt import COMPRESSION_PROMPT
from app.services.llm_service import call_llm

logger = logging.getLogger(__name__)

# =============================================================================
# Compression Service
# =============================================================================


def compress_context(
    question: str,
    context: str,
) -> str:
    """
    Compresses retrieved context using the configured LLM.

    The compressed context should preserve only the information
    relevant to answering the user's question.
    """

    if not context.strip():

        logger.info(
            "Compression skipped (empty context)."
        )

        return ""

    logger.info(
        "Compressing context | original_length=%d",
        len(context),
    )

    prompt = COMPRESSION_PROMPT.format(
        question=question,
        context=context,
    )

    compressed = call_llm(prompt).strip()

    logger.info(
        "Compression completed | compressed_length=%d",
        len(compressed),
    )

    return compressed
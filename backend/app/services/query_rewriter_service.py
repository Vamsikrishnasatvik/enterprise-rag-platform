import logging

from app.prompts.query_rewriter_prompt import QUERY_REWRITER_PROMPT
from app.services.llm_service import call_llm

logger = logging.getLogger(__name__)

# Maximum allowed expansion of the rewritten query
MAX_LENGTH_MULTIPLIER = 2.0

# Suspicious patterns that indicate hallucinated metadata
FORBIDDEN_PATTERNS = (
    "[1]",
    "[2]",
    "Document ID",
    "Policy ID",
    "Version",
    "Owner:",
    "Department:",
)


def rewrite_query(
    question: str,
    memory_context: str = "",
) -> str:
    """
    Rewrite a user question into a retrieval-optimized query.
    Falls back to the original question if the rewrite appears unsafe.
    """

    prompt = QUERY_REWRITER_PROMPT.format(
        question=question,
        memory_context=memory_context,
    )

    logger.info("Rewriting retrieval query...")

    rewritten = call_llm(prompt).strip()

    logger.info("Original Query : %s", question)
    logger.info("Rewritten Query: %s", rewritten)

    # ---------------------------------------------------------
    # Empty response
    # ---------------------------------------------------------

    if not rewritten:
        logger.warning("Empty rewrite. Using original query.")
        return question

    # ---------------------------------------------------------
    # Common invalid responses
    # ---------------------------------------------------------

    if rewritten.lower() in {
        "none",
        "n/a",
        "null",
        "no rewrite needed",
    }:
        logger.warning("Invalid rewrite '%s'. Using original query.", rewritten)
        return question

    # ---------------------------------------------------------
    # Prevent excessive expansion
    # ---------------------------------------------------------

    if len(rewritten) > len(question) * MAX_LENGTH_MULTIPLIER:
        logger.warning(
            "Rewrite too long (%d vs %d). Using original query.",
            len(rewritten),
            len(question),
        )
        return question

    # ---------------------------------------------------------
    # Reject hallucinated metadata
    # ---------------------------------------------------------

    if any(pattern.lower() in rewritten.lower() for pattern in FORBIDDEN_PATTERNS):
        logger.warning(
            "Rewrite contains hallucinated metadata. Using original query."
        )
        return question

    return rewritten
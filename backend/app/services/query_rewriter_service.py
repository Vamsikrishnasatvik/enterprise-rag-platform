import logging

from app.prompts.query_rewriter_prompt import QUERY_REWRITER_PROMPT
from app.services.llm_service import call_llm

logger = logging.getLogger(__name__)

# =============================================================================
# Constants
# =============================================================================

MAX_LENGTH_MULTIPLIER = 2.0

INVALID_RESPONSES = {
    "none",
    "n/a",
    "null",
    "no rewrite needed",
}

FORBIDDEN_PATTERNS = (
    "[1]",
    "[2]",
    "Document ID",
    "Policy ID",
    "Version",
    "Owner:",
    "Department:",
)

# =============================================================================
# Query Rewriter
# =============================================================================


def rewrite_query(
    question: str,
    memory_context: str = "",
) -> str:
    """
    Rewrites a user question into a retrieval-optimized query.

    The rewritten query is validated before use to prevent
    hallucinated metadata, excessive expansion, or invalid output.
    If validation fails, the original question is returned.
    """

    logger.info("Rewriting retrieval query...")

    prompt = QUERY_REWRITER_PROMPT.format(
        question=question,
        memory_context=memory_context,
    )

    rewritten = call_llm(prompt).strip()

    logger.info("Original Query : %s", question)
    logger.info("Rewritten Query: %s", rewritten)

    if not _is_valid_rewrite(
        original=question,
        rewritten=rewritten,
    ):
        return question

    logger.info("Query rewrite accepted.")

    return rewritten


# =============================================================================
# Helpers
# =============================================================================


def _is_valid_rewrite(
    original: str,
    rewritten: str,
) -> bool:
    """
    Validates a rewritten query before it is used for retrieval.
    """

    # ---------------------------------------------------------
    # Empty response
    # ---------------------------------------------------------

    if not rewritten:

        logger.warning(
            "Empty rewrite. Using original query."
        )

        return False

    # ---------------------------------------------------------
    # Common invalid responses
    # ---------------------------------------------------------

    if rewritten.lower() in INVALID_RESPONSES:

        logger.warning(
            "Invalid rewrite '%s'. Using original query.",
            rewritten,
        )

        return False

    # ---------------------------------------------------------
    # Prevent excessive expansion
    # ---------------------------------------------------------

    if len(rewritten) > len(original) * MAX_LENGTH_MULTIPLIER:

        logger.warning(
            "Rewrite too long (%d vs %d). Using original query.",
            len(rewritten),
            len(original),
        )

        return False

    # ---------------------------------------------------------
    # Reject hallucinated metadata
    # ---------------------------------------------------------

    if any(
        pattern.lower() in rewritten.lower()
        for pattern in FORBIDDEN_PATTERNS
    ):

        logger.warning(
            "Rewrite contains hallucinated metadata. Using original query."
        )

        return False

    return True
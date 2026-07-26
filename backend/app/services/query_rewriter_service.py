import logging

from app.prompts.query_rewriter_prompt import QUERY_REWRITER_PROMPT
from app.services.llm_service import call_llm

logger = logging.getLogger(__name__)


def rewrite_query(
    question: str,
    memory: str = "",
) -> str:
    """
    Rewrite a user question into a retrieval-optimized query.
    """

    prompt = QUERY_REWRITER_PROMPT.format(
        question=question,
        memory=memory,
    )

    logger.info(
        "Rewriting retrieval query..."
    )

    rewritten = call_llm(prompt).strip()

    logger.info(
        "Original Query: %s",
        question,
    )

    logger.info(
        "Rewritten Query: %s",
        rewritten,
    )

    # ---------------------------------------------------------
    # Safety fallback
    # ---------------------------------------------------------

    if not rewritten:
        return question

    return rewritten
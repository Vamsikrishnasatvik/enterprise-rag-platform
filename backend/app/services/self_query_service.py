import json
import logging

from app.prompts.self_query_prompt import (
    SELF_QUERY_PROMPT,
)

from app.services.llm_service import (
    generate_text,
)

logger = logging.getLogger(__name__)


def generate_self_query(
    question: str,
) -> dict:
    """
    Generate an optimized retrieval query
    together with metadata filters.
    """

    prompt = SELF_QUERY_PROMPT.format(
        question=question,
    )

    try:

        response = generate_text(
            prompt=prompt,
            temperature=0.1,
        )

        result = json.loads(response)

        result.setdefault(
            "query",
            question,
        )

        result.setdefault(
            "metadata_filters",
            {},
        )

        logger.info(
            "Self-query generated successfully."
        )

        return result

    except Exception:

        logger.exception(
            "Self-query generation failed."
        )

        return {
            "query": question,
            "metadata_filters": {},
        }
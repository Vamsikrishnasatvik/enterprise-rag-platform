import json
import logging

from app.prompts.query_expansion_prompt import (
    QUERY_EXPANSION_PROMPT,
)

from app.services.llm_service import (
    generate_text,
)

logger = logging.getLogger(__name__)


def expand_query(
    question: str,
) -> list[str]:
    """
    Generate multiple search queries
    for the same user question.

    Falls back to the original query
    if expansion fails.
    """

    prompt = f"""
{QUERY_EXPANSION_PROMPT}

Question:
{question}
"""

    try:

        response = generate_text(
            prompt=prompt,
            temperature=0.1,
            response_format="json",
        )

        queries = json.loads(response)

        if (
            not isinstance(queries, list)
            or len(queries) == 0
        ):
            raise ValueError(
                "Invalid query expansion output."
            )

        # Remove duplicates while
        # preserving order.

        seen = set()

        unique_queries = []

        for query in queries:

            query = query.strip()

            if (
                query
                and query not in seen
            ):

                seen.add(query)

                unique_queries.append(
                    query
                )

        logger.info(
            "Generated %d search queries.",
            len(unique_queries),
        )

        return unique_queries

    except Exception:

        logger.exception(
            "Query expansion failed."
        )

        return [question]
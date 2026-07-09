import json
import logging
import requests

from app.core.config import settings

from app.prompts.query_expansion_prompt import (
    QUERY_EXPANSION_PROMPT,
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

        response = requests.post(
            f"{settings.OLLAMA_BASE_URL}/api/generate",
            json={
                "model": settings.OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "format": "json",
            },
            timeout=120,
        )

        response.raise_for_status()

        queries = json.loads(
            response.json()["response"]
        )

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
import logging

from app.services.llm_service import (
    generate_text,
)

logger = logging.getLogger(__name__)


def generate_multi_queries(
    question: str,
    max_queries: int = 4,
) -> list[str]:
    """
    Generate multiple semantic search queries
    from a single user question.
    """

    prompt = f"""
You are an enterprise search expert.

Generate {max_queries - 1} alternative search
queries for the user's question.

Requirements:
- Preserve the original meaning.
- Use different wording.
- Each query must be concise.
- Return ONLY one query per line.
- Do NOT number the queries.
- Do NOT explain anything.

Question:
{question}
"""

    try:

        response = generate_text(
            prompt=prompt,
            temperature=0.2,
        )

        queries = [
            line.strip()
            for line in response.splitlines()
            if line.strip()
        ]

        queries.insert(
            0,
            question,
        )

        unique = []

        for query in queries:

            if query not in unique:
                unique.append(query)

        logger.info(
            "Generated %d retrieval queries",
            len(unique),
        )

        return unique[:max_queries]

    except Exception:

        logger.exception(
            "Multi-query generation failed."
        )

        return [question]
import json

from app.services import llm_service
from app.prompts.query_understanding_prompt import (
    QUERY_UNDERSTANDING_PROMPT,
)
from app.schemas.query_understanding import (
    QueryUnderstandingResult,
)


def understand_query(
    question: str,
) -> QueryUnderstandingResult:

    prompt = f"""
{QUERY_UNDERSTANDING_PROMPT}

User Question:
{question}
"""

    result = llm_service.generate_text(
        prompt=prompt,
        temperature=0.0,
        response_format="json",
    )

    data = json.loads(result)

    return QueryUnderstandingResult.model_validate(data)
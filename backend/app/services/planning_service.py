import json
import requests

from app.core.config import settings

from app.prompts.planning_prompt import (
    PLANNING_PROMPT,
)

from app.schemas.execution_plan import (
    ExecutionPlan,
)


def create_execution_plan(
    question: str,
    intent: str,
    metadata_filters: dict,
) -> ExecutionPlan:

    prompt = f"""
{PLANNING_PROMPT}

Question:
{question}

Intent:
{intent}

Metadata Filters:
{json.dumps(metadata_filters, indent=2)}
"""

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

    result = response.json()["response"]

    data = json.loads(result)

    return ExecutionPlan.model_validate(data)
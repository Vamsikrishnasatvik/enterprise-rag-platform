import json
import logging
import requests

from app.core.config import settings

from app.prompts.planning_prompt import (
    PLANNING_PROMPT,
)

from app.schemas.execution_plan import (
    ExecutionPlan,
)

from app.services.planner_rules import (
    apply_planner_rules,
)

logger = logging.getLogger(__name__)


def create_execution_plan(
    question: str,
    intent: str | None = None,
    metadata_filters: dict | None = None,
    conversation_summary: str | None = None,
) -> ExecutionPlan:
    """
    Generate an execution plan using the LLM.

    Falls back to a safe default plan if generation fails.
    """

    metadata_filters = metadata_filters or {}

    prompt = f"""
{PLANNING_PROMPT}

Question:
{question}

Detected Intent:
{intent or "unknown"}

Conversation Summary:
{conversation_summary or "None"}

Metadata Filters:
{json.dumps(metadata_filters, indent=2)}
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

        result = response.json()["response"]

        data = json.loads(result)

        plan = ExecutionPlan.model_validate(
            data
        )

        plan = apply_planner_rules(
            plan=plan,
            question=question,
            history_length=0,  # Will be dynamic later
        )

        return plan

    except Exception:

        logger.exception(
            "Planner failed. Using default execution plan."
        )

        plan = ExecutionPlan(
            intent=intent or "general",
            search_strategy="hybrid",
            retrieval_count=3,
            use_memory=False,
            use_metadata_filters=False,
            metadata_filters={},
            requires_reranking=True,
            requires_verification=True,
            multi_document=False,
            use_hybrid_search=True,
            use_query_expansion=False,
            use_summary_memory=False,
        )

        return apply_planner_rules(
            plan=plan,
            question=question,
            history_length=0,
        )
import logging

from app.prompts.planner_prompt import PLANNER_PROMPT
from app.services.llm_service import invoke_json_llm

logger = logging.getLogger(__name__)

# =============================================================================
# Constants
# =============================================================================

DEFAULT_QUERY_TYPE = "knowledge"

DEFAULT_EXECUTION_PLAN = [
    {
        "tool": "rag",
        "inputs": {},
    }
]

# =============================================================================
# Planner Service
# =============================================================================


def create_execution_plan(
    question: str,
    memory_context: str = "",
) -> dict:
    """
    Generates an execution plan for the current user query.

    Returns:
        {
            "query_type": str,
            "execution_plan": list,
            "reason": str,
        }
    """

    prompt = PLANNER_PROMPT.format(
        question=question,
        memory_context=memory_context,
    )

    try:

        plan = invoke_json_llm(prompt)

        execution_plan = _normalize_execution_plan(
            plan.get("execution_plan")
        )

        return {
            "query_type": plan.get(
                "query_type",
                DEFAULT_QUERY_TYPE,
            ),
            "execution_plan": execution_plan,
            "reason": plan.get(
                "reason",
                "",
            ),
        }

    except Exception:

        logger.exception(
            "Planner failed. Falling back to default RAG plan."
        )

        return {
            "query_type": DEFAULT_QUERY_TYPE,
            "execution_plan": DEFAULT_EXECUTION_PLAN.copy(),
            "reason": "Planner fallback.",
        }


# =============================================================================
# Helpers
# =============================================================================


def _normalize_execution_plan(plan) -> list:
    """
    Ensures the execution plan always conforms to the expected format.
    """

    if not isinstance(plan, list) or not plan:
        return DEFAULT_EXECUTION_PLAN.copy()

    normalized = []

    for step in plan:

        if not isinstance(step, dict):
            continue

        normalized.append(
            {
                "tool": step.get(
                    "tool",
                    "rag",
                ),
                "inputs": step.get(
                    "inputs",
                    {},
                ),
            }
        )

    return normalized or DEFAULT_EXECUTION_PLAN.copy()
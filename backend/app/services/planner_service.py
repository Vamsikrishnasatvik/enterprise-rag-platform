import json
import logging

from app.prompts.planner_prompt import PLANNER_PROMPT
from app.services.llm_service import invoke_json_llm

logger = logging.getLogger(__name__)


def create_execution_plan(
    question: str,
    memory_context: str = "",
) -> dict:
    """
    Generate an execution plan for the current user question.
    """

    prompt = PLANNER_PROMPT.format(
        question=question,
        memory_context=memory_context,
    )

    try:

        plan = invoke_json_llm(prompt)

        query_type = plan.get(
            "query_type",
            "knowledge",
        )

        reason = plan.get(
            "reason",
            "",
        )

        execution_plan = plan.get(
            "execution_plan",
            [],
        )

        # -----------------------------------------------------
        # Validate execution plan
        # -----------------------------------------------------

        if not isinstance(
            execution_plan,
            list,
        ) or len(execution_plan) == 0:

            execution_plan = [
                {
                    "tool": "rag",
                    "inputs": {},
                }
            ]

        normalized_plan = []

        for step in execution_plan:

            normalized_plan.append(
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

        return {
            "query_type": query_type,
            "execution_plan": normalized_plan,
            "reason": reason,
        }

    except Exception:

        logger.exception(
            "Planner failed. Falling back to RAG."
        )

        return {
            "query_type": "knowledge",
            "execution_plan": [
                {
                    "tool": "rag",
                    "inputs": {},
                }
            ],
            "reason": "Fallback execution plan.",
        }
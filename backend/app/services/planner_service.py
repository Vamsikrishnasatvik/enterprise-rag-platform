import json
import logging

from app.prompts.planner_prompt import PLANNER_PROMPT
from app.services.llm_service import call_llm

logger = logging.getLogger(__name__)


DEFAULT_PLAN = {
    "query_type": "knowledge",
    "execution_plan": {
        "route": "retriever",
        "reflect": True,
        "verify": False,
    },
    "reason": "Planner failed. Using fallback execution plan.",
}


def create_execution_plan(
    question: str,
    memory_context: str = "",
) -> dict:
    """
    Generate an execution plan for the Agentic RAG workflow.
    """

    prompt = PLANNER_PROMPT.format(
        question=question,
        memory_context=memory_context,
    )

    response = call_llm(prompt).strip()

    logger.info("Planner Raw Response:\n%s", response)

    # ---------------------------------------------------------
    # Remove Markdown code fences
    # ---------------------------------------------------------

    if response.startswith("```"):
        response = (
            response.replace("```json", "")
            .replace("```", "")
            .strip()
        )

    # ---------------------------------------------------------
    # Parse JSON
    # ---------------------------------------------------------

    try:
        plan = json.loads(response)

    except Exception:
        logger.exception("Planner JSON parsing failed.")
        return DEFAULT_PLAN.copy()

    # ---------------------------------------------------------
    # Validate Top-Level Fields
    # ---------------------------------------------------------

    plan.setdefault(
        "query_type",
        DEFAULT_PLAN["query_type"],
    )

    plan.setdefault(
        "execution_plan",
        DEFAULT_PLAN["execution_plan"].copy(),
    )

    plan.setdefault(
        "reason",
        DEFAULT_PLAN["reason"],
    )

    # ---------------------------------------------------------
    # Validate Execution Plan
    # ---------------------------------------------------------

    execution_plan = plan["execution_plan"]

    execution_plan.setdefault("route", "retriever")
    execution_plan.setdefault("reflect", True)
    execution_plan.setdefault("verify", False)

    # ---------------------------------------------------------
    # Normalize Route
    # ---------------------------------------------------------

    valid_routes = {
        "answer",
        "retriever",
        "tool",
    }

    if execution_plan["route"] not in valid_routes:
        logger.warning(
            "Invalid planner route '%s'. Falling back to 'retriever'.",
            execution_plan["route"],
        )
        execution_plan["route"] = "retriever"

    # ---------------------------------------------------------
    # Logging
    # ---------------------------------------------------------

    logger.info(
        "Planner Decision | type=%s | route=%s | reflect=%s | verify=%s",
        plan["query_type"],
        execution_plan["route"],
        execution_plan["reflect"],
        execution_plan["verify"],
    )

    return plan
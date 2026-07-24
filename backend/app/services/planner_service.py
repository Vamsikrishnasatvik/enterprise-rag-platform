import json
import logging

from app.prompts.planner_prompt import PLANNER_PROMPT
from app.services.llm_service import call_llm

logger = logging.getLogger(__name__)


def create_execution_plan(question: str) -> dict:
    prompt = f"""
{PLANNER_PROMPT}

User Question:
{question}
"""

    response = call_llm(prompt)

    logger.info(response)

    try:
        return json.loads(response)

    except Exception:
        logger.exception("Planner JSON parsing failed.")

        return {
            "query_type": "knowledge",
            "execution_plan": {
                "retrieve": True,
                "reflect": True,
                "verify": False,
            },
            "reason": "Planner failed. Using fallback plan.",
        }
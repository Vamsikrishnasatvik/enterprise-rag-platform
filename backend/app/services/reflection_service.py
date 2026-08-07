import json
import logging

from app.prompts.reflection_prompt import REFLECTION_PROMPT
from app.services.llm_service import call_llm

logger = logging.getLogger(__name__)

# =============================================================================
# Constants
# =============================================================================

DEFAULT_REFLECTION = {
    "passed": False,
    "confidence": 0.0,
    "grounded": False,
    "retry": True,
    "issues": [
        "Reflection failed.",
    ],
    "feedback": "Fallback reflection generated.",
}

# =============================================================================
# Reflection Service
# =============================================================================


def evaluate_answer(
    question: str,
    context: str,
    answer: str,
) -> dict:
    """
    Evaluates a generated answer using the Reflection LLM.
    """

    prompt = REFLECTION_PROMPT.format(
        question=question,
        context=context,
        answer=answer,
    )

    logger.info(
        "========== Reflection Prompt ==========\n%s",
        prompt,
    )

    response = call_llm(prompt).strip()

    logger.info(
        "========== Reflection Raw Response ==========\n%s",
        response,
    )

    response = _strip_code_fences(response)

    try:
        reflection = json.loads(response)

    except json.JSONDecodeError:

        logger.exception(
            "Reflection JSON parsing failed."
        )

        return DEFAULT_REFLECTION.copy()

    reflection = _normalize_reflection(reflection)

    logger.info(
        (
            "Reflection Decision | "
            "passed=%s | "
            "confidence=%.2f | "
            "grounded=%s | "
            "retry=%s"
        ),
        reflection["passed"],
        reflection["confidence"],
        reflection["grounded"],
        reflection["retry"],
    )

    return reflection


# =============================================================================
# Helpers
# =============================================================================


def _strip_code_fences(text: str) -> str:
    """
    Removes Markdown code fences from LLM responses.
    """

    if text.startswith("```"):
        return (
            text.replace("```json", "")
            .replace("```", "")
            .strip()
        )

    return text


def _normalize_reflection(
    reflection: dict,
) -> dict:
    """
    Normalizes the reflection response into the expected schema.
    """

    reflection.setdefault("passed", False)
    reflection.setdefault("confidence", 0.0)
    reflection.setdefault("grounded", False)
    reflection.setdefault("retry", True)
    reflection.setdefault("issues", [])
    reflection.setdefault("feedback", "")

    try:
        confidence = float(
            reflection["confidence"]
        )
    except (TypeError, ValueError):
        confidence = 0.0

    reflection["confidence"] = max(
        0.0,
        min(confidence, 1.0),
    )

    reflection["passed"] = _to_bool(
        reflection["passed"]
    )

    reflection["grounded"] = _to_bool(
        reflection["grounded"]
    )

    reflection["retry"] = _to_bool(
        reflection["retry"]
    )

    if not isinstance(
        reflection["issues"],
        list,
    ):
        reflection["issues"] = [
            str(reflection["issues"])
        ]

    reflection["feedback"] = str(
        reflection["feedback"]
    )

    return reflection


def _to_bool(value) -> bool:
    """
    Converts common LLM boolean representations into Python booleans.
    """

    if isinstance(value, bool):
        return value

    if isinstance(value, str):
        return value.strip().lower() in {
            "true",
            "yes",
            "1",
        }

    return bool(value)
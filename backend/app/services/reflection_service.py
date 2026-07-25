import json
import logging

from app.prompts.reflection_prompt import REFLECTION_PROMPT
from app.services.llm_service import call_llm

logger = logging.getLogger(__name__)


DEFAULT_REFLECTION = {
    "passed": False,
    "confidence": 0.0,
    "grounded": False,
    "retry": True,
    "issues": [
        "Reflection failed."
    ],
    "feedback": "Fallback reflection generated.",
}


def evaluate_answer(
    question: str,
    context: str,
    answer: str,
) -> dict:
    """
    Evaluate the generated answer using the Reflection LLM.
    """

    prompt = REFLECTION_PROMPT.format(
        question=question,
        context=context,
        answer=answer,
    )

    # ---------------------------------------------------------
    # Debug Logging
    # ---------------------------------------------------------

    logger.info(
        "========== Reflection Prompt ==========\n%s",
        prompt,
    )

    response = call_llm(prompt).strip()

    logger.info(
        "========== Reflection Raw Response ==========\n%s",
        response,
    )

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
        reflection = json.loads(response)

    except json.JSONDecodeError:
        logger.exception("Reflection JSON parsing failed.")
        return DEFAULT_REFLECTION.copy()

    # ---------------------------------------------------------
    # Validate Required Fields
    # ---------------------------------------------------------

    reflection.setdefault("passed", False)
    reflection.setdefault("confidence", 0.0)
    reflection.setdefault("grounded", False)
    reflection.setdefault("retry", True)
    reflection.setdefault("issues", [])
    reflection.setdefault("feedback", "")

    # ---------------------------------------------------------
    # Normalize Confidence
    # ---------------------------------------------------------

    try:
        confidence = float(reflection["confidence"])
    except (TypeError, ValueError):
        confidence = 0.0

    reflection["confidence"] = max(
        0.0,
        min(confidence, 1.0),
    )

    # ---------------------------------------------------------
    # Normalize Boolean Fields
    # ---------------------------------------------------------

    def to_bool(value):
        if isinstance(value, bool):
            return value

        if isinstance(value, str):
            return value.strip().lower() in {
                "true",
                "yes",
                "1",
            }

        return bool(value)

    reflection["passed"] = to_bool(
        reflection["passed"]
    )

    reflection["grounded"] = to_bool(
        reflection["grounded"]
    )

    reflection["retry"] = to_bool(
        reflection["retry"]
    )

    # ---------------------------------------------------------
    # Normalize Issues
    # ---------------------------------------------------------

    if not isinstance(
        reflection["issues"],
        list,
    ):
        reflection["issues"] = [
            str(reflection["issues"])
        ]

    # ---------------------------------------------------------
    # Normalize Feedback
    # ---------------------------------------------------------

    reflection["feedback"] = str(
        reflection["feedback"]
    )

    # ---------------------------------------------------------
    # Logging
    # ---------------------------------------------------------

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
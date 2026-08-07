import json
import logging

from app.prompts.verification_prompt import VERIFICATION_PROMPT
from app.services.llm_service import call_llm

logger = logging.getLogger(__name__)

# =============================================================================
# Constants
# =============================================================================

DEFAULT_VERIFICATION = {
    "supported": False,
    "confidence": 0.0,
    "missing_information": [],
    "hallucinations": [],
    "reason": "Verification failed.",
}

INVALID_LIST_VALUES = {
    "",
    "none",
    "n/a",
}

INVALID_HALLUCINATION_VALUES = {
    "",
    "none",
    "n/a",
    "no hallucination detected",
}

# =============================================================================
# Verification Service
# =============================================================================


def verify_answer(
    question: str,
    answer: str,
    context: str,
) -> dict:
    """
    Verifies whether a generated answer is fully supported by
    the retrieved enterprise context.
    """

    prompt = VERIFICATION_PROMPT.format(
        question=question,
        answer=answer,
        context=context,
    )

    logger.info(
        "========== Verification Prompt ==========\n%s",
        prompt,
    )

    response = call_llm(prompt).strip()

    logger.info(
        "========== Verification Raw Response ==========\n%s",
        response,
    )

    response = _strip_code_fences(response)

    try:
        verification = json.loads(response)

    except json.JSONDecodeError:

        logger.exception(
            "Verification JSON parsing failed."
        )

        return DEFAULT_VERIFICATION.copy()

    verification = _normalize_verification(
        verification,
    )

    logger.info(
        (
            "Verification Decision | "
            "supported=%s | "
            "confidence=%.2f | "
            "hallucinations=%d | "
            "missing=%d"
        ),
        verification["supported"],
        verification["confidence"],
        len(verification["hallucinations"]),
        len(verification["missing_information"]),
    )

    return verification


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


def _normalize_verification(
    verification: dict,
) -> dict:
    """
    Normalizes the verification response into the expected schema.
    """

    verification.setdefault("supported", False)
    verification.setdefault("confidence", 0.0)
    verification.setdefault("missing_information", [])
    verification.setdefault("hallucinations", [])
    verification.setdefault("reason", "")

    try:
        confidence = float(
            verification["confidence"]
        )
    except (TypeError, ValueError):
        confidence = 0.0

    verification["confidence"] = max(
        0.0,
        min(confidence, 1.0),
    )

    verification["supported"] = _to_bool(
        verification["supported"]
    )

    verification["hallucinations"] = _normalize_list(
        verification["hallucinations"],
        INVALID_HALLUCINATION_VALUES,
    )

    verification["missing_information"] = _normalize_list(
        verification["missing_information"],
        INVALID_LIST_VALUES,
    )

    verification["reason"] = str(
        verification["reason"]
    )

    return verification


def _normalize_list(
    value,
    invalid_values: set[str],
) -> list[str]:
    """
    Normalizes list-like values returned by the LLM.
    """

    if not isinstance(value, list):
        value = [str(value)]

    return [
        str(item)
        for item in value
        if str(item).strip().lower() not in invalid_values
    ]


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
import json
import logging

from app.prompts.verification_prompt import VERIFICATION_PROMPT
from app.services.llm_service import call_llm

logger = logging.getLogger(__name__)


DEFAULT_VERIFICATION = {
    "supported": False,
    "confidence": 0.0,
    "missing_information": [],
    "hallucinations": [],
    "reason": "Verification failed.",
}


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


def verify_answer(
    question: str,
    answer: str,
    context: str,
) -> dict:
    """
    Verify whether the generated answer is fully supported
    by the retrieved enterprise context.
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

    # ---------------------------------------------------------
    # Remove Markdown
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
        verification = json.loads(response)

    except json.JSONDecodeError:

        logger.exception(
            "Verification JSON parsing failed."
        )

        return DEFAULT_VERIFICATION.copy()

    # ---------------------------------------------------------
    # Validate Required Fields
    # ---------------------------------------------------------

    verification.setdefault("supported", False)
    verification.setdefault("confidence", 0.0)
    verification.setdefault("missing_information", [])
    verification.setdefault("hallucinations", [])
    verification.setdefault("reason", "")

    # ---------------------------------------------------------
    # Normalize Confidence
    # ---------------------------------------------------------

    try:
        confidence = float(
            verification["confidence"]
        )
    except (ValueError, TypeError):
        confidence = 0.0

    verification["confidence"] = max(
        0.0,
        min(confidence, 1.0),
    )

    # ---------------------------------------------------------
    # Normalize Boolean
    # ---------------------------------------------------------

    verification["supported"] = to_bool(
        verification["supported"]
    )

    # ---------------------------------------------------------
    # Normalize Hallucinations
    # ---------------------------------------------------------

    if not isinstance(
        verification["hallucinations"],
        list,
    ):
        verification["hallucinations"] = [
            str(
                verification["hallucinations"]
            )
        ]

    # Remove bogus "No hallucination..." responses

    verification["hallucinations"] = [
        item
        for item in verification["hallucinations"]
        if str(item).strip().lower()
        not in {
            "",
            "none",
            "n/a",
            "no hallucination detected",
        }
    ]

    # ---------------------------------------------------------
    # Normalize Missing Information
    # ---------------------------------------------------------

    if not isinstance(
        verification["missing_information"],
        list,
    ):
        verification["missing_information"] = [
            str(
                verification["missing_information"]
            )
        ]

    verification["missing_information"] = [
        item
        for item in verification["missing_information"]
        if str(item).strip().lower()
        not in {
            "",
            "none",
            "n/a",
        }
    ]

    # ---------------------------------------------------------
    # Normalize Reason
    # ---------------------------------------------------------

    verification["reason"] = str(
        verification["reason"]
    )

    # ---------------------------------------------------------
    # Logging
    # ---------------------------------------------------------

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
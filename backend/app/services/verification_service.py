import json

from app.prompts.verification_prompt import (
    VERIFICATION_PROMPT,
)
from app.services.llm_service import call_llm


def verify_answer(
    question: str,
    context: str,
    answer: str,
):
    prompt = f"""
{VERIFICATION_PROMPT}

Question:
{question}

Retrieved Context:
{context}

Generated Answer:
{answer}
"""

    response = call_llm(prompt)

    try:
        return json.loads(response)

    except Exception:
        return {
            "verified": False,
            "reason": "Verification failed.",
        }
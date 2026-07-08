import json
import requests

from app.core.config import settings

from app.prompts.memory_rewrite_prompt import (
    MEMORY_REWRITE_PROMPT,
)


def rewrite_query(
    question: str,
    summary: str | None,
    recent_history: list,
) -> str:
    """
    Rewrite follow-up questions into standalone queries
    using the conversation summary and recent messages.
    """

    prompt = f"""
{MEMORY_REWRITE_PROMPT}

Conversation Summary:

{summary or "No conversation summary available."}

Recent Messages:

{json.dumps(recent_history, indent=2)}

Current User Question:

{question}
"""

    response = requests.post(
        f"{settings.OLLAMA_BASE_URL}/api/generate",
        json={
            "model": settings.OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
        },
        timeout=120,
    )

    response.raise_for_status()

    rewritten = response.json()["response"].strip()

    return rewritten
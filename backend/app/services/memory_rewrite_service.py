import json

from app.prompts.memory_rewrite_prompt import (
    MEMORY_REWRITE_PROMPT,
)

from app.services.llm_service import (
    generate_text,
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

    return generate_text(
        prompt=prompt,
        temperature=0.1,
    ).strip()
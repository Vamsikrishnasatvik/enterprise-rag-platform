import requests

from app.core.config import settings


def summarize_conversation(
    history: list,
) -> str:
    """
    Generate a concise summary of a conversation.

    This summary is used by the MemoryAgent to
    preserve long-term context without sending
    the entire chat history to the LLM.
    """

    if not history:
        return ""

    conversation = ""

    for message in history:
        conversation += (
            f"{message['role']}: "
            f"{message['content']}\n"
        )

    prompt = f"""
You are summarizing an enterprise chat conversation.

Write a concise summary that preserves:

- main topic
- important facts
- decisions
- unresolved questions
- user preferences (if any)

Keep the summary under 200 words.

Conversation:

{conversation}

Summary:
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

    return response.json()["response"].strip()
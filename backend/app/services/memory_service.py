from app.core.config import settings
import requests


def generate_conversation_summary(
    text: str,
):
    prompt = f"""
You are an AI assistant.

Summarize the following conversation in 2-3 concise sentences.

Focus on:
- user goals
- important facts
- datasets discussed
- decisions made

Conversation:

{text}

Summary:
"""

    try:
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

        data = response.json()

        return data.get(
            "response",
            text[:1000],
        )

    except Exception as e:
        print(
            "SUMMARY GENERATION FAILED:",
            str(e),
        )
        return text[:1000]
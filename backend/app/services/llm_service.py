import requests

from app.core.config import settings

from app.prompts.answer_prompt import (
    ANSWER_PROMPT,
)
import json

def generate_text(
    prompt: str,
    temperature: float = 0.1,
    response_format: str | None = None,
    timeout: int = 120,
) -> str:
    """
    Generic Ollama text generation.

    Used by:
    - Answer Agent
    - Metadata Extraction
    - Multi-Query Retrieval
    - Query Expansion
    - Future AI services
    """

    # -----------------------------
    # Test fallback
    # -----------------------------
    if settings.ENVIRONMENT == "test":

        prompt_lower = prompt.lower()

        if "multi" in prompt_lower and "query" in prompt_lower:
            return json.dumps([
                "What is the HR Leave Policy?",
                "Explain employee leave policy",
                "Annual leave rules",
                "Paid leave policy",
            ])

        return "Test response"

    try:

        payload = {
            "model": settings.OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "top_p": 0.9,
            },
        }

        if response_format == "json":
            payload["format"] = "json"

        response = requests.post(
            f"{settings.OLLAMA_BASE_URL}/api/generate",
            json=payload,
            timeout=timeout,
        )

        response.raise_for_status()

        return response.json().get(
            "response",
            "",
        ).strip()

    except requests.exceptions.RequestException:
        raise


def generate_answer(
    question: str,
    context: str,
    history: list | None = None,
):
    """
    Generate the final answer using the LLM.
    """

    history_text = ""

    if history:
        history_text = "\n".join(
            f"{message['role']}: {message['content']}"
            for message in history
        )

    prompt = ANSWER_PROMPT.format(
        question=question,
        context=context,
        history=history_text or "None",
    )

    print("=" * 80)
    print(
        "OLLAMA MODEL:",
        settings.OLLAMA_MODEL,
    )
    print(
        "PROMPT LENGTH:",
        len(prompt),
    )
    print("=" * 80)

    answer = generate_text(
        prompt=prompt,
        temperature=0.1,
    )

    print("=" * 80)
    print("OLLAMA RESPONSE RECEIVED")
    print("=" * 80)

    return answer
import requests

from app.core.config import settings

from app.prompts.answer_prompt import (
    ANSWER_PROMPT,
)


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
        history=history_text if history_text else "None",
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

    try:

        response = requests.post(
            f"{settings.OLLAMA_BASE_URL}/api/generate",
            json={
                "model": settings.OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.1,
                    "top_p": 0.9,
                },
            },
            timeout=120,
        )

        print(
            "OLLAMA STATUS:",
            response.status_code,
        )

        if response.status_code != 200:
            print("OLLAMA ERROR:")
            print(response.text)

        response.raise_for_status()

        return response.json().get(
            "response",
            "No response generated.",
        ).strip()

    except requests.exceptions.RequestException as e:

        print("OLLAMA REQUEST FAILED:")
        print(str(e))
        raise
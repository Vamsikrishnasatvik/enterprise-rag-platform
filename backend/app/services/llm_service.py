import requests

from app.core.config import settings


def call_llm(prompt: str) -> str:
    """
    Generic function to send a prompt to the configured LLM.
    """

    print("=" * 80)
    print("OLLAMA MODEL:", settings.OLLAMA_MODEL)
    print("PROMPT LENGTH:", len(prompt))
    print("=" * 80)

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

        print("OLLAMA STATUS:", response.status_code)

        if response.status_code != 200:
            print(response.text)

        response.raise_for_status()

        return response.json().get(
            "response",
            "No response generated.",
        )

    except requests.exceptions.RequestException:
        print("OLLAMA REQUEST FAILED")
        raise


def generate_answer(
    question: str,
    context: str,
    history: list | None = None,
):
    """
    Build the RAG prompt and call the LLM.
    """

    history_text = ""

    if history:
        for msg in history:
            history_text += (
                f"{msg['role']}: "
                f"{msg['content']}\n"
            )

    prompt = f"""
You are a data analyst.

The CONTEXT contains tabular data.

You MUST answer ONLY from the CONTEXT.

You MUST NOT use external knowledge.

Conversation History:
{history_text}

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""

    return call_llm(prompt)
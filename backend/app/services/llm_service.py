import requests

from app.core.config import settings


def generate_answer(
    question: str,
    context: str,
    history: list | None = None,
):
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

If the question asks for:
- highest
- lowest
- maximum
- minimum
- average
- count
- top

you must inspect the values in the context and compute the answer.

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
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
        "prompt": question,
        "stream": False,
    },
    timeout=120,
)

        print("OLLAMA STATUS:", response.status_code)

        if response.status_code != 200:
            print("OLLAMA ERROR:")
            print(response.text)

        response.raise_for_status()

        data = response.json()

        return data.get(
            "response",
            "No response generated.",
        )

    except requests.exceptions.RequestException as e:
        print("OLLAMA REQUEST FAILED:")
        print(str(e))
        raise
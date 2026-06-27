import requests

from app.core.config import settings


def generate_answer(
    question: str,
    context: str,
):
    prompt = f"""
You are an enterprise document assistant.

Answer ONLY from the provided context.

If the answer is not present in the context, reply:

I could not find that information in the uploaded documents.

Context:
{context}

Question:
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

    data = response.json()

    return data["response"]
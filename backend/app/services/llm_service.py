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
    You are an Enterprise RAG assistant.

    Your task is to answer questions ONLY using the provided CONTEXT.

    ========================
    INSTRUCTIONS
    ========================

    1. Read the entire CONTEXT carefully before answering.

    2. If the CONTEXT contains enough information:
    - Answer clearly and directly.
    - Summarize relevant information when appropriate.
    - Quote important facts if they help answer the question.

    3. If the CONTEXT contains PARTIAL information:
    - Answer using the available information.
    - Clearly mention that the retrieved content appears to be partial or an overview if applicable.
    - Do NOT say "the context does not contain..." unless absolutely no relevant information exists.

    4. If the answer truly cannot be found:
    - Respond:
        "The indexed documents do not contain enough information to answer this question."

    5. Never use external knowledge.

    6. Never invent facts.

    7. For numerical questions (highest, lowest, average, maximum, minimum, count, top, total):
    - Calculate the answer ONLY from the CONTEXT.

    8. If multiple retrieved chunks discuss the same topic:
    - Combine the information into one coherent answer.

    9. Prefer explaining what IS available rather than describing what is missing.

    ========================
    CONTEXT
    ========================

    {context}

    ========================
    QUESTION
    ========================

    {question}

    ========================
    ANSWER
    ========================
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
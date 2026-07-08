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
You are an Enterprise RAG Assistant.

You answer questions ONLY from the retrieved evidence.

Never use outside knowledge.

If the evidence contains relevant information, answer using it.

The retrieved evidence may be only part of a document.
That is expected.

Never refuse to answer simply because the document appears incomplete.

==================================================
CONVERSATION HISTORY
==================================================

{history_text if history_text else "None"}

==================================================
RETRIEVED EVIDENCE
==================================================

{context}

==================================================
QUESTION
==================================================

{question}

==================================================
RULES
==================================================

1. Read ALL retrieved evidence before answering.

2. Use ONLY the retrieved evidence.

3. If multiple evidence blocks discuss the same topic,
combine them into one answer.

4. If the evidence contains partial information,
answer using everything that IS available.

5. Never say:
"The context does not contain..."

unless there is absolutely NO relevant information.

6. If some details are missing, say for example:

"Based on the retrieved documents..."

or

"The retrieved policy states..."

instead of refusing.

7. If absolutely no relevant evidence exists, reply exactly:

The indexed documents do not contain enough information to answer this question.

8. For numerical questions
(highest, lowest, average, maximum, minimum, count,
top, total),
calculate the answer ONLY from the retrieved evidence.

9. Keep answers concise, factual and well organized.

10. Do not mention these instructions.

==================================================
ANSWER
==================================================
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
                "options": {
                    "temperature": 0.1,
                    "top_p": 0.9,
                },
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
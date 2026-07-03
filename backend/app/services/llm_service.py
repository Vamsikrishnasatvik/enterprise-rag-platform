import requests

from app.core.config import settings

from app.services.cache_service import (
    get_cache,
    set_cache,
)


def generate_answer(
    question: str,
    context: str,
    history: list | None = None,
):
    # ==========================
    # LLM Response Cache
    # ==========================
    cache_key = (
        f"llm:{question}:{hash(context)}"
    )

    cached_answer = get_cache(
        cache_key
    )

    if cached_answer:
        print("=" * 80)
        print("LLM CACHE HIT")
        print("=" * 80)
        return cached_answer

    # ==========================
    # Build Chat History
    # ==========================
    history_text = ""

    if history:
        for msg in history:
            history_text += (
                f"{msg['role']}: "
                f"{msg['content']}\n"
            )

    # ==========================
    # Prompt
    # ==========================
    prompt = f"""
You are an expert data analyst.

You MUST answer ONLY from the provided CONTEXT.

The CONTEXT may contain:
- CSV rows
- tables
- datasets
- numerical values
- business documents

Conversation History:
{history_text}

Rules:

1. NEVER use external knowledge.
2. NEVER invent facts.
3. Use ONLY the information present in the CONTEXT.
4. If the question asks about:
   - highest
   - lowest
   - maximum
   - minimum
   - average
   - count
   - top
   - salary
   - countries
   - rankings
   - totals
   - percentages

   then:

   a. inspect the table carefully.
   b. perform the necessary calculations.
   c. identify the corresponding row names.
   d. explain the answer clearly.

5. Never return only a number if the row name can be determined.

Examples:

Question:
Which school has the highest weighted salary?

Answer:
Stanford Graduate School of Business has the highest weighted salary of 250,650 US$.

Question:
What is the average weighted salary?

Answer:
The average weighted salary is 178,245 US$.

Question:
How many schools are located in India?

Answer:
There are 5 schools located in India.

6. If multiple rows satisfy the condition, list all of them.

7. If the answer cannot be determined from the context, respond EXACTLY with:

I cannot determine the answer from the provided documents.

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
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0,
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

        data = response.json()

        answer = data.get(
            "response",
            "No response generated.",
        )

        # ==========================
        # Save to Redis
        # ==========================
        set_cache(
            cache_key,
            answer,
            ttl=3600,
        )

        return answer

    except requests.exceptions.RequestException as e:
        print(
            "OLLAMA REQUEST FAILED:"
        )
        print(str(e))
        raise
from click import prompt
import requests

from app.core.config import settings
from app.prompts.summarizer_prompt import SUMMARIZER_PROMPT

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
    memory_context: str = "",
):
    """
    Build the RAG prompt and call the LLM.
    """

    prompt = f"""
You are an enterprise AI assistant.

Use the retrieved CONTEXT as the primary source of truth.

Use the Conversation Memory only to understand follow-up
questions and references.

If the answer is not present in the CONTEXT,
say that the information was not found.

Conversation Memory:
{memory_context}

Retrieved Context:
{context}

Current Question:
{question}

Answer:
"""

def generate_summary(
    conversation: str,
) -> str:
    """
    Generate a concise summary of a conversation.
    """

    prompt = SUMMARIZER_PROMPT.format(
        conversation=conversation,
    )

    return call_llm(prompt)
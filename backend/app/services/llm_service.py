import logging

import requests

from app.core.config import settings
from app.prompts.answer_prompt import ANSWER_PROMPT
from app.prompts.general_answer_prompt import GENERAL_ANSWER_PROMPT

logger = logging.getLogger(__name__)

# =============================================================================
# Generic LLM Client
# =============================================================================

def call_llm(prompt: str) -> str:
    """
    Generic transport layer for communicating with the configured LLM.
    """

    logger.info(
        "Calling LLM | model=%s | prompt_length=%d",
        settings.OLLAMA_MODEL,
        len(prompt),
    )

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

        logger.info("LLM completed successfully.")

        return response.json().get(
            "response",
            "No response generated.",
        )

    except requests.exceptions.RequestException:
        logger.exception("LLM request failed.")
        raise


# =============================================================================
# Enterprise RAG Answer Generation
# =============================================================================

def generate_answer(
    question: str,
    context: str,
    memory_context: str = "",
) -> str:
    """
    Generate an answer using enterprise knowledge retrieved
    from the RAG pipeline.
    """

    prompt = ANSWER_PROMPT.format(
        memory_context=memory_context,
        context=context,
        question=question,
    )

    logger.debug(
        "Generating RAG answer | context_length=%d | memory_length=%d",
        len(context),
        len(memory_context),
    )

    return call_llm(prompt)


# =============================================================================
# General Answer Generation
# =============================================================================

def generate_general_answer(
    question: str,
    memory_context: str = "",
) -> str:
    """
    Generate a conversational answer that does not require
    enterprise document retrieval.
    """

    prompt = GENERAL_ANSWER_PROMPT.format(
        memory_context=memory_context,
        question=question,
    )

    logger.debug(
        "Generating general answer | memory_length=%d",
        len(memory_context),
    )

    return call_llm(prompt)
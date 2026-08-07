import json
import logging

import requests

from app.core.config import settings
from app.prompts.answer_prompt import ANSWER_PROMPT
from app.prompts.general_answer_prompt import GENERAL_ANSWER_PROMPT

logger = logging.getLogger(__name__)

# =============================================================================
# Constants
# =============================================================================

LLM_TIMEOUT = 120

# =============================================================================
# Generic LLM Client
# =============================================================================


def call_llm(prompt: str) -> str:
    """
    Sends a prompt to the configured LLM and returns the generated response.

    Used by:
        - PlannerAgent
        - QueryRewriterAgent
        - CompressionAgent
        - AnswerAgent
        - ReflectionAgent
        - VerificationAgent
        - Future agents
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
            timeout=LLM_TIMEOUT,
        )

        response.raise_for_status()

        logger.info("LLM completed successfully.")

        return response.json().get(
            "response",
            "",
        ).strip()

    except requests.RequestException:
        logger.exception("LLM request failed.")
        raise


# =============================================================================
# JSON LLM
# =============================================================================


def invoke_json_llm(prompt: str) -> dict:
    """
    Calls the LLM expecting a JSON response.

    Used by:
        - PlannerAgent
        - ReflectionAgent
        - VerificationAgent
        - Future Tool Planner
    """

    response = call_llm(prompt).strip()

    try:
        return json.loads(response)

    except json.JSONDecodeError:

        logger.error(
            "Invalid JSON returned by LLM:\n%s",
            response,
        )

        raise ValueError(
            "LLM returned invalid JSON."
        )


# =============================================================================
# Enterprise RAG Answer Generation
# =============================================================================


def generate_answer(
    question: str,
    context: str,
    memory_context: str = "",
) -> str:
    """
    Generates an answer grounded in retrieved enterprise documents.
    """

    prompt = ANSWER_PROMPT.format(
        memory_context=memory_context,
        context=context,
        question=question,
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
    Generates a conversational answer that does not require
    enterprise document retrieval.
    """

    prompt = GENERAL_ANSWER_PROMPT.format(
        memory_context=memory_context,
        question=question,
    )

    return call_llm(prompt)
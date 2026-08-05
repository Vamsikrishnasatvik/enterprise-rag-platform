import json
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

    return response.json().get(
        "response",
        "",
    )


# =============================================================================
# JSON LLM
# =============================================================================

def invoke_json_llm(prompt: str) -> dict:
    """
    Invoke the LLM expecting a JSON response.

    Used by:
        - Planner
        - Reflection
        - Verification
        - Future Tool Planner
    """

    response = call_llm(prompt)

    try:
        return json.loads(response)

    except json.JSONDecodeError:

        logger.exception(
            "Failed to parse JSON response from LLM."
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

    prompt = GENERAL_ANSWER_PROMPT.format(
        memory_context=memory_context,
        question=question,
    )

    return call_llm(prompt)
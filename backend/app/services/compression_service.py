from app.prompts.compression_prompt import COMPRESSION_PROMPT
from app.services.llm_service import call_llm


def compress_context(
    question: str,
    context: str,
) -> str:

    prompt = COMPRESSION_PROMPT.format(
        question=question,
        context=context,
    )

    return call_llm(prompt)
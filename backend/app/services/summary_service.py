from app.services.llm_service import generate_text


def summarize_conversation(
    history: list,
) -> str:
    """
    Generate a concise summary of a conversation.

    This summary is used by the MemoryAgent to
    preserve long-term context without sending
    the entire chat history to the LLM.
    """

    if not history:
        return ""

    conversation = ""

    for message in history:
        conversation += (
            f"{message['role']}: "
            f"{message['content']}\n"
        )

    prompt = f"""
You are summarizing an enterprise chat conversation.

Write a concise summary that preserves:

- main topic
- important facts
- decisions
- unresolved questions
- user preferences (if any)

Keep the summary under 200 words.

Conversation:

{conversation}

Summary:
"""

    return generate_text(
        prompt=prompt,
        temperature=0.1,
    )

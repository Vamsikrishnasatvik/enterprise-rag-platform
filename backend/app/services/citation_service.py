import re


def add_citations(
    answer: str,
    sources: list,
) -> str:
    """
    Adds a citation marker to each sentence in the answer.

    This implementation is deterministic and does not
    invoke another LLM.
    """

    if not sources:
        return answer

    citation = "[1]"

    sentences = re.split(r"(?<=[.!?])\s+", answer.strip())

    cited = []

    for sentence in sentences:

        sentence = sentence.strip()

        if not sentence:
            continue

        if re.search(r"\[\d+\]$", sentence):
            cited.append(sentence)
        else:
            cited.append(f"{sentence} {citation}")

    return " ".join(cited)
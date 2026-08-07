import re

# =============================================================================
# Constants
# =============================================================================

DEFAULT_CITATION = "[1]"

SENTENCE_SPLIT_PATTERN = r"(?<=[.!?])\s+"

EXISTING_CITATION_PATTERN = r"\[\d+\]$"

# =============================================================================
# Citation Service
# =============================================================================


def add_citations(
    answer: str,
    sources: list,
) -> str:
    """
    Adds deterministic inline citations to an answer.

    Each sentence receives a citation marker unless it already
    ends with an existing citation.

    This implementation is deterministic and does not invoke
    another LLM.
    """

    if not answer.strip():
        return answer

    if not sources:
        return answer

    citation = DEFAULT_CITATION

    sentences = re.split(
        SENTENCE_SPLIT_PATTERN,
        answer.strip(),
    )

    cited_sentences = []

    for sentence in sentences:

        sentence = sentence.strip()

        if not sentence:
            continue

        if re.search(
            EXISTING_CITATION_PATTERN,
            sentence,
        ):
            cited_sentences.append(sentence)
            continue

        cited_sentences.append(
            f"{sentence} {citation}"
        )

    return " ".join(cited_sentences)
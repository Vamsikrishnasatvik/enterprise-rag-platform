import logging

logger = logging.getLogger(__name__)


def prepare_evidence(
    chunks: list,
    max_chunks: int = 3,
) -> list:
    """
    Phase 3.6.1

    Prepare evidence for the AnswerAgent.

    Current responsibilities:
    - Keep top N reranked chunks
    - Remove duplicate chunk IDs

    Future:
    - Merge duplicate evidence
    - Group by document
    - Page-level citations
    """

    evidence = []
    seen = set()

    for chunk in chunks:

        if chunk["chunk_id"] in seen:
            continue

        seen.add(chunk["chunk_id"])

        evidence.append(chunk)

        if len(evidence) >= max_chunks:
            break

    logger.info(
        "Prepared %d evidence chunks",
        len(evidence),
    )

    return evidence
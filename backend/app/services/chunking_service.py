import logging

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
)

from app.schemas.parser import ParsedDocument

logger = logging.getLogger(__name__)

# =============================================================================
# Constants
# =============================================================================

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# =============================================================================
# Chunking Service
# =============================================================================


def chunk_document(
    parsed_document: ParsedDocument,
) -> list[str]:
    """
    Splits a parsed document into overlapping text chunks.

    Uses a RecursiveCharacterTextSplitter to preserve semantic
    context across chunk boundaries.
    """

    if not parsed_document.text.strip():

        logger.info(
            "Chunking skipped (empty document)."
        )

        return []

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )

    chunks = splitter.split_text(
        parsed_document.text,
    )

    logger.info(
        "Document chunked | chunks=%d | chunk_size=%d | overlap=%d",
        len(chunks),
        CHUNK_SIZE,
        CHUNK_OVERLAP,
    )

    return chunks
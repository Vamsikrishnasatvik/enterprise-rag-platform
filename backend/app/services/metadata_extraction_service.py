import json
import logging

from app.services import llm_service
from app.prompts.metadata_extraction_prompt import (
    METADATA_EXTRACTION_PROMPT,
)

logger = logging.getLogger(__name__)


def extract_metadata(
    document_text: str,
) -> dict:
    """
    Extract document-level metadata using the LLM.

    Runs once per document during ingestion.
    """

    prompt = f"""
{METADATA_EXTRACTION_PROMPT}

DOCUMENT

{document_text[:12000]}
"""

    try:

        response = llm_service.generate_text(
            prompt=prompt,
            temperature=0.0,
            response_format="json",
            timeout=300,
        )

        metadata = json.loads(response)

        metadata.setdefault(
            "tags",
            [],
        )

        return metadata

    except Exception:

        logger.exception(
            "Metadata extraction failed."
        )

        return {
            "department": "",
            "document_type": "",
            "version": "",
            "effective_date": "",
            "owner": "",
            "classification": "",
            "tags": [],
        }
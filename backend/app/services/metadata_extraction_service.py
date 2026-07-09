import json
import logging
import requests

from app.core.config import settings
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

        response = requests.post(
            f"{settings.OLLAMA_BASE_URL}/api/generate",
            json={
                "model": settings.OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "format": "json",
                "options": {
                    "temperature": 0,
                },
            },
            timeout=300,
        )

        response.raise_for_status()

        metadata = json.loads(
            response.json()["response"]
        )

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
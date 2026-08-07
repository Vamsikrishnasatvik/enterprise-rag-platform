import logging
from pathlib import Path

import fitz
from docx import Document as DocxDocument

from app.schemas.parser import ParsedDocument

logger = logging.getLogger(__name__)

# =============================================================================
# Constants
# =============================================================================

PDF_CONTENT_TYPE = "application/pdf"

DOCX_CONTENT_TYPE = (
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
)

TEXT_EXTENSIONS = {
    ".txt",
    ".csv",
}

# =============================================================================
# Public Parser
# =============================================================================


def parse_document(
    file_path: str,
    file_type: str,
) -> ParsedDocument:
    """
    Parses a document by dispatching to the appropriate parser
    based on MIME type or file extension.
    """

    file_type = (file_type or "").lower()
    suffix = Path(file_path).suffix.lower()

    logger.info(
        "Parsing document | file=%s | type=%s",
        file_path,
        file_type,
    )

    if (
        file_type == PDF_CONTENT_TYPE
        or suffix == ".pdf"
    ):
        return parse_pdf(file_path)

    if (
        file_type == DOCX_CONTENT_TYPE
        or suffix == ".docx"
    ):
        return parse_docx(file_path)

    if (
        file_type.startswith("text/")
        or suffix in TEXT_EXTENSIONS
    ):
        return parse_txt(file_path)

    raise ValueError(
        f"Unsupported document type: {file_type}"
    )


# =============================================================================
# PDF Parser
# =============================================================================


def parse_pdf(
    file_path: str,
) -> ParsedDocument:
    """
    Parses a PDF document using PyMuPDF.
    """

    pages: list[str] = []

    with fitz.open(file_path) as document:

        for page in document:
            pages.append(
                page.get_text("text")
            )

    text = "\n".join(pages)

    logger.info(
        "Parsed PDF | pages=%d",
        len(pages),
    )

    return ParsedDocument(
        text=text,
        page_count=len(pages),
        metadata={
            "filename": Path(file_path).name,
            "content_type": PDF_CONTENT_TYPE,
            "pages": pages,
        },
    )


# =============================================================================
# DOCX Parser
# =============================================================================


def parse_docx(
    file_path: str,
) -> ParsedDocument:
    """
    Parses a Microsoft Word (.docx) document.
    """

    document = DocxDocument(file_path)

    paragraphs = [
        paragraph.text
        for paragraph in document.paragraphs
        if paragraph.text.strip()
    ]

    logger.info(
        "Parsed DOCX | paragraphs=%d",
        len(paragraphs),
    )

    return ParsedDocument(
        text="\n".join(paragraphs),
        page_count=1,
        metadata={
            "filename": Path(file_path).name,
            "content_type": DOCX_CONTENT_TYPE,
        },
    )


# =============================================================================
# Text Parser
# =============================================================================


def parse_txt(
    file_path: str,
) -> ParsedDocument:
    """
    Parses plain text documents.
    """

    with open(
        file_path,
        "r",
        encoding="utf-8",
        errors="ignore",
    ) as file:

        text = file.read()

    logger.info(
        "Parsed text document | characters=%d",
        len(text),
    )

    return ParsedDocument(
        text=text,
        page_count=1,
        metadata={
            "filename": Path(file_path).name,
            "content_type": "text/plain",
        },
    )
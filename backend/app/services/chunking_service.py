from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
)

from app.schemas.parser import ParsedDocument


def chunk_document(
    parsed_document: ParsedDocument,
) -> list[str]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )

    return splitter.split_text(
        parsed_document.text
    )
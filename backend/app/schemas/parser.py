from typing import Any

from pydantic import BaseModel


class ParsedDocument(BaseModel):
    text: str
    page_count: int
    metadata: dict[str, Any]
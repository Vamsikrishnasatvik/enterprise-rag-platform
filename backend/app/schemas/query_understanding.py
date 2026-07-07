from pydantic import BaseModel, Field


class Entity(BaseModel):
    type: str
    value: str


class QueryUnderstandingResult(BaseModel):
    intent: str = Field(
        default="document_search"
    )

    rewritten_query: str

    entities: list[Entity] = []

    metadata_filters: dict = {}
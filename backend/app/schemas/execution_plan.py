from pydantic import BaseModel, Field


class ExecutionPlan(BaseModel):
    search_strategy: str = Field(
        default="semantic"
    )

    retrieval_count: int = Field(
        default=3,
        ge=1,
        le=10,
    )

    use_metadata_filters: bool = False

    use_memory: bool = False

    requires_reranking: bool = False

    requires_verification: bool = False

    multi_document: bool = False
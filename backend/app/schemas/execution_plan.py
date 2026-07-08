from pydantic import BaseModel, Field


class ExecutionPlan(BaseModel):
    """
    Execution plan produced by the PlannerAgent.

    This tells downstream agents how the workflow
    should execute.
    """

    # -------------------------
    # Query Understanding
    # -------------------------

    intent: str = "general"

    # -------------------------
    # Retrieval
    # -------------------------

    search_strategy: str = "semantic"

    retrieval_count: int = Field(
        default=3,
        ge=1,
        le=20,
    )

    # -------------------------
    # Conversation Memory
    # -------------------------

    use_memory: bool = False

    # -------------------------
    # Metadata Filtering
    # -------------------------

    use_metadata_filters: bool = False

    metadata_filters: dict = Field(
        default_factory=dict
    )

    # -------------------------
    # Retrieval Pipeline
    # -------------------------

    requires_reranking: bool = False

    requires_verification: bool = True

    multi_document: bool = False

    # -------------------------
    # Future Features
    # -------------------------

    use_hybrid_search: bool = False

    use_query_expansion: bool = False

    use_summary_memory: bool = False
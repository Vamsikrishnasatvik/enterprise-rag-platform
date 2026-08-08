from typing import Any, TypedDict


class GraphState(TypedDict, total=False):
    # ==========================================================
    # Runtime
    # ==========================================================

    db: Any
    conversation_id: int

    # ==========================================================
    # User Input
    # ==========================================================

    question: str

    # ==========================================================
    # Conversation Memory
    # ==========================================================

    conversation_summary: str
    recent_messages: list[dict[str, Any]]
    memory_context: str

    # ==========================================================
    # Planning
    # ==========================================================

    query_type: str
    planning_reason: str
    execution_plan: list[dict[str, Any]]

    # ==========================================================
    # Supervisor
    # ==========================================================

    needs_retrieval: bool
    needs_verification: bool

    # ==========================================================
    # Retrieval
    # ==========================================================

    retrieval_query: str
    retrieval_limit: int
    retrieval_strategy: str

    retrieved_chunks: list[Any]
    retrieval_context: str
    retrieved_documents: int
    retrieval_score: float
    reranker_score: float

    # ==========================================================
    # Compression
    # ==========================================================

    compressed_context: str

    # ==========================================================
    # Answer
    # ==========================================================

    answer: str
    citations: list[dict[str, Any]]

    # ==========================================================
    # Reflection
    # ==========================================================

    reflection: dict[str, Any]
    needs_retry: bool

    # ==========================================================
    # Verification
    # ==========================================================

    verification: dict[str, Any]

    # ==========================================================
    # Retry
    # ==========================================================

    retry_required: bool
    retry_count: int
    max_retries: int

    # ==========================================================
    # Tool Execution
    # ==========================================================

    tool_outputs: list[Any]

    # ==========================================================
    # Monitoring
    # ==========================================================

    execution_trace: list[dict[str, Any]]
    agent_timings: dict[str, float]
    errors: list[str]
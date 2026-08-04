from typing import Any, Dict, List, TypedDict


class GraphState(TypedDict, total=False):
    """
    Shared state passed between all agents.
    """

    # ==========================================================
    # Runtime
    # ==========================================================

    db: Any
    conversation_id: int

    # ==========================================================
    # User Input
    # ==========================================================

    question: str
    original_question: str

    # ==========================================================
    # Planner
    # ==========================================================

    execution_plan: Dict[str, Any]
    query_type: str
    planning_reason: str

    # ==========================================================
    # Supervisor
    # ==========================================================

    next_node: str
    routing_reason: str
    needs_retrieval: bool
    needs_verification: bool

    # ==========================================================
    # Conversation Memory
    # ==========================================================

    conversation_summary: str
    recent_messages: List[Dict[str, Any]]
    memory_context: str

    # ==========================================================
    # Retrieval
    # ==========================================================

    retrieval_query: str
    retrieval_limit: int
    retrieval_strategy: str

    retrieved_chunks: List[Any]

    # Final context passed to Answer and Reflection agents
    retrieval_context: str

    retrieved_document_count: int
    retrieval_score: float
    reranker_score: float

    # ==========================================================
    # Answer
    # ==========================================================

    answer: str
    citations: List[Dict[str, Any]]

    # ==========================================================
    # Reflection
    # ==========================================================

    reflection: Dict[str, Any]
    confidence_score: float
    needs_retry: bool

    # ==========================================================
    # Verification
    # ==========================================================

    verification: Dict[str, Any]
    verification_passed: bool
    verification_reason: str

    # ==========================================================
    # Retry
    # ==========================================================

    retry_required: bool
    retry_reason: str
    retry_count: int
    max_retries: int

    # ==========================================================
    # Monitoring
    # ==========================================================

    execution_trace: List[Dict[str, Any]]
    agent_timings: Dict[str, float]
    errors: List[str]

    # ==========================================================
    # Tool Calling (Future)
    # ==========================================================

    selected_tool: str
    tool_result: Dict[str, Any]
    tool_reason: str
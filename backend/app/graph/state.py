from typing import TypedDict, List, Dict, Any


class GraphState(TypedDict, total=False):
    """
    Shared state passed between all agents.
    """

    # ==========================================================
    # User Input
    # ==========================================================

    question: str

    # ==========================================================
    # Planner
    # ==========================================================

    execution_plan: Dict[str, bool]
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
    recent_messages: List[Dict]
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

    # ==========================================================
    # Answer
    # ==========================================================

    answer: str
    citations: List[Dict]

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

    execution_trace: List[Dict]
    agent_timings: Dict[str, float]
    errors: List[str]

    # ==========================================================
    # Tool Calling (Future)
    # ==========================================================

    selected_tool: str
    tool_result: Dict[str, Any]
    tool_reason: str
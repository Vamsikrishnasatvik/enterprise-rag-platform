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
    recent_messages: List[Dict[str, Any]]
    memory_context: str

    # ==========================================================
    # Planning
    # ==========================================================

    query_type: str
    planning_reason: str
    execution_plan: List[Dict[str, Any]]

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

    retrieved_chunks: List[Any]
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
    citations: List[Dict[str, Any]]

    # ==========================================================
    # Reflection
    # ==========================================================

    reflection: Dict[str, Any]
    needs_retry: bool

    # ==========================================================
    # Verification
    # ==========================================================

    verification: Dict[str, Any]

    # ==========================================================
    # Retry
    # ==========================================================

    retry_required: bool
    retry_count: int
    max_retries: int

    # ==========================================================
    # Tool Execution
    # ==========================================================

    tool_outputs: List[Any]

    # ==========================================================
    # Monitoring
    # ==========================================================

    execution_trace: List[Dict[str, Any]]
    agent_timings: Dict[str, float]
    errors: List[str]
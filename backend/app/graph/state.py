from typing import TypedDict, List, Dict


class GraphState(TypedDict, total=False):
    """
    Shared state passed between all agents.
    """

    # -----------------------------
    # User Input
    # -----------------------------
    question: str

    # -----------------------------
    # Planner
    # -----------------------------
    execution_plan: dict
    query_type: str
    planning_reason: str

    # -----------------------------
    # Supervisor
    # -----------------------------
    next_node: str
    routing_reason: str
    needs_retrieval: bool
    needs_verification: bool

    # -----------------------------
    # Memory
    # -----------------------------
    conversation_summary: str
    recent_messages: list
    conversation_history: list          # Temporary (remove later)
    memory_context: str

    # -----------------------------
    # Retrieval
    # -----------------------------
    retrieval_query: str
    retrieval_limit: int
    retrieval_strategy: str
    retrieved_chunks: list
    compressed_context: str             # Later rename to retrieval_context

    # -----------------------------
    # Answer
    # -----------------------------
    answer: str
    citations: List[Dict]

    # -----------------------------
    # Reflection
    # -----------------------------
    reflection: dict
    confidence_score: float
    needs_retry: bool

    # -----------------------------
    # Monitoring
    # -----------------------------
    execution_trace: List[str]
    agent_timings: Dict[str, float]
    retry_count: int
    errors: List[str]

    # -----------------------------
    # Verification
    # -----------------------------
    verification: dict
    verification_passed: bool
    verification_reason: str

    # -----------------------------
    # Retry
    # -----------------------------
    retry_required: bool
    retry_reason: str
    max_retries: int
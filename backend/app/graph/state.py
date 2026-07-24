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
    # Retrieval
    # -----------------------------
    retrieved_chunks: list
    compressed_context: str

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

    # Retry
    retry_required: bool
    retry_reason: str
    retry_count: int
    max_retries: int

    # Retrieval
    retrieval_limit: int
    retrieval_strategy: str
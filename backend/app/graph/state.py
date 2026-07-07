from typing import TypedDict, List, Dict, Any, Optional


class GraphState(TypedDict):
    """
    Shared state passed between all LangGraph nodes.
    """

    # ==========================
    # Request Information
    # ==========================
    question: str
    tenant_id: int
    user_id: int
    conversation_id: Optional[int]

    # ==========================
    # Query Understanding
    # ==========================
    rewritten_query: Optional[str]
    intent: Optional[str]
    entities: List[Dict[str, Any]]

    # ==========================
    # Planning
    # ==========================
    metadata_filters: Dict[str, Any]
    execution_plan: Dict[str, Any]

    # ==========================
    # Retrieval Configuration
    # ==========================
    search_limit: int
    use_metadata_filters: bool
    retrieval_strategy: str

    # ==========================
    # Retrieval
    # ==========================
    retrieved_chunks: List[Dict[str, Any]]
    reranked_chunks: List[Dict[str, Any]]
    evidence_chunks: List[Dict[str, Any]]
    context: Optional[str]

    # ==========================
    # Verification
    # ==========================
    confidence_score: float
    needs_retry: bool
    verification_reason: Optional[str]

    retrieval_attempts: int
    max_retrieval_attempts: int

    # ==========================
    # Final Response
    # ==========================
    answer: Optional[str]
    citations: List[Dict[str, Any]]

    # ==========================
    # Debugging / Monitoring
    # ==========================
    execution_trace: List[Dict[str, Any]]

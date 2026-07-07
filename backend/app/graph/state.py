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
    # Retrieval
    # ==========================
    retrieved_chunks: List[Dict[str, Any]]

    # ==========================
    # Verification
    # ==========================
    confidence_score: float
    needs_retry: bool

    # ==========================
    # Final Response
    # ==========================
    answer: Optional[str]
    citations: List[Dict[str, Any]]

    # ==========================
    # Debugging / Monitoring
    # ==========================
    execution_trace: List[str]
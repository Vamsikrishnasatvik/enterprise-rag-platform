from typing import TypedDict, List, Dict, Any


class GraphState(TypedDict, total=False):
    """
    Shared state passed between all agents in the LangGraph workflow.
    """

    # User input
    question: str

    # Query analysis
    query_analysis: Dict[str, Any]

    # Execution plan decided by the Supervisor
    execution_plan: Dict[str, Any]

    # Retrieved documents/chunks
    retrieved_chunks: List[Dict[str, Any]]

    # Context passed to the LLM
    compressed_context: str

    # Final response
    answer: str

    # Source citations
    citations: List[Dict[str, Any]]

    # Confidence score
    confidence_score: float

    # Reflection output
    reflection: Dict[str, Any]

    # Verification output
    verification: Dict[str, Any]

    # Execution tracing
    execution_trace: List[str]

    # Time spent by each agent
    agent_timings: Dict[str, float]

    # Retry count
    retry_count: int

    # Error list
    errors: List[str]
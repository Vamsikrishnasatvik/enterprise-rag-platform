from langgraph.graph import START, END, StateGraph

from app.graph.state import GraphState

from app.agents.memory_agent import MemoryAgent
from app.agents.planner_agent import PlannerAgent
from app.agents.supervisor_agent import SupervisorAgent
from app.agents.query_rewriter_agent import QueryRewriterAgent
from app.agents.retriever_agent import RetrieverAgent
from app.agents.compression_agent import CompressionAgent
from app.agents.answer_agent import AnswerAgent
from app.agents.citation_agent import CitationAgent
from app.agents.reflection_agent import ReflectionAgent
from app.agents.verification_agent import VerificationAgent
from app.agents.retry_agent import RetryAgent


# =============================================================================
# Constants
# =============================================================================

DEFAULT_MAX_RETRIES = 2


# =============================================================================
# Agent Instances
# =============================================================================

memory = MemoryAgent()
planner = PlannerAgent()
supervisor = SupervisorAgent()
query_rewriter = QueryRewriterAgent()
retriever = RetrieverAgent()
compression = CompressionAgent()
answer = AnswerAgent()
citation = CitationAgent()
reflection = ReflectionAgent()
verification = VerificationAgent()
retry = RetryAgent()


# =============================================================================
# Nodes
# =============================================================================

def memory_node(state: GraphState):
    return memory(state)


def planner_node(state: GraphState):
    return planner(state)


def supervisor_node(state: GraphState):
    return supervisor(state)


def query_rewriter_node(state: GraphState):
    return query_rewriter(state)


def retriever_node(state: GraphState):
    return retriever(state)


def compression_node(state: GraphState):
    return compression(state)


def answer_node(state: GraphState):
    return answer(state)


def citation_node(state: GraphState):
    return citation(state)


def reflection_node(state: GraphState):
    return reflection(state)


def verification_node(state: GraphState):
    return verification(state)


def retry_node(state: GraphState):
    return retry(state)


# =============================================================================
# Routers
# =============================================================================

def supervisor_router(state: GraphState):
    """
    Route according to the Planner/Supervisor decision.
    """

    route = state.get(
        "next_node",
        "answer",
    )

    if route not in {
        "answer",
        "retriever",
        "tool",
    }:
        route = "answer"

    return route


def reflection_router(state: GraphState):
    """
    Reflection routing.

    Flow:
    - Non-RAG -> END
    - Retry requested -> Retry (if retries remain)
    - Otherwise -> Verification
    """

    # ---------------------------------------------------------
    # Skip reflection for non-RAG queries
    # ---------------------------------------------------------

    if state.get("next_node") != "retriever":
        return "end"

    retry_count = state.get(
        "retry_count",
        0,
    )

    max_retries = state.get(
        "max_retries",
        DEFAULT_MAX_RETRIES,
    )

    needs_retry = state.get(
        "needs_retry",
        False,
    )

    # ---------------------------------------------------------
    # Retry if retries remain
    # ---------------------------------------------------------

    if (
        needs_retry
        and retry_count < max_retries
    ):
        return "retry"

    # ---------------------------------------------------------
    # Otherwise continue to verification
    # ---------------------------------------------------------

    return "verification"


def verification_router(state: GraphState):
    """
    Verification may request another retrieval if
    grounding failed.
    """

    retry_required = state.get(
        "retry_required",
        False,
    )

    retry_count = state.get(
        "retry_count",
        0,
    )

    max_retries = state.get(
        "max_retries",
        DEFAULT_MAX_RETRIES,
    )

    if (
        retry_required
        and retry_count < max_retries
    ):
        return "retry"

    return "end"


# =============================================================================
# Workflow
# =============================================================================

def build_workflow():
    """
    Build and compile the Agentic RAG workflow graph.
    """

    workflow = StateGraph(GraphState)

    # -------------------------------------------------------------------------
    # Register Nodes
    # -------------------------------------------------------------------------

    workflow.add_node("memory", memory_node)
    workflow.add_node("planner", planner_node)
    workflow.add_node("supervisor", supervisor_node)
    workflow.add_node("query_rewriter", query_rewriter_node)
    workflow.add_node("retriever", retriever_node)
    workflow.add_node("compression", compression_node)
    workflow.add_node("answer", answer_node)
    workflow.add_node("citation", citation_node)
    workflow.add_node("reflection", reflection_node)
    workflow.add_node("verification", verification_node)
    workflow.add_node("retry", retry_node)

    # -------------------------------------------------------------------------
    # Entry
    # -------------------------------------------------------------------------

    workflow.add_edge(START, "memory")
    workflow.add_edge("memory", "planner")
    workflow.add_edge("planner", "supervisor")

    # -------------------------------------------------------------------------
    # Supervisor Routing
    # -------------------------------------------------------------------------

    workflow.add_conditional_edges(
        "supervisor",
        supervisor_router,
        {
            "answer": "answer",
            "retriever": "query_rewriter",
            "tool": "answer",  # TODO: Replace with ToolAgent in a future phase.
        },
    )

    # -------------------------------------------------------------------------
    # RAG Pipeline
    # -------------------------------------------------------------------------

    workflow.add_edge("query_rewriter", "retriever")
    workflow.add_edge("retriever", "compression")
    workflow.add_edge("compression", "answer")
    workflow.add_edge("answer", "citation")
    workflow.add_edge("citation", "reflection")

    # -------------------------------------------------------------------------
    # Reflection Routing
    # -------------------------------------------------------------------------

    workflow.add_conditional_edges(
        "reflection",
        reflection_router,
        {
            "retry": "retry",
            "verification": "verification",
            "end": END,
        },
    )

    # -------------------------------------------------------------------------
    # Verification Routing
    # -------------------------------------------------------------------------

    workflow.add_conditional_edges(
        "verification",
        verification_router,
        {
            "retry": "retry",
            "end": END,
        },
    )

    # -------------------------------------------------------------------------
    # Retry Loop
    # -------------------------------------------------------------------------

    workflow.add_edge("retry", "query_rewriter")

    # -------------------------------------------------------------------------
    # Compile and freeze the workflow graph
    # -------------------------------------------------------------------------

    return workflow.compile()


graph = build_workflow()
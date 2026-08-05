from langgraph.graph import START, END, StateGraph

from app.graph.state import GraphState

from app.agents.memory_agent import MemoryAgent
from app.agents.planner_agent import PlannerAgent
from app.agents.supervisor_agent import SupervisorAgent
from app.agents.tool_executor_agent import ToolExecutorAgent
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
tool_executor = ToolExecutorAgent()
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


def tool_executor_node(state: GraphState):
    return tool_executor(state)


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

def reflection_router(state: GraphState):
    """
    Reflection routing.
    """

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

    if (
        needs_retry
        and retry_count < max_retries
    ):
        return "retry"

    return "verification"


def verification_router(state: GraphState):
    """
    Verification routing.
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

    workflow = StateGraph(GraphState)

    # ---------------------------------------------------------------------
    # Register Nodes
    # ---------------------------------------------------------------------

    workflow.add_node(
        "memory",
        memory_node,
    )

    workflow.add_node(
        "planner",
        planner_node,
    )

    workflow.add_node(
        "supervisor",
        supervisor_node,
    )

    workflow.add_node(
        "tool_executor",
        tool_executor_node,
    )

    workflow.add_node(
        "query_rewriter",
        query_rewriter_node,
    )

    workflow.add_node(
        "retriever",
        retriever_node,
    )

    workflow.add_node(
        "compression",
        compression_node,
    )

    workflow.add_node(
        "answer",
        answer_node,
    )

    workflow.add_node(
        "citation",
        citation_node,
    )

    workflow.add_node(
        "reflection",
        reflection_node,
    )

    workflow.add_node(
        "verification",
        verification_node,
    )

    workflow.add_node(
        "retry",
        retry_node,
    )

    # ---------------------------------------------------------------------
    # Entry
    # ---------------------------------------------------------------------

    workflow.add_edge(
        START,
        "memory",
    )

    workflow.add_edge(
        "memory",
        "planner",
    )

    workflow.add_edge(
        "planner",
        "supervisor",
    )

    workflow.add_edge(
        "supervisor",
        "query_rewriter",
    )

    workflow.add_edge(
        "query_rewriter",
        "tool_executor",
    )

    workflow.add_edge(
        "tool_executor",
        "compression",
    )

    # ---------------------------------------------------------------------
    # RAG Pipeline
    # ---------------------------------------------------------------------

    workflow.add_edge(
        "compression",
        "answer",
    )

    workflow.add_edge(
        "answer",
        "citation",
    )

    workflow.add_edge(
        "citation",
        "reflection",
    )

    # ---------------------------------------------------------------------
    # Reflection
    # ---------------------------------------------------------------------

    workflow.add_conditional_edges(
        "reflection",
        reflection_router,
        {
            "retry": "retry",
            "verification": "verification",
        },
    )

    # ---------------------------------------------------------------------
    # Verification
    # ---------------------------------------------------------------------

    workflow.add_conditional_edges(
        "verification",
        verification_router,
        {
            "retry": "retry",
            "end": END,
        },
    )

    # ---------------------------------------------------------------------
    # Retry Loop
    # ---------------------------------------------------------------------

    workflow.add_edge(
        "retry",
        "query_rewriter",
    )

    return workflow.compile()


graph = build_workflow()
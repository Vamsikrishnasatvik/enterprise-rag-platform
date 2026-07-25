from langgraph.graph import START, END, StateGraph

from app.graph.state import GraphState

from app.agents.memory_agent import MemoryAgent
from app.agents.planner_agent import PlannerAgent
from app.agents.supervisor_agent import SupervisorAgent
from app.agents.retriever_agent import RetrieverAgent
from app.agents.compression_agent import CompressionAgent
from app.agents.answer_agent import AnswerAgent
from app.agents.citation_agent import CitationAgent
from app.agents.reflection_agent import ReflectionAgent
from app.agents.verification_agent import VerificationAgent
from app.agents.retry_agent import RetryAgent


# =============================================================================
# Agent Instances
# =============================================================================

memory = MemoryAgent()
planner = PlannerAgent()
supervisor = SupervisorAgent()
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
    return state.get("next_node", "answer")


def reflection_router(state: GraphState):
    """
    Decide whether to:
    - End (non-RAG)
    - Retry retrieval
    - Continue to Verification
    """

    # ---------------------------------------------------------
    # Skip Reflection for non-RAG routes
    # ---------------------------------------------------------

    if state.get("next_node") != "retriever":
        return "end"

    # ---------------------------------------------------------
    # Retry requested by Reflection
    # ---------------------------------------------------------

    if (
        state.get("needs_retry", False)
        and state.get("retry_count", 0)
        < state.get("max_retries", 2)
    ):
        return "retry"

    # ---------------------------------------------------------
    # Reflection passed -> Verify grounding
    # ---------------------------------------------------------

    if state.get("reflection", {}).get("passed", False):
        return "verification"

    # ---------------------------------------------------------
    # Otherwise finish
    # ---------------------------------------------------------

    return "end"


def verification_router(state: GraphState):
    """
    Verification may request another retrieval if
    grounding failed.
    """

    if (
        state.get("retry_required", False)
        and state.get("retry_count", 0)
        < state.get("max_retries", 2)
    ):
        return "retry"

    return "end"


# =============================================================================
# Workflow
# =============================================================================

def build_workflow():

    workflow = StateGraph(GraphState)

    # -------------------------------------------------------------------------
    # Register Nodes
    # -------------------------------------------------------------------------

    workflow.add_node("memory", memory_node)
    workflow.add_node("planner", planner_node)
    workflow.add_node("supervisor", supervisor_node)
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
            "retriever": "retriever",
            "tool": "answer",   # ToolAgent (future)
        },
    )

    # -------------------------------------------------------------------------
    # RAG Pipeline
    # -------------------------------------------------------------------------

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

    workflow.add_edge("retry", "retriever")

    # -------------------------------------------------------------------------
    # Compile Graph
    # -------------------------------------------------------------------------

    return workflow.compile()


graph = build_workflow()
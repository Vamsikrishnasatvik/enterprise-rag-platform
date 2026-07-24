from langgraph.graph import START, END, StateGraph

from app.graph.state import GraphState

from app.agents.memory_agent import MemoryAgent
from app.agents.planner_agent import PlannerAgent
from app.agents.supervisor_agent import SupervisorAgent
from app.agents.retriever_agent import RetrieverAgent
from app.agents.answer_agent import AnswerAgent
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
answer = AnswerAgent()
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


def answer_node(state: GraphState):
    return answer(state)


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
    return state.get("next_node", "answer")


def reflection_router(state: GraphState):
    execution_plan = state.get("execution_plan", {})

    if execution_plan.get("verify", False):
        return "verification"

    return "end"


def verification_router(state: GraphState):
    if state.get("retry_required", False):
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
    workflow.add_node("answer", answer_node)
    workflow.add_node("reflection", reflection_node)
    workflow.add_node("verification", verification_node)
    workflow.add_node("retry", retry_node)

    # -------------------------------------------------------------------------
    # Entry Point
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
            "retriever": "retriever",
            "answer": "answer",
        },
    )

    # -------------------------------------------------------------------------
    # Main Pipeline
    # -------------------------------------------------------------------------

    workflow.add_edge("retriever", "answer")

    workflow.add_edge("answer", "reflection")

    # -------------------------------------------------------------------------
    # Reflection Routing
    # Planner decides whether verification should execute
    # -------------------------------------------------------------------------

    workflow.add_conditional_edges(
        "reflection",
        reflection_router,
        {
            "verification": "verification",
            "end": END,
        },
    )

    # -------------------------------------------------------------------------
    # Verification Routing
    # Verification decides whether retry is needed
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

    return workflow.compile()


graph = build_workflow()
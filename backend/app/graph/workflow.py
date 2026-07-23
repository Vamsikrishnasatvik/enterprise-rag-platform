from langgraph.graph import START, END, StateGraph

from app.graph.state import GraphState
from app.agents.supervisor_agent import SupervisorAgent

supervisor = SupervisorAgent()


def supervisor_node(state: GraphState):
    return supervisor(state)


def build_workflow():
    workflow = StateGraph(GraphState)

    workflow.add_node("supervisor", supervisor_node)

    workflow.add_edge(START, "supervisor")
    workflow.add_edge("supervisor", END)

    return workflow.compile()


graph = build_workflow()
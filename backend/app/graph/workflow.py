from langgraph.graph import StateGraph, START, END

from app.graph.router import (
    verifier_router,
)

from app.graph.state import GraphState
from app.graph.nodes import (
    query_node,
    planner_node,
    retriever_node,
    verifier_node,
    answer_node,
)


def create_workflow():

    workflow = StateGraph(GraphState)

    workflow.add_node(
        "query",
        query_node,
    )

    workflow.add_node(
        "planner",
        planner_node,
    )

    workflow.add_node(
        "retriever",
        retriever_node,
    )

    workflow.add_node(
        "answer",
        answer_node,
    )

    workflow.add_node(
        "verifier",
        verifier_node,
    )

    workflow.add_edge(
        START,
        "query",
    )

    workflow.add_edge(
        "query",
        "planner",
    )

    workflow.add_edge(
        "planner",
        "retriever",
    )

    workflow.add_edge(
        "retriever",
        "verifier",
    )

    workflow.add_conditional_edges(
        "verifier",
        verifier_router,
        {
            "retriever": "retriever",
            "answer": "answer",
        },
    )

    workflow.add_edge(
        "answer",
        END,
    )

    return workflow
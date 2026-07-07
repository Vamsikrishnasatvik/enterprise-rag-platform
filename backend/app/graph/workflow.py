from langgraph.graph import StateGraph, START, END

from app.graph.router import (
    verifier_router,
)

from app.graph.state import GraphState
from app.graph.nodes import (
    query_node,
    planner_node,
    retriever_node,
    reranker_node,
    verifier_node,
    evidence_node, 
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
        "reranker",
        reranker_node,
    )

    workflow.add_node(
        "evidence",
        evidence_node,
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
        "reranker",
    )

    workflow.add_edge(
        "reranker",
        "verifier",
    )

    workflow.add_conditional_edges(
        "verifier",
        verifier_router,
        {
            "retriever": "retriever",
            "evidence": "evidence",
        },
    )

    workflow.add_edge(
        "evidence",
        "answer",
    )

    workflow.add_edge(
        "answer",
        END,
    )

    return workflow
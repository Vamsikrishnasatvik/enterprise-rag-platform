from langgraph.graph import StateGraph, START, END

from app.graph.state import GraphState
from app.graph.nodes import (
    query_node,
    retriever_node,
    answer_node,
)


def create_workflow():

    workflow = StateGraph(GraphState)

    workflow.add_node(
        "query",
        query_node,
    )

    workflow.add_node(
        "retriever",
        retriever_node,
    )

    workflow.add_node(
        "answer",
        answer_node,
    )

    workflow.add_edge(
        START,
        "query",
    )

    workflow.add_edge(
        "query",
        "retriever",
    )

    workflow.add_edge(
        "retriever",
        "answer",
    )

    workflow.add_edge(
        "answer",
        END,
    )

    return workflow
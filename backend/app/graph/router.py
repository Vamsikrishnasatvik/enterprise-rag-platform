from app.graph.state import GraphState


def verifier_router(
    state: GraphState,
) -> str:

    if state["needs_retry"]:
        return "retriever"

    return "answer"
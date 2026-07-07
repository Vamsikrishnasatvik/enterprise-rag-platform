from app.graph.state import GraphState


def verifier_router(
    state: GraphState,
) -> str:
    """
    Route after verification.

    Retry retrieval if confidence is low.
    Otherwise continue to the EvidenceAgent.
    """

    if state["needs_retry"]:
        return "retriever"

    return "evidence"
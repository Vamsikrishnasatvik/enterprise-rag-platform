from app.agents.retriever_agent import RetrieverAgent
from app.services import retrieval_orchestrator


def test_retriever_agent(graph_state, monkeypatch):

    def fake_retrieve_documents(**kwargs):
        return [
            {
                "chunk_id": 1,
                "document_id": 1,
                "content": (
                    "The HR Leave Policy allows employees to take annual leave, "
                    "sick leave, maternity leave, paternity leave, and emergency leave "
                    "according to company guidelines and approval workflows."
                ),
                "score": 0.95,
            }
        ]

    monkeypatch.setattr(
        retrieval_orchestrator,
        "retrieve_documents",
        fake_retrieve_documents,
    )

    agent = RetrieverAgent()

    result = agent.run(graph_state)

    assert isinstance(result, dict)

    assert "retrieved_chunks" in result

    assert isinstance(
        result["retrieved_chunks"],
        list,
    )

    assert len(
        result["retrieved_chunks"]
    ) > 0

    assert len(
        result["execution_trace"]
    ) == 1

    trace = result["execution_trace"][0]

    assert trace["agent"] == "RetrieverAgent"
    assert trace["status"] == "completed"
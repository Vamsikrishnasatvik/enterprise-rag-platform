from app.agents.retriever_agent import RetrieverAgent


def test_retriever_agent(graph_state):

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
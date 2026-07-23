from app.graph.workflow import graph


def test_supervisor_graph():
    state = {
        "question": "What is RAG?"
    }

    result = graph.invoke(state)

    assert "execution_plan" in result
    assert result["execution_plan"]["retrieve"] is True
from app.agents.planner_agent import PlannerAgent


def test_planner_agent(graph_state):

    planner = PlannerAgent()

    result = planner.run(graph_state)

    assert isinstance(result, dict)
    assert "execution_plan" in result
    assert "retrieval_strategy" in result
    assert "search_limit" in result
    assert result["search_limit"] > 0

    assert result["retrieval_strategy"] in [
        "semantic",
        "bm25",
        "hybrid",
        "multi_query",
    ]

    assert len(result["execution_trace"]) == 1
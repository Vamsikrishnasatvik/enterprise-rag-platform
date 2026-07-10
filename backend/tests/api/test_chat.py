def test_chat_query(
    client,
    auth_headers,
):

    response = client.post(
        "/chat/query",
        headers=auth_headers,
        json={
            "query": "What is the HR Leave Policy?",
            "conversation_id": None,
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert "answer" in body
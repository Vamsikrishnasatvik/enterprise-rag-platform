def test_login(client):

    response = client.post(
        "/auth/login",
        json={
            "email": "admin@test.com",
            "password": "password123",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert "access_token" in body
    assert body["token_type"] == "bearer"
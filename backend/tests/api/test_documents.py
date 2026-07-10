import tempfile

from fastapi.testclient import TestClient


def test_upload_document(
    client,
    auth_headers,
):

    with tempfile.NamedTemporaryFile(
        suffix=".txt",
        delete=False,
    ) as tmp:

        tmp.write(
            b"This is a pytest document."
        )

        tmp.flush()

        with open(
            tmp.name,
            "rb",
        ) as f:

            response = client.post(
                "/documents/upload",
                headers=auth_headers,
                files={
                    "file": (
                        "pytest.txt",
                        f,
                        "text/plain",
                    )
                },
            )

    assert response.status_code == 200

    body = response.json()

    assert "document_id" in body

    assert "status" in body
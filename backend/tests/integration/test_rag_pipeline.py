import tempfile
import time


def wait_for_job(
    client,
    auth_headers,
    job_id,
    timeout=60,
):
    start = time.time()

    while time.time() - start < timeout:

        response = client.get(
            f"/ingestion/{job_id}",
            headers=auth_headers,
        )

        assert response.status_code == 200

        body = response.json()

        if body["status"] == "COMPLETED":
            return body

        if body["status"] == "FAILED":
            raise AssertionError(
                body["error_message"]
            )

        time.sleep(1)

    raise TimeoutError(
        "Ingestion timeout."
    )


def test_rag_pipeline(
    client,
    auth_headers,
):

    with tempfile.NamedTemporaryFile(
        suffix=".txt",
        delete=False,
    ) as tmp:

        tmp.write(
            b"""
            HR Leave Policy

            Employees receive 20 annual leave days.

            Sick leave is 10 days.

            """
        )

        tmp.flush()

        with open(
            tmp.name,
            "rb",
        ) as f:

            upload = client.post(
                "/documents/upload",
                headers=auth_headers,
                files={
                    "file": (
                        "policy.txt",
                        f,
                        "text/plain",
                    )
                },
            )

    assert upload.status_code == 200

    upload_body = upload.json()

    job_id = upload_body["job_id"]

    wait_for_job(
        client,
        auth_headers,
        job_id,
    )

    response = client.post(
        "/chat/query",
        headers=auth_headers,
        json={
            "query": "How many annual leave days do employees receive?",
            "conversation_id": None,
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert "answer" in body

    assert len(body["answer"]) > 0
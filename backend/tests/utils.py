import time


def wait_for_ingestion(
    client,
    headers,
    job_id,
    timeout=60,
):

    start = time.time()

    while time.time() - start < timeout:

        response = client.get(
            f"/ingestion/{job_id}",
            headers=headers,
        )

        assert response.status_code == 200

        body = response.json()

        status = body["status"]

        if status == "COMPLETED":
            return body

        if status == "FAILED":
            raise AssertionError(
                body["error_message"]
            )

        time.sleep(1)

    raise TimeoutError(
        "Ingestion timeout"
    )
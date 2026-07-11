import pytest

from app.db.session import SessionLocal

from fastapi.testclient import TestClient

from app.main import app

@pytest.fixture(scope="session")
def client():
    """
    Shared FastAPI TestClient.
    """

    with TestClient(app) as client:
        yield client


@pytest.fixture
def auth_headers(client):
    """
    Returns authentication headers for API tests.
    """

    response = client.post(
        "/auth/login",
        json={
            "email": "admin@test.com",
            "password": "password123",
        },
    )

    assert response.status_code == 200

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }

# ---------------------------------------------------------
# Database Session
# ---------------------------------------------------------

@pytest.fixture(scope="function")
def db_session():
    """
    Provides a database session for tests.

    Every test gets a fresh SQLAlchemy session.
    """

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# ---------------------------------------------------------
# Default Graph State
# ---------------------------------------------------------

@pytest.fixture
def graph_state():

    return {
        "tenant_id": 1,
        "question": "Explain the HR Leave Policy",
        "rewritten_query": "",
        "intent": None,
        "metadata_filters": {},
        "conversation_summary": "",
        "chat_history": [],
        "execution_plan": {
            "search_strategy": "semantic",
            "retrieval_count": 5,
        },
        "retrieved_chunks": [],
        "execution_trace": [],
        "search_limit": 5,
        "retrieval_strategy": "semantic",
        "retrieval_attempts": 0,
    }


# ---------------------------------------------------------
# Sample Metadata
# ---------------------------------------------------------

@pytest.fixture
def sample_metadata():

    return {
        "department": "Human Resources",
        "document_type": "Policy",
        "version": "2.0",
        "effective_date": "2026-01-01",
        "owner": "HR Team",
        "classification": "Internal",
        "tags": [
            "leave",
            "policy",
        ],
    }


# ---------------------------------------------------------
# Sample Chunks
# ---------------------------------------------------------

@pytest.fixture
def sample_chunks():

    return [
        {
            "chunk_id": 1,
            "content": "HR Leave Policy...",
            "score": 0.95,
        },
        {
            "chunk_id": 2,
            "content": "Annual leave rules...",
            "score": 0.90,
        },
    ]

# ---------------------------------------------------------
# Mock LLM
# ---------------------------------------------------------

import pytest

from app.services import llm_service


@pytest.fixture(autouse=True)
def mock_llm(monkeypatch):
    """
    Mock Ollama for all tests.
    """

    def fake_generate_text(
        prompt: str,
        temperature: float = 0.1,
    ):

        prompt_lower = prompt.lower()

        # Multi-query generation prompt
        if (
            "enterprise search expert" in prompt_lower
            or "alternative search" in prompt_lower
        ):
            return """Explain the HR Leave Policy
Employee leave policy
Annual leave rules
Paid leave policy"""

        return "Test response"

    monkeypatch.setattr(
        llm_service,
        "generate_text",
        fake_generate_text,
    )
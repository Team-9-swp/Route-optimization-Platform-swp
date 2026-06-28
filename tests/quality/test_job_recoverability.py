"""QRT-RE-01 — Job recoverability.

Verifies that submitted jobs remain retrievable after the application is
recreated using the same persistent database.
"""

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient

from app.db import dispose_engine
from app.main import create_app
from app.repository import JobRepository


@pytest_asyncio.fixture(autouse=True)
async def clean_repository():
    repo = JobRepository()
    await repo.clear_all()
    await dispose_engine()
    yield
    repo = JobRepository()
    await repo.clear_all()
    await dispose_engine()


@pytest.fixture
def client():
    with TestClient(create_app(init_db_on_startup=True)) as c:
        yield c


@pytest.mark.quality
@pytest.mark.integration
def test_qrt_re_01_a_completed_job_survives_store_recreation(client):
    """A job submitted through the API must survive an application restart."""
    payload = {"orders": []}
    response = client.post("/solve?seed=42&time_limit=2", json=payload)
    assert response.status_code == 202
    body = response.json()
    job_id = body["job_id"]
    assert body["status"] == "pending"

    new_client = TestClient(create_app(init_db_on_startup=True))
    with new_client:
        fetched = new_client.get(f"/jobs/{job_id}")

    assert fetched.status_code == 200
    data = fetched.json()
    assert data["job_id"] == job_id
    assert data["input_data"] == payload
    assert data["seed"] == 42
    assert data["status"] in {"pending", "running", "completed", "failed"}


@pytest.mark.quality
@pytest.mark.integration
def test_qrt_re_01_b_api_retrieval_after_application_recreation(client):
    """The same behaviour verified through the public GET /jobs/{job_id} endpoint."""
    payload = {"orders": []}
    response = client.post("/solve?seed=7&name=recoverability-test", json=payload)
    assert response.status_code == 202
    body = response.json()
    job_id = body["job_id"]

    new_client = TestClient(create_app(init_db_on_startup=True))
    with new_client:
        fetched = new_client.get(f"/jobs/{job_id}")

    assert fetched.status_code == 200
    data = fetched.json()
    assert data["job_id"] == job_id
    assert data["name"] == "recoverability-test"
    assert data["input_data"] == payload

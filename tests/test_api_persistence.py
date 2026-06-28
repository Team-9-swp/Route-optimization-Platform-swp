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


@pytest.mark.integration
def test_submitted_job_survives_service_restart(client):
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

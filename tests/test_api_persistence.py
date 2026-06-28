import pytest
import pytest_asyncio
from fastapi.testclient import TestClient

from app.main import create_app
from app.repository import JobRepository


@pytest_asyncio.fixture(autouse=True)
async def clean_repository():
    repo = JobRepository()
    await repo.clear_all()
    yield
    await repo.clear_all()


@pytest.fixture
def client():
    with TestClient(create_app(init_db_on_startup=True)) as c:
        yield c


@pytest.mark.integration
def test_submitted_job_survives_service_restart(client):
    response = client.post("/solve?seed=42&time_limit=2", json={"orders": []})
    assert response.status_code == 202
    job_id = response.json()["job_id"]

    new_client = TestClient(create_app(init_db_on_startup=True))
    with new_client:
        fetched = new_client.get(f"/jobs/{job_id}")
    assert fetched.status_code == 200
    assert fetched.json()["job_id"] == job_id

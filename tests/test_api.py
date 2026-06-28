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
    return TestClient(create_app())


@pytest.mark.integration
@pytest.mark.asyncio
async def test_post_solve_returns_202(client):
    response = client.post("/solve?seed=42&time_limit=2", json={"orders": []})
    assert response.status_code == 202
    data = response.json()
    assert data["status"] == "pending"
    assert "max_restarts" not in data


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_job_not_found(client):
    response = client.get("/jobs/nonexistent")
    assert response.status_code == 404


@pytest.mark.integration
@pytest.mark.asyncio
async def test_list_jobs(client):
    repo = JobRepository()
    await repo.create_job({"orders": []}, seed=1)
    response = client.get("/jobs")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1


@pytest.mark.integration
@pytest.mark.asyncio
async def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

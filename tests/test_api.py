import json
from pathlib import Path

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient

from app.main import create_app
from app.repository import JobRepository


@pytest.fixture
def client():
    with TestClient(create_app(init_db_on_startup=False)) as c:
        yield c


@pytest_asyncio.fixture
async def clean_repository():
    repo = JobRepository()
    await repo.clear_all()
    yield
    await repo.clear_all()


@pytest.fixture
def integration_client(clean_repository):
    with TestClient(create_app(init_db_on_startup=True)) as c:
        yield c


@pytest.mark.integration
async def test_post_solve_returns_202(integration_client):
    response = integration_client.post("/solve?seed=1", json={"orders": []})
    assert response.status_code == 202
    data = response.json()
    assert "job_id" in data
    assert data["status"] == "pending"


@pytest.mark.integration
def test_post_solve_default_seed(integration_client):
    response = integration_client.post("/solve", json={"orders": []})
    assert response.status_code == 202
    data = response.json()
    assert "job_id" in data
    assert data["status"] == "pending"


@pytest.mark.integration
def test_post_solve_with_name_and_auto_validate(integration_client):
    response = integration_client.post(
        "/solve?seed=1&name=my-job&auto_validate=true",
        json={"orders": []},
    )
    assert response.status_code == 202
    data = response.json()
    assert data["name"] == "my-job"
    assert data["status"] == "pending"


@pytest.mark.integration
def test_get_jobs_list(integration_client):
    integration_client.post("/solve?seed=1&name=a", json={"orders": []})
    integration_client.post("/solve?seed=1&name=b", json={"orders": []})
    response = integration_client.get("/jobs?page=1&page_size=10")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2


@pytest.mark.integration
def test_get_job_not_found(integration_client):
    response = integration_client.get("/jobs/does-not-exist")
    assert response.status_code == 404


@pytest.mark.integration
def test_post_validate(integration_client):
    root = Path(__file__).resolve().parent.parent
    instance = json.loads((root / "test_cases" / "t1.json").read_text())
    solution = json.loads((root / "test_cases" / "sol_t1.json").read_text())
    response = integration_client.post("/validate", json={"instance": instance, "solution": solution})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["passed"], bool)
    assert "violations" in data


@pytest.mark.integration
def test_cors_preflight(integration_client):
    response = integration_client.options(
        "/solve",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "POST",
        },
    )
    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.api import service
from app.main import app
from app.store import JobStore


@pytest.fixture(autouse=True)
def fresh_store():
    service._store = JobStore()


@pytest.fixture
def client():
    return TestClient(app)


def test_post_solve_returns_202(client):
    response = client.post("/solve?seed=1", json={"orders": []})
    assert response.status_code == 202
    data = response.json()
    assert "job_id" in data
    assert data["status"] == "pending"


def test_post_solve_default_seed(client):
    response = client.post("/solve", json={"orders": []})
    assert response.status_code == 202
    data = response.json()
    assert "job_id" in data
    assert data["status"] == "pending"


def test_post_solve_with_name_and_auto_validate(client):
    response = client.post(
        "/solve?seed=1&name=my-job&auto_validate=true",
        json={"orders": []},
    )
    assert response.status_code == 202
    data = response.json()
    assert data["name"] == "my-job"
    assert data["status"] == "pending"


def test_get_jobs_list(client):
    client.post("/solve?seed=1&name=a", json={"orders": []})
    client.post("/solve?seed=1&name=b", json={"orders": []})
    response = client.get("/jobs?page=1&page_size=10")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2


def test_get_job_not_found(client):
    response = client.get("/jobs/does-not-exist")
    assert response.status_code == 404


def test_post_validate(client):
    root = Path(__file__).resolve().parent.parent
    instance = json.loads((root / "test_cases" / "t1.json").read_text())
    solution = json.loads((root / "test_cases" / "sol_t1.json").read_text())
    response = client.post(
        "/validate", json={"instance": instance, "solution": solution}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["passed"], bool)
    assert "violations" in data


def test_cors_preflight(client):
    response = client.options(
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

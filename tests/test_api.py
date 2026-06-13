import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_post_solve_returns_202(client):
    response = client.post("/solve", json={"instance": {"orders": []}, "seed": 1})
    assert response.status_code == 202
    data = response.json()
    assert "job_id" in data
    assert data["status"] == "pending"


def test_get_job_not_found(client):
    response = client.get("/jobs/does-not-exist")
    assert response.status_code == 404


def test_post_solve_invalid_body(client):
    response = client.post("/solve", json={})
    assert response.status_code == 422

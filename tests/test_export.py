"""Tests for the solution export endpoint (no database required)."""

from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient

from app.main import create_app
from app.schemas import JobResponse, JobStatus


@pytest.fixture
def client():
    with TestClient(create_app(init_db_on_startup=False)) as c:
        yield c


def _completed_job(job_id: str = "test-job", result: dict | None = None) -> JobResponse:
    return JobResponse(
        job_id=job_id,
        status=JobStatus.COMPLETED,
        created_at=datetime.now(timezone.utc),
        started_at=datetime.now(timezone.utc),
        finished_at=datetime.now(timezone.utc),
        result=result or {"vehicles": [], "loaders": [], "unserved_optional": []},
        objective_value=100.0,
    )


def test_export_valid_solution(client, monkeypatch):
    result = {
        "vehicles": [{"id": 1, "route": [0, 1, 0], "time": [10.0]}],
        "loaders": [],
        "unserved_optional": [],
    }

    async def mock_get_job(job_id):
        return _completed_job(job_id, result)

    monkeypatch.setattr("app.api.service.get_job", mock_get_job)

    response = client.get("/jobs/test-job/export")
    assert response.status_code == 200
    data = response.json()
    assert "vehicles" in data
    assert "loaders" in data
    assert data["vehicles"] == result["vehicles"]


def test_export_schema_matches_validator(client, monkeypatch):
    result = {
        "vehicles": [{"id": 1, "route": [0, 1, 0], "time": [10.0]}],
        "loaders": [],
        "unserved_optional": [],
    }

    async def mock_get_job(job_id):
        return _completed_job(job_id, result)

    monkeypatch.setattr("app.api.service.get_job", mock_get_job)

    export_resp = client.get("/jobs/test-job/export")
    assert export_resp.status_code == 200
    export_data = export_resp.json()

    validation_resp = client.post(
        "/validate",
        json={
            "instance": {
                "vehicle_capacity": 100,
                "vehicle_speed": 1,
                "loader_speed": 1,
                "vehicle_shift_size": 1000,
                "loader_shift_size": 1000,
                "depot": {"x": 0, "y": 0, "load_time": 0},
                "orders": [
                    {
                        "id": 1, "x": 3, "y": 4, "volume": 10,
                        "time_window": [0, 100], "vehicle_service_time": 5,
                        "loader_cnt": 0, "loader_service_time": 0, "optional": 0,
                    },
                ],
                "weights": {
                    "vehicle_salary": 1, "fuel_cost": 1, "loader_salary": 1,
                    "loader_work": 1, "optional_order_penalty": 1,
                },
            },
            "solution": export_data,
        },
    )
    assert validation_resp.status_code == 200
    validation_data = validation_resp.json()
    assert isinstance(validation_data["passed"], bool)


def test_export_404_for_missing_job(client, monkeypatch):
    async def mock_get_job(job_id):
        return None

    monkeypatch.setattr("app.api.service.get_job", mock_get_job)

    response = client.get("/jobs/nonexistent/export")
    assert response.status_code == 404


def test_export_includes_loader_routes(client, monkeypatch):
    result = {
        "vehicles": [{"id": 1, "route": [0, 1, 0], "time": [10.0]}],
        "loaders": [{"id": 1, "route": [1]}],
        "unserved_optional": [],
    }

    async def mock_get_job(job_id):
        return _completed_job(job_id, result)

    monkeypatch.setattr("app.api.service.get_job", mock_get_job)

    response = client.get("/jobs/test-job/export")
    assert response.status_code == 200
    data = response.json()
    assert len(data["loaders"]) == 1
    assert data["loaders"][0]["id"] == 1
    assert data["loaders"][0]["route"] == [1]


def test_export_pending_job_returns_400(client, monkeypatch):
    async def mock_get_job(job_id):
        return JobResponse(
            job_id=job_id,
            status=JobStatus.PENDING,
            created_at=datetime.now(timezone.utc),
        )

    monkeypatch.setattr("app.api.service.get_job", mock_get_job)

    response = client.get("/jobs/pending-job/export")
    assert response.status_code == 400

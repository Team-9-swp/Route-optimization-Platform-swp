import json
from datetime import datetime, timezone
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import create_app
from app.schemas import (
    JobListResponse,
    JobResponse,
    JobStatus,
    SolveResponse,
)


@pytest.fixture
def client():
    with TestClient(create_app(init_db_on_startup=False)) as c:
        yield c


def test_post_solve_returns_202(client, monkeypatch):
    async def mock_submit_job(instance, seed, name=None, auto_validate=False, time_limit=None):
        return SolveResponse(
            job_id="test-job-id",
            status=JobStatus.PENDING,
            created_at=datetime.now(timezone.utc),
        )

    monkeypatch.setattr("app.api.service.submit_job", mock_submit_job)

    response = client.post("/solve?seed=1", json={"orders": []})
    assert response.status_code == 202
    data = response.json()
    assert "job_id" in data
    assert data["status"] == "pending"


def test_post_solve_default_seed(client, monkeypatch):
    async def mock_submit_job(instance, seed, name=None, auto_validate=False, time_limit=None):
        return SolveResponse(
            job_id="test-job-id",
            status=JobStatus.PENDING,
            created_at=datetime.now(timezone.utc),
        )

    monkeypatch.setattr("app.api.service.submit_job", mock_submit_job)

    response = client.post("/solve", json={"orders": []})
    assert response.status_code == 202
    data = response.json()
    assert "job_id" in data
    assert data["status"] == "pending"


def test_post_solve_with_name_and_auto_validate(client, monkeypatch):
    async def mock_submit_job(instance, seed, name=None, auto_validate=False, time_limit=None):
        return SolveResponse(
            job_id="test-job-id",
            status=JobStatus.PENDING,
            created_at=datetime.now(timezone.utc),
            name=name,
        )

    monkeypatch.setattr("app.api.service.submit_job", mock_submit_job)

    response = client.post(
        "/solve?seed=1&name=my-job&auto_validate=true",
        json={"orders": []},
    )
    assert response.status_code == 202
    data = response.json()
    assert data["name"] == "my-job"
    assert data["status"] == "pending"


def test_get_jobs_list(client, monkeypatch):
    async def mock_list_jobs(page=1, page_size=25, sort_desc=True):
        job = JobResponse(
            job_id="test-job",
            status=JobStatus.PENDING,
            created_at=datetime.now(timezone.utc),
        )
        return JobListResponse(
            items=[job, job],
            total=2,
            page=page,
            page_size=page_size,
        )

    monkeypatch.setattr("app.api.service.list_jobs", mock_list_jobs)

    response = client.get("/jobs?page=1&page_size=10")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2


def test_get_job_not_found(client, monkeypatch):
    async def mock_get_job(job_id):
        return None

    monkeypatch.setattr("app.api.service.get_job", mock_get_job)

    response = client.get("/jobs/does-not-exist")
    assert response.status_code == 404


def test_post_validate(client):
    root = Path(__file__).resolve().parent.parent
    instance = (root / "test_cases" / "t1.json").read_bytes()
    solution = (root / "test_cases" / "sol_t1.json").read_bytes()
    response = client.post(
        "/validate",
        json={"instance": json.loads(instance), "solution": json.loads(solution)},
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


def test_api_docs_accessible(client):
    response = client.get("/docs")
    assert response.status_code == 200
    assert "swagger" in response.text.lower() or "openapi" in response.text.lower()


def test_job_detail_includes_loader_balance(client, monkeypatch):
    result = {
        "vehicles": [{"id": 1, "route": [0, 1, 0], "time": [10.0]}],
        "loaders": [{"id": 10, "route": [1]}],
        "unserved_optional": [],
    }

    async def mock_get_job(job_id):
        return JobResponse(
            job_id=job_id,
            status=JobStatus.COMPLETED,
            created_at=datetime.now(timezone.utc),
            started_at=datetime.now(timezone.utc),
            finished_at=datetime.now(timezone.utc),
            result=result,
            objective_value=100.0,
        )

    monkeypatch.setattr("app.api.service.get_job", mock_get_job)

    response = client.get("/jobs/test-job-loaders")
    assert response.status_code == 200
    data = response.json()
    assert "result" in data
    assert data["result"]["loaders"] == result["loaders"]


def test_job_detail_gantt_data_structure(client, monkeypatch):
    result = {
        "vehicles": [
            {"id": 1, "route": [0, 1, 0], "time": [10.0]},
            {"id": 2, "route": [0, 2, 0], "time": [15.0]},
        ],
        "loaders": [],
        "unserved_optional": [],
    }

    async def mock_get_job(job_id):
        return JobResponse(
            job_id=job_id,
            status=JobStatus.COMPLETED,
            created_at=datetime.now(timezone.utc),
            started_at=datetime.now(timezone.utc),
            finished_at=datetime.now(timezone.utc),
            result=result,
            objective_value=100.0,
        )

    monkeypatch.setattr("app.api.service.get_job", mock_get_job)

    response = client.get("/jobs/test-job-gantt")
    assert response.status_code == 200
    data = response.json()
    vehicles = data["result"]["vehicles"]
    assert len(vehicles) == 2
    for v in vehicles:
        assert "id" in v
        assert "route" in v
        if v.get("time"):
            assert isinstance(v["time"], list)
            assert all(isinstance(t, (int, float)) for t in v["time"])


def test_job_detail_includes_unserved_optional_field(client, monkeypatch):
    async def mock_get_job(job_id):
        return JobResponse(
            job_id=job_id,
            status=JobStatus.COMPLETED,
            created_at=datetime.now(timezone.utc),
            started_at=datetime.now(timezone.utc),
            finished_at=datetime.now(timezone.utc),
            result={
                "vehicles": [{"id": 1, "route": [0, 1, 0], "time": [10.0]}],
                "loaders": [],
                "unserved_optional": [99],
            },
            objective_value=100.0,
            unserved_optional=[99],
        )

    monkeypatch.setattr("app.api.service.get_job", mock_get_job)

    response = client.get("/jobs/test-job-optional")
    assert response.status_code == 200
    data = response.json()
    assert "unserved_optional" in data
    assert data["unserved_optional"] == [99]

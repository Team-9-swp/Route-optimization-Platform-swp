"""QRT-SE-01 - safe error confidentiality."""

import time

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient

from app.db import dispose_engine
from app.main import create_app
from app.repository import JobRepository

FORBIDDEN_PATTERNS = [
    "Traceback (most recent call last)",
    '.py", line',
    "/app/",
    "site-packages",
    "SECRET_QRT_VALUE",
    "C:/internal",
    "c:/internal",
]


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


def _assert_no_forbidden_leaks(text: str) -> None:
    lowered = text.lower()
    for pattern in FORBIDDEN_PATTERNS:
        assert pattern.lower() not in lowered, f"Forbidden pattern leaked: {pattern!r}"


def _wait_for_terminal_job(client: TestClient, job_id: str) -> dict:
    latest: dict = {}
    for _ in range(50):
        response = client.get(f"/jobs/{job_id}")
        assert response.status_code == 200
        latest = response.json()
        if latest["status"] in {"completed", "failed"}:
            return latest
        time.sleep(0.1)
    pytest.fail(f"Job {job_id} did not reach a terminal state. Latest: {latest}")


@pytest.mark.qrt
@pytest.mark.quality
@pytest.mark.integration
def test_qrt_se_01_solver_failure_produces_safe_job_error(client, monkeypatch):
    def _raising_solve(*args, **kwargs):
        raise RuntimeError(
            "SECRET_QRT_VALUE Traceback (most recent call last):\n"
            '  File "/app/internal/solver.py", line 99\n'
            '  File "C:/internal/private.py", line 42\n'
            "internal crash"
        )

    monkeypatch.setattr("app.runner._solve_sync", _raising_solve)

    response = client.post("/solve?seed=1&time_limit=2", json={"orders": []})
    assert response.status_code == 202
    job_id = response.json()["job_id"]

    data = _wait_for_terminal_job(client, job_id)

    assert data["status"] == "failed"
    assert data.get("error")
    _assert_no_forbidden_leaks(data["error"])
    assert "internal crash" not in data["error"]


@pytest.mark.qrt
@pytest.mark.quality
@pytest.mark.integration
def test_qrt_se_01_api_response_does_not_expose_internal_details(client, monkeypatch):
    def _raising_solve(*args, **kwargs):
        raise ValueError(
            'SECRET_QRT_VALUE /app/solver.py", line 42 '
            "site-packages traceback-like internals"
        )

    monkeypatch.setattr("app.runner._solve_sync", _raising_solve)

    response = client.post("/solve?seed=1&time_limit=2", json={"orders": []})
    assert response.status_code == 202
    job_id = response.json()["job_id"]

    data = _wait_for_terminal_job(client, job_id)
    fetched = client.get(f"/jobs/{job_id}")

    assert data["status"] == "failed"
    _assert_no_forbidden_leaks(response.text)
    _assert_no_forbidden_leaks(fetched.text)
    assert data.get("error")

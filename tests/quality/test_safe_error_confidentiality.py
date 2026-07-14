"""QRT-SE-01 — Safe error confidentiality.

Verifies that solver failures are reported through the API with a controlled,
user-safe message and do not leak stack traces, file paths, or secrets.
"""

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient

from app.db import dispose_engine
from app.main import create_app
from app.repository import JobRepository

pytestmark = [pytest.mark.qrt, pytest.mark.quality]


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


FORBIDDEN_PATTERNS = [
    "Traceback (most recent call last)",
    '.py", line',
    "/app/",
    "site-packages",
    "SECRET_QRT_VALUE",
    "c:/swp",
    "C:/swp",
]


def _assert_no_forbidden_leaks(text: str) -> None:
    lowered = text.lower()
    for pattern in FORBIDDEN_PATTERNS:
        assert (
            pattern.lower() not in lowered
        ), f"Forbidden pattern leaked in response: {pattern!r}"


@pytest.mark.integration
def test_qrt_se_01_a_solver_failure_produces_safe_job_error(client, monkeypatch):
    """A controlled solver failure must store only a safe error message."""

    def _raising_solve(*args, **kwargs):
        raise ValueError('SECRET_QRT_VALUE /app/solver.py", line 42 internal crash')

    monkeypatch.setattr(
        "app.runner._solve_sync",
        _raising_solve,
    )

    payload = {"orders": []}
    response = client.post("/solve?seed=1&time_limit=2", json=payload)
    assert response.status_code == 202
    job_id = response.json()["job_id"]

    # Wait for the runner background task to record the failure.
    import time

    for _ in range(50):
        fetched = client.get(f"/jobs/{job_id}")
        data = fetched.json()
        if data["status"] in {"failed", "completed"}:
            break
        time.sleep(0.1)

    assert data["status"] == "failed"
    error_text = data.get("error", "")
    assert error_text
    _assert_no_forbidden_leaks(error_text)
    assert (
        "internal crash" not in error_text
    ), "Original exception message must not be exposed"


@pytest.mark.integration
def test_qrt_se_01_b_api_response_does_not_expose_internal_details(client, monkeypatch):
    """The public API response must not contain traceback or secret patterns."""

    def _raising_solve(*args, **kwargs):
        raise RuntimeError(
            "SECRET_QRT_VALUE Traceback (most recent call last):\n"
            '  File "/app/src/solver.py", line 99\n internal'
        )

    monkeypatch.setattr(
        "app.runner._solve_sync",
        _raising_solve,
    )

    payload = {"orders": []}
    response = client.post("/solve?seed=1&time_limit=2", json=payload)
    assert response.status_code == 202
    job_id = response.json()["job_id"]

    import time

    for _ in range(50):
        fetched = client.get(f"/jobs/{job_id}")
        data = fetched.json()
        if data["status"] in {"failed", "completed"}:
            break
        time.sleep(0.1)

    assert data["status"] == "failed"
    _assert_no_forbidden_leaks(response.text)
    _assert_no_forbidden_leaks(fetched.text)
    assert data.get("error")

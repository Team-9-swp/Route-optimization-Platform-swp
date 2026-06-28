"""QRT-PE-01 - solver time behaviour."""

import asyncio
import json
import time
from pathlib import Path

import httpx
import pytest

from app.main import app

ROOT = Path(__file__).resolve().parent.parent.parent
FIXTURE = ROOT / "test_cases" / "t1.json"
PERFORMANCE_THRESHOLD_SECONDS = 900


@pytest.fixture(scope="module")
def instance() -> dict:
    assert FIXTURE.exists(), f"Required committed QRT fixture is missing: {FIXTURE}"
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


async def _wait_for_terminal_job(
    client: httpx.AsyncClient, job_id: str, timeout_s: float
) -> dict:
    start = time.monotonic()
    latest: dict = {}
    while time.monotonic() - start <= timeout_s:
        response = await client.get(f"/jobs/{job_id}")
        assert response.status_code == 200
        latest = response.json()
        if latest["status"] in {"completed", "failed"}:
            return latest
        await asyncio.sleep(1)
    pytest.fail(
        f"Job {job_id} did not reach a terminal state within {timeout_s}s. Latest: {latest}"
    )


@pytest.mark.qrt
@pytest.mark.quality
@pytest.mark.integration
@pytest.mark.asyncio
async def test_qrt_pe_01_fixed_benchmark_completes_within_900_seconds(instance):
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        start = time.monotonic()
        response = await client.post(
            "/solve?seed=42&time_limit=60&auto_validate=true",
            json=instance,
        )
        assert response.status_code == 202
        job_id = response.json()["job_id"]
        job_data = await _wait_for_terminal_job(
            client,
            job_id,
            timeout_s=PERFORMANCE_THRESHOLD_SECONDS,
        )
        elapsed = time.monotonic() - start

    assert elapsed <= PERFORMANCE_THRESHOLD_SECONDS, (
        f"Fixed QRT benchmark took {elapsed:.2f}s, threshold is "
        f"{PERFORMANCE_THRESHOLD_SECONDS}s"
    )
    assert job_data["status"] == "completed", (
        f"Fixed QRT benchmark reached {job_data.get('status')} instead of completed: "
        f"{job_data.get('error')}"
    )
    assert job_data["validation_status"] == "passed"
    assert job_data["validation_report"]["passed"] is True
    assert job_data["validation_report"]["report"]["total_violations"] == 0


@pytest.mark.qrt
@pytest.mark.quality
@pytest.mark.integration
@pytest.mark.asyncio
async def test_qrt_pe_01_configured_time_limit_reaches_terminal_state(instance):
    configured_limit = 2.0
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        start = time.monotonic()
        response = await client.post(
            f"/solve?seed=42&time_limit={configured_limit}&auto_validate=true",
            json=instance,
        )
        assert response.status_code == 202
        job_id = response.json()["job_id"]
        job_data = await _wait_for_terminal_job(
            client,
            job_id,
            timeout_s=configured_limit + 10,
        )
        elapsed = time.monotonic() - start

    assert job_data["status"] in {"completed", "failed"}
    assert job_data["status"] not in {"pending", "running"}
    assert elapsed <= configured_limit + 10, (
        f"Configured limit check took {elapsed:.2f}s, allowed maximum is "
        f"{configured_limit + 10:.2f}s"
    )
    if job_data["status"] == "completed":
        assert job_data["validation_status"] == "passed"
        assert job_data["validation_report"]["passed"] is True


@pytest.mark.qrt
@pytest.mark.quality
@pytest.mark.integration
@pytest.mark.asyncio
async def test_qrt_pe_01_api_submission_remains_responsive(instance):
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        start = time.monotonic()
        response = await client.post("/solve?seed=42&time_limit=60", json=instance)
        elapsed = time.monotonic() - start

    assert response.status_code == 202
    assert elapsed < 1.0, f"API submission blocked for {elapsed:.2f}s"

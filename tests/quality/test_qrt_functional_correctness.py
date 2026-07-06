"""QRT-FC-01 - solver functional correctness."""

import asyncio
import json
import time
from pathlib import Path

import httpx
import pytest

from app.main import app

ROOT = Path(__file__).resolve().parent.parent.parent
FIXTURE = ROOT / "test_cases" / "t1.json"


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
async def test_qrt_fc_01_solver_completes_and_has_zero_hard_violations(instance):
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.post(
            "/solve?seed=42&time_limit=60&auto_validate=true",
            json=instance,
        )
        assert response.status_code == 202
        job_id = response.json()["job_id"]

        job_data = await _wait_for_terminal_job(client, job_id, timeout_s=180)

    assert job_data["status"] == "completed", (
        f"Solver did not complete. Status: {job_data.get('status')}, "
        f"error: {job_data.get('error')}"
    )
    assert job_data["result"], "Completed QRT job must store a solver result"
    assert job_data["validation_status"] == "passed"
    assert job_data["validation_report"]["passed"] is True
    assert job_data["validation_report"]["report"]["total_violations"] == 0

    optional_ids = {
        order["id"] for order in instance["orders"] if order.get("optional")
    }
    unserved = set(job_data["result"].get("unserved_optional", []))
    served_optional = optional_ids - unserved
    routed_orders = {
        order
        for route in job_data["result"].get("vehicles", [])
        for order in route.get("route", [])
        if order != 0
    }
    assert served_optional.issubset(routed_orders)
    assert any(order.get("loader_cnt", 0) > 0 for order in instance["orders"])
    assert job_data["result"].get("loaders"), "Fixture requires loader assignments"

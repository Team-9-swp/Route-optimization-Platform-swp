import asyncio
import pytest
import json
import time
from pathlib import Path
import httpx
from app.main import app


@pytest.mark.qrt
@pytest.mark.quality
@pytest.mark.integration
@pytest.mark.asyncio
async def test_solver_zero_hard_constraint_violations():
    instance_path = Path("test_cases/t1.json")
    if not instance_path.exists():
        pytest.skip("test_cases/t1.json not found")

    with open(instance_path, "r") as f:
        instance = json.load(f)

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.post(
            "/solve?seed=42&time_limit=120&max_restarts=1&auto_validate=true",
            json=instance
        )
        assert response.status_code == 202
        job_id = response.json()["job_id"]

        max_wait = 180
        start = time.time()
        job_data = {}
        while time.time() - start < max_wait:
            job_resp = await client.get(f"/jobs/{job_id}")
            assert job_resp.status_code == 200
            job_data = job_resp.json()
            if job_data["status"] in ["completed", "failed"]:
                break
            await asyncio.sleep(2)

    assert job_data["status"] == "completed", f"Job failed or timed out. Status: {job_data.get('status')}, Error: {job_data.get('error')}"
    assert job_data["validation_status"] == "passed", "Solution did not pass validation"

import asyncio
import json

import httpx
import pytest
import pytest_asyncio

from app.main import app


@pytest_asyncio.fixture
async def client():
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as c:
        yield c


@pytest.mark.slow
@pytest.mark.asyncio
async def test_solve_t1_instance(client):
    with open("test_cases/t1.json") as f:
        instance = json.load(f)

    response = await client.post("/solve?seed=42&time_limit=120&max_restarts=3", json=instance)
    assert response.status_code == 202
    job_id = response.json()["job_id"]

    for _ in range(200):
        response = await client.get(f"/jobs/{job_id}")
        data = response.json()
        if data["status"] in ("completed", "failed"):
            break
        await asyncio.sleep(0.5)

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "completed"
    assert "vehicles" in data["result"]
    assert "loaders" in data["result"]

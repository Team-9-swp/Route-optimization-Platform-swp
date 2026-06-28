import pytest
import json
import time
from pathlib import Path
import httpx
from app.main import app


@pytest.mark.qrt
@pytest.mark.quality
@pytest.mark.asyncio
async def test_api_async_responsiveness():
    instance_path = Path("test_cases/t1.json")
    if not instance_path.exists():
        pytest.skip("test_cases/t1.json not found")

    with open(instance_path, "r") as f:
        instance = json.load(f)

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        start = time.time()
        response = await client.post(
            "/solve?seed=42&time_limit=30&max_restarts=5",
            json=instance
        )
        elapsed = time.time() - start

    assert response.status_code == 202
    assert elapsed < 1.0, f"API submission blocked for {elapsed:.2f}s. Solver must be async."

import pytest
import pytest_asyncio

from app.repository import JobRepository
from app.schemas import JobStatus


@pytest_asyncio.fixture
async def repo():
    r = JobRepository()
    await r.clear_all()
    yield r
    await r.clear_all()


@pytest.mark.asyncio
async def test_create_and_get_job(repo):
    job = await repo.create_job({"orders": []}, seed=42, name="test-job")
    assert job.status == JobStatus.PENDING
    fetched = await repo.get_job(job.job_id)
    assert fetched is not None
    assert fetched.name == "test-job"
    assert fetched.seed == 42

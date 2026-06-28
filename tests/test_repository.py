import pytest
import pytest_asyncio

from app.repository import JobRepository
from app.schemas import JobStatus, ValidationStatus


@pytest_asyncio.fixture
async def repo():
    r = JobRepository()
    await r.clear_all()
    yield r
    await r.clear_all()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_create_and_get_job(repo):
    job = await repo.create_job({"orders": []}, seed=42, name="test-job")
    assert job.status == JobStatus.PENDING
    fetched = await repo.get_job(job.job_id)
    assert fetched is not None
    assert fetched.name == "test-job"
    assert fetched.seed == 42


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_missing_job_returns_none(repo):
    assert await repo.get_job("nonexistent-job-id") is None


@pytest.mark.integration
@pytest.mark.asyncio
async def test_update_job(repo):
    job = await repo.create_job({"orders": []}, seed=42)
    await repo.update_job(
        job.job_id,
        status=JobStatus.RUNNING,
        objective_value=123.45,
        validation_status=ValidationStatus.PASSED,
    )
    updated = await repo.get_job(job.job_id)
    assert updated.status == JobStatus.RUNNING
    assert updated.objective_value == 123.45
    assert updated.validation_status == ValidationStatus.PASSED


@pytest.mark.integration
@pytest.mark.asyncio
async def test_update_missing_job_is_silent(repo):
    await repo.update_job("missing-id", status=JobStatus.COMPLETED)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_list_jobs_pagination_and_sorting(repo):
    for i in range(5):
        await repo.create_job({"id": i}, seed=i)

    page1, total = await repo.list_jobs(page=1, page_size=2)
    assert total == 5
    assert len(page1) == 2
    assert page1[0].created_at >= page1[1].created_at

    page2, total = await repo.list_jobs(page=2, page_size=2)
    assert len(page2) == 2

    page3, total = await repo.list_jobs(page=3, page_size=2)
    assert len(page3) == 1


@pytest.mark.integration
@pytest.mark.asyncio
async def test_job_survives_new_repository_instance(repo):
    job = await repo.create_job({"orders": []}, seed=42, name="survivor")
    new_repo = JobRepository()
    fetched = await new_repo.get_job(job.job_id)
    assert fetched is not None
    assert fetched.name == "survivor"

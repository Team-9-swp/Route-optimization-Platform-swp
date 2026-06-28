import pytest
import pytest_asyncio

from app.repository import JobRepository
from app.runner import run_solver
from app.schemas import JobStatus


@pytest_asyncio.fixture
async def repository():
    repo = JobRepository()
    await repo.clear_all()
    yield repo
    await repo.clear_all()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_runner_updates_job_to_completed(repository):
    record = await repository.create_job({"orders": []}, seed=42, time_limit=2)
    await run_solver(record.job_id, repository)
    updated = await repository.get_job(record.job_id)
    assert updated.status in (JobStatus.COMPLETED, JobStatus.FAILED)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_runner_does_not_leak_traceback(repository, monkeypatch):
    def failing_solver(*args, **kwargs):
        raise RuntimeError("boom")

    monkeypatch.setattr("app.runner._solve_sync", failing_solver)
    record = await repository.create_job({"orders": []}, seed=42)
    await run_solver(record.job_id, repository)
    updated = await repository.get_job(record.job_id)
    assert updated.status == JobStatus.FAILED
    assert "Traceback" not in (updated.error or "")
    assert "RuntimeError: boom" in (updated.error or "")

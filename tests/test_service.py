import pytest

from app.schemas import JobStatus
from app.service import SolverService
from app.store import JobStore


async def noop_runner(job_id: str, store: JobStore) -> None:
    record = store.get_job(job_id)
    if record is not None:
        record.status = JobStatus.RUNNING


@pytest.fixture
def service():
    return SolverService(runner=noop_runner)


@pytest.mark.asyncio
async def test_submit_job_returns_pending(service):
    response = await service.submit_job(instance={"orders": []}, seed=1)
    assert response.status == JobStatus.PENDING
    assert response.job_id is not None


@pytest.mark.asyncio
async def test_get_job_existing(service):
    submitted = await service.submit_job(instance={"orders": []}, seed=1)
    fetched = service.get_job(submitted.job_id)
    assert fetched is not None
    assert fetched.job_id == submitted.job_id


def test_get_job_missing(service):
    assert service.get_job("missing") is None

import pytest
import pytest_asyncio

from app.repository import JobRepository
from app.schemas import JobStatus
from app.service import SolverService


@pytest_asyncio.fixture
async def repository():
    repo = JobRepository()
    await repo.clear_all()
    yield repo
    await repo.clear_all()


@pytest.fixture
def service(repository):
    return SolverService(repository=repository)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_submit_job_returns_pending(service, repository):
    response = await service.submit_job({"orders": []}, seed=1)
    assert response.status == JobStatus.PENDING
    record = await repository.get_job(response.job_id)
    assert record is not None


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_job_not_found(service):
    assert await service.get_job("nonexistent") is None


@pytest.mark.integration
@pytest.mark.asyncio
async def test_list_jobs_pagination(service, repository):
    for i in range(3):
        await repository.create_job({"id": i}, seed=i)
    result = await service.list_jobs(page=1, page_size=2)
    assert result.total == 3
    assert len(result.items) == 2

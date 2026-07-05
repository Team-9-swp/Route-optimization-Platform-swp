import asyncio
import json
from pathlib import Path

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


async def noop_runner(
    job_id: str, repository: JobRepository, *, auto_validate: bool = False
) -> None:
    record = await repository.get_job(job_id)
    if record is not None:
        await repository.update_job(job_id, status=JobStatus.RUNNING)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_submit_job_returns_pending(service, repository):
    response = await service.submit_job({"orders": []}, seed=1)
    assert response.status == JobStatus.PENDING
    assert response.job_id is not None
    record = await repository.get_job(response.job_id)
    assert record is not None


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_job_existing(service, repository):
    submitted = await service.submit_job({"orders": []}, seed=1)
    fetched = await service.get_job(submitted.job_id)
    assert fetched is not None
    assert fetched.job_id == submitted.job_id


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_job_missing(service):
    assert await service.get_job("missing") is None


@pytest.mark.integration
@pytest.mark.asyncio
async def test_service_submits_job_with_name_and_auto_validate(repository, monkeypatch):
    calls = {}

    async def fake_runner(job_id, repo, *, auto_validate=False):
        calls["auto_validate"] = auto_validate
        await repo.update_job(
            job_id,
            status=JobStatus.COMPLETED,
            result={"objective_value": 1.0, "vehicles": [], "loaders": []},
        )

    service = SolverService(repository=repository, runner=fake_runner)
    response = await service.submit_job(
        {"orders": []}, seed=1, name="my-job", auto_validate=True
    )
    await asyncio.sleep(0)
    assert response.name == "my-job"
    assert calls["auto_validate"] is True


@pytest.mark.integration
@pytest.mark.asyncio
async def test_service_lists_jobs(repository):
    service = SolverService(repository=repository, runner=noop_runner)
    await service.submit_job({"orders": []}, seed=1, name="a")
    await service.submit_job({"orders": []}, seed=1, name="b")
    response = await service.list_jobs(page=1, page_size=10)
    assert response.total == 2
    assert len(response.items) == 2


@pytest.mark.asyncio
async def test_service_validate_solution():
    service = SolverService()
    root = Path(__file__).resolve().parent.parent
    instance = json.loads((root / "test_cases" / "t1.json").read_text())
    solution = json.loads((root / "test_cases" / "sol_t1.json").read_text())
    result = await service.validate_solution(instance, solution)
    assert isinstance(result.passed, bool)
    assert hasattr(result, "violations")

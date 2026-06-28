import asyncio
import json
from pathlib import Path

import pytest

from app.schemas import JobStatus
from app.service import SolverService
from app.store import JobStore


async def noop_runner(
    job_id: str, store: JobStore, *, auto_validate: bool = False
) -> None:
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


@pytest.mark.asyncio
async def test_service_submits_job_with_name_and_auto_validate(monkeypatch):
    calls = {}

    async def fake_runner(job_id, store, *, auto_validate=False):
        calls["auto_validate"] = auto_validate
        store.update_job(
            job_id,
            status=JobStatus.COMPLETED,
            result={"objective_value": 1.0, "vehicles": [], "loaders": []},
        )

    store = JobStore()
    service = SolverService(store=store, runner=fake_runner)
    response = await service.submit_job(
        {"orders": []}, seed=1, name="my-job", auto_validate=True
    )
    await asyncio.sleep(0)
    assert response.name == "my-job"
    assert calls["auto_validate"] is True


@pytest.mark.asyncio
async def test_service_lists_jobs():
    store = JobStore()
    service = SolverService(store=store, runner=noop_runner)
    await service.submit_job({"orders": []}, seed=1, name="a")
    await service.submit_job({"orders": []}, seed=1, name="b")
    response = service.list_jobs(page=1, page_size=10)
    assert response.total == 2
    assert len(response.items) == 2


def test_service_validate_solution():
    service = SolverService()
    root = Path(__file__).resolve().parent.parent
    instance = json.loads((root / "test_cases" / "t1.json").read_text())
    solution = json.loads((root / "test_cases" / "sol_t1.json").read_text())
    result = service.validate_solution(instance, solution)
    assert isinstance(result.passed, bool)
    assert hasattr(result, "violations")

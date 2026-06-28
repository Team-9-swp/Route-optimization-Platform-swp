import pytest
import pytest_asyncio

from app.repository import JobRepository
from app.runner import run_solver
from app.schemas import JobStatus, ValidationStatus


@pytest_asyncio.fixture
async def repository():
    repo = JobRepository()
    await repo.clear_all()
    yield repo
    await repo.clear_all()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_run_solver_success(repository, monkeypatch):
    def _fast_solve(instance, seed, time_budget):
        return {
            "vehicles": [{"id": 1, "route": [0, 1, 0], "time": [0.0]}],
            "loaders": [],
            "objective_value": 42.0,
        }

    monkeypatch.setattr("app.runner._solve_sync", _fast_solve)

    record = await repository.create_job(
        instance={"orders": []},
        seed=42,
        time_limit=2,
    )
    await run_solver(record.job_id, repository)
    updated = await repository.get_job(record.job_id)
    assert updated.status == JobStatus.COMPLETED
    assert updated.objective_value == 42.0
    assert updated.result["vehicles"][0]["id"] == 1
    assert "vehicles" in updated.result
    assert "loaders" in updated.result


@pytest.mark.integration
@pytest.mark.asyncio
async def test_run_solver_failure(repository):
    record = await repository.create_job(instance={"orders": []}, seed=42)
    await run_solver(record.job_id, repository)
    updated = await repository.get_job(record.job_id)
    assert updated.status == JobStatus.FAILED
    assert updated.error is not None


def _valid_instance():
    return {
        "vehicle_capacity": 100,
        "vehicle_speed": 1,
        "loader_speed": 1,
        "vehicle_shift_size": 1000,
        "loader_shift_size": 1000,
        "depot": {"x": 0, "y": 0, "load_time": 0},
        "orders": [
            {
                "id": 1,
                "x": 3,
                "y": 4,
                "volume": 10,
                "time_window": [0, 100],
                "vehicle_service_time": 5,
                "loader_cnt": 0,
                "loader_service_time": 0,
                "optional": 0,
            }
        ],
        "weights": {
            "vehicle_salary": 1,
            "loader_salary": 1,
            "fuel_cost": 1,
            "loader_work": 1,
            "optional_order_penalty": 1,
        },
    }


@pytest.mark.integration
@pytest.mark.asyncio
async def test_runner_extracts_objective_value(monkeypatch, repository):
    def fake_solve(instance, seed, *args, **kwargs):
        return {"objective_value": 99.5, "vehicles": [], "loaders": []}

    monkeypatch.setattr("app.runner._solve_sync", fake_solve)
    record = await repository.create_job(_valid_instance(), seed=1)
    await run_solver(record.job_id, repository, auto_validate=False)

    updated = await repository.get_job(record.job_id)
    assert updated.status == JobStatus.COMPLETED
    assert updated.objective_value == 99.5


@pytest.mark.integration
@pytest.mark.asyncio
async def test_runner_auto_validate(monkeypatch, repository):
    def fake_solve(instance, seed, *args, **kwargs):
        return {
            "objective_value": 99.5,
            "vehicles": [{"id": 1, "route": [0, 1, 0], "time": [5.0]}],
            "loaders": [],
        }

    monkeypatch.setattr("app.runner._solve_sync", fake_solve)
    record = await repository.create_job(_valid_instance(), seed=1)
    await run_solver(record.job_id, repository, auto_validate=True)

    updated = await repository.get_job(record.job_id)
    assert updated.status == JobStatus.COMPLETED
    assert updated.validation_status == ValidationStatus.PASSED


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

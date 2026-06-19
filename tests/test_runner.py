import pytest

from app.runner import run_solver
from app.schemas import JobStatus, ValidationStatus
from app.store import JobStore


@pytest.fixture
def store():
    return JobStore()


@pytest.mark.asyncio
async def test_run_solver_success(store):
    record = store.create_job(
        instance={
            "vehicle_capacity": 100,
            "vehicle_speed": 1,
            "loader_speed": 1,
            "vehicle_shift_size": 240,
            "loader_shift_size": 240,
            "depot": {"x": 0, "y": 0, "load_time": 0},
            "orders": [
                {
                    "id": 1,
                    "x": 1,
                    "y": 0,
                    "volume": 1,
                    "time_window": [0, 100],
                    "vehicle_service_time": 1,
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
        },
        seed=42,
    )
    await run_solver(record.job_id, store)
    updated = store.get_job(record.job_id)
    assert updated.status == JobStatus.COMPLETED
    assert "vehicles" in updated.result
    assert "loaders" in updated.result


@pytest.mark.asyncio
async def test_run_solver_failure(store):
    record = store.create_job(instance={"orders": []}, seed=42)
    await run_solver(record.job_id, store)
    updated = store.get_job(record.job_id)
    assert updated.status == JobStatus.FAILED
    assert updated.error is not None


@pytest.mark.asyncio
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


@pytest.mark.asyncio
async def test_runner_extracts_objective_value(monkeypatch, store):
    def fake_solve(instance, seed):
        return {"objective_value": 99.5, "vehicles": [], "loaders": []}

    monkeypatch.setattr("app.runner._solve_sync", fake_solve)
    record = store.create_job(_valid_instance(), seed=1)
    await run_solver(record.job_id, store, auto_validate=False)

    updated = store.get_job(record.job_id)
    assert updated.status == JobStatus.COMPLETED
    assert updated.objective_value == 99.5


@pytest.mark.asyncio
async def test_runner_auto_validate(monkeypatch, store):
    def fake_solve(instance, seed):
        return {
            "objective_value": 99.5,
            "vehicles": [{"id": 1, "route": [0, 1, 0], "time": [5.0]}],
            "loaders": [],
        }

    monkeypatch.setattr("app.runner._solve_sync", fake_solve)
    record = store.create_job(_valid_instance(), seed=1)
    await run_solver(record.job_id, store, auto_validate=True)

    updated = store.get_job(record.job_id)
    assert updated.status == JobStatus.COMPLETED
    assert updated.validation_status == ValidationStatus.PASSED

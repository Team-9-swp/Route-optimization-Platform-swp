import pytest

from app.runner import run_solver
from app.schemas import JobStatus
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

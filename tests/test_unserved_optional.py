import pytest
import pytest_asyncio

from app.repository import JobRepository
from app.runner import run_solver


@pytest_asyncio.fixture
async def repository():
    repo = JobRepository()
    await repo.clear_all()
    yield repo
    await repo.clear_all()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_unserved_optional_present_after_solve(repository):
    instance = {
        "vehicle_capacity": 100,
        "vehicle_speed": 1.0,
        "loader_speed": 0.5,
        "vehicle_shift_size": 1000,
        "loader_shift_size": 1000,
        "depot": {"x": 0, "y": 0, "load_time": 0},
        "orders": [
            {
                "id": 1,
                "x": 1,
                "y": 0,
                "volume": 10,
                "loader_cnt": 1,
                "time_window": [0, 100],
                "vehicle_service_time": 5,
                "loader_service_time": 5,
                "optional": 0,
            },
            {
                "id": 2,
                "x": 2,
                "y": 0,
                "volume": 10,
                "loader_cnt": 1,
                "time_window": [0, 100],
                "vehicle_service_time": 5,
                "loader_service_time": 5,
                "optional": 1,
            },
            {
                "id": 3,
                "x": 3,
                "y": 0,
                "volume": 10,
                "loader_cnt": 1,
                "time_window": [0, 100],
                "vehicle_service_time": 5,
                "loader_service_time": 5,
                "optional": 1,
            },
        ],
        "weights": {
            "vehicle_salary": 100,
            "fuel_cost": 1,
            "loader_salary": 50,
            "loader_work": 1,
            "optional_order_penalty": 10,
        },
    }
    record = await repository.create_job(instance, seed=42, time_limit=2)
    await run_solver(record.job_id, repository)
    updated = await repository.get_job(record.job_id)
    assert updated.result is not None
    assert "unserved_optional" in updated.result
    assert isinstance(updated.result["unserved_optional"], list)

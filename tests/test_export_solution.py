import pytest
import pytest_asyncio
from fastapi.testclient import TestClient

from app.db import dispose_engine
from app.main import create_app
from app.repository import JobRepository
from app.schemas import JobStatus


def _minimal_instance():
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
            },
            {
                "id": 2,
                "x": 6,
                "y": 8,
                "volume": 5,
                "time_window": [0, 100],
                "vehicle_service_time": 5,
                "loader_cnt": 0,
                "loader_service_time": 0,
                "optional": 0,
            },
        ],
        "weights": {
            "vehicle_salary": 1,
            "loader_salary": 1,
            "fuel_cost": 1,
            "loader_work": 1,
            "optional_order_penalty": 1,
        },
    }


def _minimal_solution():
    return {
        "vehicles": [{"id": 1, "route": [0, 1, 2, 0], "time": [5.0, 15.0]}],
        "loaders": [],
    }


@pytest_asyncio.fixture(autouse=True)
async def clean_repository():
    repo = JobRepository()
    await repo.clear_all()
    await dispose_engine()
    yield
    repo = JobRepository()
    await repo.clear_all()
    await dispose_engine()


@pytest.fixture
def client():
    with TestClient(create_app(init_db_on_startup=True)) as c:
        yield c


@pytest.mark.integration
async def test_exported_solution_is_validator_compatible(client):
    """Reproduces issue #126 and verifies the fix.

    Previously the web interface exported the whole ``JobResponse`` envelope,
    so a downloaded file had ``vehicles``/``loaders`` nested under ``result``
    and could not be passed to the project validator. The export endpoint now
    returns the solution at the top level, matching the validator schema.
    """
    repo = JobRepository()
    record = await repo.create_job(_minimal_instance(), seed=42, name="export-test")
    await repo.update_job(
        record.job_id,
        status=JobStatus.COMPLETED,
        result=_minimal_solution(),
        objective_value=42.0,
    )

    exported = client.get(f"/jobs/{record.job_id}/solution")
    assert exported.status_code == 200
    solution = exported.json()

    # Validator-compatible shape: top-level vehicles/loaders.
    assert "vehicles" in solution
    assert "loaders" in solution

    # The exported solution validates successfully on its own.
    validation = client.post(
        "/validate",
        json={"instance": _minimal_instance(), "solution": solution},
    )
    assert validation.status_code == 200
    assert validation.json()["passed"] is True

    # Regression guard: the whole job envelope is NOT validator-compatible,
    # because vehicles/loaders are nested under ``result``.
    envelope = client.get(f"/jobs/{record.job_id}").json()
    assert "vehicles" not in envelope
    assert "vehicles" in envelope["result"]


@pytest.mark.integration
def test_export_solution_not_found(client):
    response = client.get("/jobs/does-not-exist/solution")
    assert response.status_code == 404


@pytest.mark.integration
async def test_export_solution_not_ready_for_pending_job(client):
    repo = JobRepository()
    record = await repo.create_job(_minimal_instance(), seed=42)

    response = client.get(f"/jobs/{record.job_id}/solution")
    assert response.status_code == 404

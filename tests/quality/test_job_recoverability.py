"""QRT-RE-01 - job recoverability with PostgreSQL persistence."""

from datetime import datetime, timezone

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient

from app.db import dispose_engine
from app.main import create_app
from app.repository import JobRepository
from app.schemas import JobStatus, ValidationStatus


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


def _completed_result() -> dict:
    return {
        "objective_value": 123.45,
        "vehicles": [{"id": 1, "route": [0, 1, 0], "time": [10.0]}],
        "loaders": [],
        "unserved_optional": [99],
    }


def _validation_report() -> dict:
    return {
        "passed": True,
        "objective_value": 123.45,
        "violations": [],
        "report": {"total_violations": 0, "violations": {}},
    }


@pytest.mark.qrt
@pytest.mark.quality
@pytest.mark.integration
@pytest.mark.asyncio
async def test_qrt_re_01_completed_job_survives_repository_recreation():
    payload = {"orders": [{"id": 1, "optional": 0}], "weights": {"fuel_cost": 1}}
    result = _completed_result()
    validation = _validation_report()

    first_repo = JobRepository()
    record = await first_repo.create_job(
        payload,
        seed=42,
        name="recoverability-completed",
        time_limit=60,
    )
    await first_repo.update_job(
        record.job_id,
        status=JobStatus.COMPLETED,
        started_at=datetime.now(timezone.utc),
        finished_at=datetime.now(timezone.utc),
        result=result,
        objective_value=result["objective_value"],
        validation_status=ValidationStatus.PASSED,
        validation_report=validation,
    )

    await dispose_engine()

    second_repo = JobRepository()
    restored = await second_repo.get_job(record.job_id)

    assert restored is not None
    assert restored.job_id == record.job_id
    assert restored.input_data == payload
    assert restored.seed == 42
    assert restored.time_limit == 60
    assert restored.name == "recoverability-completed"
    assert restored.status == JobStatus.COMPLETED
    assert restored.result == result
    assert restored.objective_value == result["objective_value"]
    assert restored.validation_status == ValidationStatus.PASSED
    assert restored.validation_report == validation


@pytest.mark.qrt
@pytest.mark.quality
@pytest.mark.integration
@pytest.mark.asyncio
async def test_qrt_re_01_completed_job_is_retrievable_after_application_recreation(
    client,
):
    payload = {"orders": [{"id": 7, "optional": 0}], "weights": {"fuel_cost": 1}}
    result = _completed_result()
    validation = _validation_report()

    repo = JobRepository()
    record = await repo.create_job(
        payload,
        seed=7,
        name="recoverability-api",
        time_limit=30,
    )
    await repo.update_job(
        record.job_id,
        status=JobStatus.COMPLETED,
        started_at=datetime.now(timezone.utc),
        finished_at=datetime.now(timezone.utc),
        result=result,
        objective_value=result["objective_value"],
        validation_status=ValidationStatus.PASSED,
        validation_report=validation,
    )

    await dispose_engine()

    with TestClient(create_app(init_db_on_startup=True)) as recreated_client:
        response = recreated_client.get(f"/jobs/{record.job_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["job_id"] == record.job_id
    assert data["input_data"] == payload
    assert data["seed"] == 7
    assert data["time_limit"] == 30
    assert data["name"] == "recoverability-api"
    assert data["status"] == "completed"
    assert data["result"] == result
    assert data["objective_value"] == result["objective_value"]
    assert data["validation_status"] == "passed"
    assert data["validation_report"] == validation
    assert data["unserved_optional"] == [99]

from datetime import datetime, timezone

import pytest

from app.schemas import JobRecord, JobResponse, JobStatus, SolveResponse, ValidationStatus


def test_job_status_values():
    assert JobStatus.PENDING.value == "pending"
    assert JobStatus.RUNNING.value == "running"
    assert JobStatus.COMPLETED.value == "completed"
    assert JobStatus.FAILED.value == "failed"


def test_job_record_completed():
    now = datetime.now(timezone.utc)
    job = JobRecord(
        job_id="abc",
        status=JobStatus.COMPLETED,
        created_at=now,
        started_at=now,
        finished_at=now,
        result={"vehicles": []},
    )
    assert job.status == "completed"
    assert job.result == {"vehicles": []}


def test_solve_response():
    now = datetime.now(timezone.utc)
    resp = SolveResponse(job_id="abc", status=JobStatus.PENDING, created_at=now)
    assert resp.job_id == "abc"
    assert resp.status == JobStatus.PENDING


def test_job_response():
    now = datetime.now(timezone.utc)
    resp = JobResponse(job_id="abc", status=JobStatus.COMPLETED, created_at=now)
    assert resp.result is None
    assert resp.error is None


def test_job_record_accepts_name_and_validation_fields():
    now = datetime.now(timezone.utc)
    record = JobRecord(
        job_id="abc",
        status=JobStatus.PENDING,
        created_at=now,
        name="test-job",
        objective_value=123.45,
        validation_status=ValidationStatus.PENDING,
        validation_report={"passed": True},
    )
    assert record.name == "test-job"
    assert record.objective_value == 123.45
    assert record.validation_status == ValidationStatus.PENDING

import pytest
from pydantic import ValidationError

from app.schemas import JobRecord, JobResponse, JobStatus, SolveRequest, SolveResponse


def test_solve_request_defaults():
    req = SolveRequest(instance={"orders": []})
    assert req.instance == {"orders": []}
    assert req.seed == 42


def test_solve_request_accepts_seed():
    req = SolveRequest(instance={}, seed=7)
    assert req.seed == 7


def test_solve_request_rejects_negative_seed():
    with pytest.raises(ValidationError):
        SolveRequest(instance={}, seed=-1)


def test_job_status_values():
    assert JobStatus.PENDING.value == "pending"
    assert JobStatus.RUNNING.value == "running"
    assert JobStatus.COMPLETED.value == "completed"
    assert JobStatus.FAILED.value == "failed"


def test_job_record_completed():
    from datetime import datetime, timezone

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
    from datetime import datetime, timezone

    now = datetime.now(timezone.utc)
    resp = SolveResponse(job_id="abc", status=JobStatus.PENDING, created_at=now)
    assert resp.job_id == "abc"
    assert resp.status == JobStatus.PENDING


def test_job_response():
    from datetime import datetime, timezone

    now = datetime.now(timezone.utc)
    resp = JobResponse(job_id="abc", status=JobStatus.COMPLETED, created_at=now)
    assert resp.result is None
    assert resp.error is None

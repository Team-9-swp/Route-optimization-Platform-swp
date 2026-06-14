import uuid
from datetime import datetime, timezone
from threading import Lock

from app.schemas import JobRecord, JobStatus


class JobStore:
    def __init__(self) -> None:
        self._jobs: dict[str, JobRecord] = {}
        self._lock = Lock()

    def create_job(self, instance: dict, seed: int) -> JobRecord:
        job_id = str(uuid.uuid4())
        record = JobRecord(
            job_id=job_id,
            status=JobStatus.PENDING,
            created_at=datetime.now(timezone.utc),
            input_data=instance,
            seed=seed,
        )
        with self._lock:
            self._jobs[job_id] = record
        return record

    def get_job(self, job_id: str) -> JobRecord | None:
        with self._lock:
            return self._jobs.get(job_id)

    def update_job(
        self,
        job_id: str,
        *,
        status: JobStatus | None = None,
        started_at: datetime | None = None,
        finished_at: datetime | None = None,
        result: dict | None = None,
        error: str | None = None,
    ) -> None:
        with self._lock:
            record = self._jobs.get(job_id)
            if record is None:
                return
            if status is not None:
                record.status = status
            if started_at is not None:
                record.started_at = started_at
            if finished_at is not None:
                record.finished_at = finished_at
            if result is not None:
                record.result = result
            if error is not None:
                record.error = error

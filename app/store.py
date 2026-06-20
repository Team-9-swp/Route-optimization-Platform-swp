import uuid
from datetime import datetime, timezone
from threading import Lock

from app.schemas import JobRecord, JobStatus, ValidationStatus


class JobStore:
    def __init__(self) -> None:
        self._jobs: dict[str, JobRecord] = {}
        self._lock = Lock()

    def create_job(
        self,
        instance: dict,
        seed: int,
        name: str | None = None,
        time_limit: float | None = None,
        max_restarts: int | None = None,
    ) -> JobRecord:
        job_id = str(uuid.uuid4())
        record = JobRecord(
            job_id=job_id,
            status=JobStatus.PENDING,
            created_at=datetime.now(timezone.utc),
            name=name,
            input_data=instance,
            seed=seed,
            time_limit=time_limit,
            max_restarts=max_restarts,
        )
        with self._lock:
            self._jobs[job_id] = record
        return record

    def get_job(self, job_id: str) -> JobRecord | None:
        with self._lock:
            return self._jobs.get(job_id)

    def list_jobs(
        self,
        *,
        page: int = 1,
        page_size: int = 25,
        sort_desc: bool = True,
    ) -> tuple[list[JobRecord], int]:
        with self._lock:
            records = list(self._jobs.values())
        records.sort(key=lambda r: r.created_at, reverse=sort_desc)
        total = len(records)
        start = (page - 1) * page_size
        return records[start : start + page_size], total

    def update_job(
        self,
        job_id: str,
        *,
        status: JobStatus | None = None,
        name: str | None = None,
        started_at: datetime | None = None,
        finished_at: datetime | None = None,
        result: dict | None = None,
        error: str | None = None,
        objective_value: float | None = None,
        validation_status: ValidationStatus | None = None,
        validation_report: dict | None = None,
    ) -> None:
        with self._lock:
            record = self._jobs.get(job_id)
            if record is None:
                return
            if status is not None:
                record.status = status
            if name is not None:
                record.name = name
            if started_at is not None:
                record.started_at = started_at
            if finished_at is not None:
                record.finished_at = finished_at
            if result is not None:
                record.result = result
            if error is not None:
                record.error = error
            if objective_value is not None:
                record.objective_value = objective_value
            if validation_status is not None:
                record.validation_status = validation_status
            if validation_report is not None:
                record.validation_report = validation_report

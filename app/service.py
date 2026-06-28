import asyncio
from typing import Any, Callable, Coroutine

from app.runner import run_solver
from app.schemas import JobListResponse, JobResponse, SolveResponse, ValidationResponse
from app.store import JobStore
from app.validation import validate_solution as _validate_solution


class SolverService:
    def __init__(
        self,
        store: JobStore | None = None,
        runner: Callable[..., Coroutine[Any, Any, None]] | None = None,
    ) -> None:
        self._store = store or JobStore()
        self._runner = runner or run_solver

    async def submit_job(
        self,
        instance: dict,
        seed: int,
        *,
        name: str | None = None,
        auto_validate: bool = False,
        time_limit: float | None = None,
        max_restarts: int | None = None,
    ) -> SolveResponse:
        record = self._store.create_job(
            instance, seed, name=name, time_limit=time_limit, max_restarts=max_restarts
        )
        asyncio.create_task(
            self._runner(record.job_id, self._store, auto_validate=auto_validate)
        )
        return SolveResponse(
            job_id=record.job_id,
            status=record.status,
            created_at=record.created_at,
            name=record.name,
        )

    def get_job(self, job_id: str) -> JobResponse | None:
        record = self._store.get_job(job_id)
        if record is None:
            return None
        return JobResponse(
            job_id=record.job_id,
            status=record.status,
            name=record.name,
            created_at=record.created_at,
            input_data=record.input_data,
            seed=record.seed,
            started_at=record.started_at,
            finished_at=record.finished_at,
            result=record.result,
            error=record.error,
            objective_value=record.objective_value,
            validation_status=record.validation_status,
            validation_report=record.validation_report,
        )

    def list_jobs(
        self,
        *,
        page: int = 1,
        page_size: int = 25,
        sort_desc: bool = True,
    ) -> JobListResponse:
        records, total = self._store.list_jobs(
            page=page, page_size=page_size, sort_desc=sort_desc
        )
        return JobListResponse(
            items=[self.get_job(record.job_id) for record in records],
            total=total,
            page=page,
            page_size=page_size,
        )

    def validate_solution(self, instance: dict, solution: dict) -> ValidationResponse:
        result = _validate_solution(instance, solution)
        return ValidationResponse(**result)

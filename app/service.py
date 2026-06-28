import asyncio
from typing import Any, Awaitable, Callable

from app.repository import JobRepository
from app.runner import run_solver
from app.schemas import JobListResponse, JobResponse, SolveResponse, ValidationResponse
from app.validation import validate_solution as _validate_solution


class SolverService:
    def __init__(
        self,
        repository: JobRepository | None = None,
        runner: Callable[..., Awaitable[None]] | None = None,
    ) -> None:
        self._repository = repository or JobRepository()
        self._runner = runner or run_solver

    async def submit_job(
        self,
        instance: dict,
        seed: int,
        *,
        name: str | None = None,
        auto_validate: bool = False,
        time_limit: float | None = None,
    ) -> SolveResponse:
        record = await self._repository.create_job(
            instance, seed, name=name, time_limit=time_limit
        )
        asyncio.create_task(
            self._runner(record.job_id, self._repository, auto_validate=auto_validate)
        )
        return SolveResponse(
            job_id=record.job_id,
            status=record.status,
            created_at=record.created_at,
            name=record.name,
        )

    async def get_job(self, job_id: str) -> JobResponse | None:
        record = await self._repository.get_job(job_id)
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
            unserved_optional=record.result.get("unserved_optional") if record.result else None,
        )

    async def list_jobs(
        self,
        *,
        page: int = 1,
        page_size: int = 25,
        sort_desc: bool = True,
    ) -> JobListResponse:
        records, total = await self._repository.list_jobs(
            page=page, page_size=page_size, sort_desc=sort_desc
        )
        items = []
        for record in records:
            job = await self.get_job(record.job_id)
            if job is not None:
                items.append(job)
        return JobListResponse(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
        )

    async def validate_solution(self, instance: dict, solution: dict) -> ValidationResponse:
        result = _validate_solution(instance, solution)
        return ValidationResponse(**result)

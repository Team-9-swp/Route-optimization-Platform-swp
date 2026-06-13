import asyncio
from typing import Any, Callable, Coroutine

from app.runner import run_solver
from app.schemas import JobResponse, SolveResponse
from app.store import JobStore


class SolverService:
    def __init__(
        self,
        store: JobStore | None = None,
        runner: Callable[[str, JobStore], Coroutine[Any, Any, None]] | None = None,
    ) -> None:
        self._store = store or JobStore()
        self._runner = runner or run_solver

    async def submit_job(self, instance: dict, seed: int) -> SolveResponse:
        record = self._store.create_job(instance, seed)
        asyncio.create_task(self._runner(record.job_id, self._store))
        return SolveResponse(
            job_id=record.job_id,
            status=record.status,
            created_at=record.created_at,
        )

    def get_job(self, job_id: str) -> JobResponse | None:
        record = self._store.get_job(job_id)
        if record is None:
            return None
        return JobResponse(
            job_id=record.job_id,
            status=record.status,
            created_at=record.created_at,
            started_at=record.started_at,
            finished_at=record.finished_at,
            result=record.result,
            error=record.error,
        )

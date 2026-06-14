import asyncio
import contextlib
import io
import traceback
from datetime import datetime, timezone

from app.schemas import JobStatus
from app.store import JobStore


def _solve_sync(instance: dict, seed: int) -> dict | None:
    import main_mvp

    return main_mvp.solve(instance, seed)


async def run_solver(job_id: str, store: JobStore) -> None:
    record = store.get_job(job_id)
    if record is None:
        return

    store.update_job(
        job_id,
        status=JobStatus.RUNNING,
        started_at=datetime.now(timezone.utc),
    )

    try:
        stdout_capture = io.StringIO()
        with contextlib.redirect_stdout(stdout_capture):
            result = await asyncio.to_thread(
                _solve_sync,
                record.input_data,
                record.seed,
            )

        if result is None:
            store.update_job(
                job_id,
                status=JobStatus.FAILED,
                finished_at=datetime.now(timezone.utc),
                error="Solver returned infeasible solution",
            )
            return

        store.update_job(
            job_id,
            status=JobStatus.COMPLETED,
            finished_at=datetime.now(timezone.utc),
            result=result,
        )
    except Exception as exc:
        store.update_job(
            job_id,
            status=JobStatus.FAILED,
            finished_at=datetime.now(timezone.utc),
            error=f"{type(exc).__name__}: {exc}\n{traceback.format_exc()}",
        )

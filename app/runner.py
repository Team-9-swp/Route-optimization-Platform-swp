import asyncio
import contextlib
import io
import traceback
from datetime import datetime, timezone

from app.schemas import JobStatus, ValidationStatus
from app.store import JobStore
from app.validation import validate_solution


def _solve_sync(
    instance: dict,
    seed: int,
    time_budget: float = 30.0,
    max_restarts: int | None = None,
) -> dict | None:
    from beta_code.pipeline.orchestrate import solve as _solve

    return _solve(instance, time_limit=time_budget, seed=seed)


def _extract_objective_value(result: dict | None) -> float | None:
    if result is None:
        return None
    if "objective_value" in result:
        return result["objective_value"]
    if "_cost" in result:
        result["objective_value"] = result["_cost"]
        return result["objective_value"]
    return None


async def run_solver(
    job_id: str,
    store: JobStore,
    *,
    auto_validate: bool = False,
) -> None:
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
                record.time_limit if record.time_limit is not None else 30.0,
                record.max_restarts,
            )

        if result is None:
            store.update_job(
                job_id,
                status=JobStatus.FAILED,
                finished_at=datetime.now(timezone.utc),
                error="Solver returned infeasible solution",
            )
            return

        objective_value = _extract_objective_value(result)
        store.update_job(
            job_id,
            status=JobStatus.COMPLETED,
            finished_at=datetime.now(timezone.utc),
            result=result,
            objective_value=objective_value,
        )

        if auto_validate:
            validation = validate_solution(record.input_data, result)
            store.update_job(
                job_id,
                validation_status=ValidationStatus.PASSED if validation["passed"] else ValidationStatus.FAILED,
                validation_report=validation,
            )
    except Exception as exc:
        store.update_job(
            job_id,
            status=JobStatus.FAILED,
            finished_at=datetime.now(timezone.utc),
            error=f"{type(exc).__name__}: {exc}\n{traceback.format_exc()}",
        )

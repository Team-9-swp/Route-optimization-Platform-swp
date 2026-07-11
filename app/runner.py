import asyncio
import contextlib
import io
import logging
from datetime import datetime, timezone

from app.repository import JobRepository
from app.schemas import JobStatus, ValidationStatus
from app.validation import validate_solution

logger = logging.getLogger(__name__)


def _solve_sync(
    instance: dict,
    seed: int,
    time_budget: float = 30.0,
) -> dict | None:
    from solver import solve as _solve

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
    repository: JobRepository,
    *,
    auto_validate: bool = False,
) -> None:
    record = await repository.get_job(job_id)
    if record is None:
        return

    await repository.update_job(
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
                record.time_limit if record.time_limit is not None else 120.0,
            )

        if result is None:
            await repository.update_job(
                job_id,
                status=JobStatus.FAILED,
                finished_at=datetime.now(timezone.utc),
                error="Solver returned infeasible solution",
            )
            return

        objective_value = _extract_objective_value(result)
        result = {
            k: v
            for k, v in result.items()
            if k not in ("_cost", "_evaluator", "objective_value")
        }

        validation_status = None
        validation_report = None
        if auto_validate:
            validation = validate_solution(record.input_data, result)
            validation_status = (
                ValidationStatus.PASSED
                if validation["passed"]
                else ValidationStatus.FAILED
            )
            validation_report = validation

        await repository.update_job(
            job_id,
            status=JobStatus.COMPLETED,
            finished_at=datetime.now(timezone.utc),
            result=result,
            objective_value=objective_value,
            validation_status=validation_status,
            validation_report=validation_report,
        )
    except Exception as exc:
        logger.exception("Solver failed for job %s", job_id)
        # Store a user-safe error message. Detailed diagnostics are written to
        # the server-side log above via logger.exception().
        await repository.update_job(
            job_id,
            status=JobStatus.FAILED,
            finished_at=datetime.now(timezone.utc),
            error=f"{type(exc).__name__}: solver execution failed",
        )

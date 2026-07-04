from fastapi import APIRouter, Body, HTTPException, Query

from app.schemas import (
    JobListResponse,
    JobResponse,
    JobStatus,
    SolveResponse,
    ValidationRequest,
    ValidationResponse,
)
from app.service import SolverService

router = APIRouter()
service = SolverService()


@router.post("/solve", response_model=SolveResponse, status_code=202)
async def solve(
    instance: dict = Body(...),
    seed: int = Query(default=42, ge=0),
    name: str | None = Query(default=None),
    auto_validate: bool = Query(default=False),
    time_limit: float | None = Query(default=None, gt=0),
) -> SolveResponse:
    return await service.submit_job(
        instance,
        seed,
        name=name,
        auto_validate=auto_validate,
        time_limit=time_limit,
    )


@router.get("/jobs/{job_id}", response_model=JobResponse)
async def get_job(job_id: str) -> JobResponse:
    job = await service.get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.get("/jobs", response_model=JobListResponse)
async def list_jobs(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=100),
) -> JobListResponse:
    return await service.list_jobs(page=page, page_size=page_size)


@router.post("/validate", response_model=ValidationResponse)
async def validate(payload: ValidationRequest) -> ValidationResponse:
    return await service.validate_solution(payload.instance, payload.solution)


@router.get("/jobs/{job_id}/export")
async def export_job(job_id: str) -> dict:
    job = await service.get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    if job.status != JobStatus.COMPLETED:
        raise HTTPException(status_code=400, detail="Job is not completed")
    if job.result is None:
        raise HTTPException(status_code=400, detail="Job has no result")
    return {
        "vehicles": job.result.get("vehicles", []),
        "loaders": job.result.get("loaders", []),
    }


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}

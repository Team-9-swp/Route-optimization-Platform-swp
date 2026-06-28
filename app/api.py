from fastapi import APIRouter, HTTPException, Query

from app.schemas import (
    JobListResponse,
    JobResponse,
    ValidationRequest,
    ValidationResponse,
)
from app.service import SolverService

router = APIRouter()
service = SolverService()


@router.post("/solve", status_code=202)
async def solve_endpoint(
    instance: dict,
    seed: int = Query(42),
    time_limit: int = Query(60),
    max_restarts: int = Query(3),
    auto_validate: bool = Query(False),
    name: str | None = Query(None),
):
    response = await service.submit_job(
        instance=instance,
        seed=seed,
        name=name,
        auto_validate=auto_validate,
        time_limit=time_limit,
        max_restarts=max_restarts,
    )
    return response.model_dump()


@router.get("/jobs/{job_id}", response_model=JobResponse)
async def get_job(job_id: str) -> JobResponse:
    job = service.get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.get("/jobs", response_model=JobListResponse)
async def list_jobs(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=100),
) -> JobListResponse:
    return service.list_jobs(page=page, page_size=page_size)


@router.post("/validate", response_model=ValidationResponse)
async def validate(payload: ValidationRequest) -> ValidationResponse:
    return service.validate_solution(payload.instance, payload.solution)


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}

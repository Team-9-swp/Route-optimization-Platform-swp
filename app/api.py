from fastapi import APIRouter, Body, HTTPException, Query

from app.schemas import JobResponse, SolveResponse
from app.service import SolverService

router = APIRouter()
service = SolverService()


@router.post("/solve", response_model=SolveResponse, status_code=202)
async def solve(
    instance: dict = Body(...),
    seed: int = Query(default=42, ge=0),
) -> SolveResponse:
    return await service.submit_job(instance, seed)


@router.get("/jobs/{job_id}", response_model=JobResponse)
async def get_job(job_id: str) -> JobResponse:
    job = service.get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

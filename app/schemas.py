from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class JobStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class JobRecord(BaseModel):
    job_id: str
    status: JobStatus
    created_at: datetime
    input_data: dict[str, Any] = Field(default_factory=dict)
    seed: int = 42
    started_at: datetime | None = None
    finished_at: datetime | None = None
    result: dict[str, Any] | None = None
    error: str | None = None


class SolveResponse(BaseModel):
    job_id: str
    status: JobStatus
    created_at: datetime


class JobResponse(BaseModel):
    job_id: str
    status: JobStatus
    created_at: datetime
    started_at: datetime | None = None
    finished_at: datetime | None = None
    result: dict[str, Any] | None = None
    error: str | None = None

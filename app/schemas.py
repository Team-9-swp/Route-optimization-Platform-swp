from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class JobStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class ValidationStatus(str, Enum):
    PENDING = "pending"
    PASSED = "passed"
    FAILED = "failed"


class JobRecord(BaseModel):
    job_id: str
    status: JobStatus
    created_at: datetime
    name: str | None = None
    input_data: dict[str, Any] = Field(default_factory=dict)
    seed: int = 42
    time_limit: float | None = None
    max_restarts: int | None = None
    started_at: datetime | None = None
    finished_at: datetime | None = None
    result: dict[str, Any] | None = None
    error: str | None = None
    objective_value: float | None = None
    validation_status: ValidationStatus | None = None
    validation_report: dict[str, Any] | None = None


class SolveResponse(BaseModel):
    job_id: str
    status: JobStatus
    created_at: datetime
    name: str | None = None


class JobResponse(BaseModel):
    job_id: str
    status: JobStatus
    name: str | None = None
    created_at: datetime
    input_data: dict[str, Any] = Field(default_factory=dict)
    seed: int = 42
    started_at: datetime | None = None
    finished_at: datetime | None = None
    result: dict[str, Any] | None = None
    error: str | None = None
    objective_value: float | None = None
    validation_status: ValidationStatus | None = None
    validation_report: dict[str, Any] | None = None


class ValidationRequest(BaseModel):
    instance: dict[str, Any]
    solution: dict[str, Any]


class ValidationResponse(BaseModel):
    passed: bool
    objective_value: float | None = None
    violations: list[str] = Field(default_factory=list)
    report: dict[str, Any] = Field(default_factory=dict)


class JobListResponse(BaseModel):
    items: list[JobResponse]
    total: int
    page: int
    page_size: int

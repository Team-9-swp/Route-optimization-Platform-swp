# Backend API for Frontend Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Extend the existing FastAPI backend so the React frontend can list jobs, validate solutions, check health, and see richer job metadata, while keeping the in-memory store.

**Architecture:** Add CORS middleware, expand Pydantic schemas and the in-memory `JobStore`, enrich the runner/service with `name`, `objective_value`, and auto-validation, and expose new endpoints (`GET /jobs`, `POST /validate`, `GET /health`).

**Tech Stack:** FastAPI, Pydantic, Python 3.11, existing `main_mvp.py` solver, existing `validator.py`.

---

## File Structure

| File | Responsibility |
|------|----------------|
| `app/main.py` | FastAPI app factory, CORS middleware registration |
| `app/schemas.py` | Pydantic models: `JobRecord`, `SolveResponse`, `JobResponse`, `ValidationResponse`, `ValidationStatus`, `JobListResponse` |
| `app/store.py` | Thread-safe in-memory job store with extended update fields |
| `app/runner.py` | Async solver runner; extracts `objective_value`; triggers validation when requested |
| `app/validation.py` | Thin wrapper around the existing `validator.py` logic, exposing `validate(instance, solution)` |
| `app/service.py` | Service layer: `submit_job`, `get_job`, `list_jobs`, `validate_solution` |
| `app/api.py` | FastAPI route handlers for `/solve`, `/jobs`, `/jobs/{id}`, `/validate`, `/health` |
| `tests/test_api.py` | Unit tests for API endpoints |
| `tests/test_service.py` | Unit tests for service layer and validation |
| `tests/test_validation.py` | Tests for validation wrapper |
| `docker-compose.yml` | Docker Compose with `api` and `frontend` services |
| `Dockerfile` | API image; ensure `curl` is available for healthchecks |

---

### Task 1: Add CORS middleware

**Files:**
- Modify: `app/main.py`
- Test: `tests/test_api.py`

- [ ] **Step 1: Write the failing test**

```python
def test_cors_preflight(client):
    response = client.options(
        "/solve",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "POST",
        },
    )
    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_api.py::test_cors_preflight -v`
Expected: FAIL — header missing or 400

- [ ] **Step 3: Implement CORS middleware**

```python
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Route Optimization Solver",
        description="Async wrapper around main_mvp.py CVRPTW solver",
        version="0.1.0",
    )

    origins = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[origin.strip() for origin in origins],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(router)
    return app


app = create_app()
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_api.py::test_cors_preflight -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add app/main.py tests/test_api.py
git commit -m "feat(api): add configurable CORS middleware"
```

---

### Task 2: Expand job schemas

**Files:**
- Modify: `app/schemas.py`
- Test: `tests/test_schemas.py`

- [ ] **Step 1: Write the failing test**

```python
from datetime import datetime, timezone

from app.schemas import JobRecord, JobStatus, ValidationStatus


def test_job_record_accepts_name_and_validation_fields():
    record = JobRecord(
        job_id="abc",
        status=JobStatus.PENDING,
        created_at=datetime.now(timezone.utc),
        name="test-job",
        objective_value=123.45,
        validation_status=ValidationStatus.PENDING,
        validation_report={"passed": True},
    )
    assert record.name == "test-job"
    assert record.objective_value == 123.45
    assert record.validation_status == ValidationStatus.PENDING
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_schemas.py::test_job_record_accepts_name_and_validation_fields -v`
Expected: FAIL — fields do not exist

- [ ] **Step 3: Expand schemas**

```python
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_schemas.py::test_job_record_accepts_name_and_validation_fields -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add app/schemas.py tests/test_schemas.py
git commit -m "feat(schemas): add name, objective, validation fields"
```

---

### Task 3: Extend JobStore update method

**Files:**
- Modify: `app/store.py`
- Test: `tests/test_store.py`

- [ ] **Step 1: Write the failing test**

```python
from app.schemas import JobStatus, ValidationStatus
from app.store import JobStore


def test_store_updates_extended_fields():
    store = JobStore()
    record = store.create_job({"orders": []}, seed=1)
    store.update_job(
        record.job_id,
        status=JobStatus.COMPLETED,
        name="job-name",
        objective_value=42.0,
        validation_status=ValidationStatus.PASSED,
        validation_report={"ok": True},
    )
    updated = store.get_job(record.job_id)
    assert updated.name == "job-name"
    assert updated.objective_value == 42.0
    assert updated.validation_status == ValidationStatus.PASSED
    assert updated.validation_report == {"ok": True}


def test_store_lists_jobs_sorted_by_created_at():
    store = JobStore()
    a = store.create_job({"orders": []}, seed=1)
    b = store.create_job({"orders": []}, seed=1)
    items, total = store.list_jobs(page=1, page_size=10)
    assert total == 2
    assert items[0].created_at >= items[1].created_at
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_store.py -v`
Expected: FAIL — unexpected keyword arguments / missing method

- [ ] **Step 3: Extend update_job and add list_jobs**

```python
import uuid
from datetime import datetime, timezone
from threading import Lock

from app.schemas import JobRecord, JobStatus, ValidationStatus


class JobStore:
    def __init__(self) -> None:
        self._jobs: dict[str, JobRecord] = {}
        self._lock = Lock()

    def create_job(self, instance: dict, seed: int, name: str | None = None) -> JobRecord:
        job_id = str(uuid.uuid4())
        record = JobRecord(
            job_id=job_id,
            status=JobStatus.PENDING,
            created_at=datetime.now(timezone.utc),
            name=name,
            input_data=instance,
            seed=seed,
        )
        with self._lock:
            self._jobs[job_id] = record
        return record

    def get_job(self, job_id: str) -> JobRecord | None:
        with self._lock:
            return self._jobs.get(job_id)

    def list_jobs(
        self,
        *,
        page: int = 1,
        page_size: int = 25,
        sort_by: str = "created_at",
        sort_desc: bool = True,
    ) -> tuple[list[JobRecord], int]:
        with self._lock:
            records = list(self._jobs.values())
        reverse = sort_desc
        if sort_by == "created_at":
            records.sort(key=lambda r: r.created_at, reverse=reverse)
        elif sort_by == "status":
            records.sort(key=lambda r: r.status.value, reverse=reverse)
        total = len(records)
        start = (page - 1) * page_size
        return records[start : start + page_size], total

    def update_job(
        self,
        job_id: str,
        *,
        status: JobStatus | None = None,
        name: str | None = None,
        started_at: datetime | None = None,
        finished_at: datetime | None = None,
        result: dict | None = None,
        error: str | None = None,
        objective_value: float | None = None,
        validation_status: ValidationStatus | None = None,
        validation_report: dict | None = None,
    ) -> None:
        with self._lock:
            record = self._jobs.get(job_id)
            if record is None:
                return
            if status is not None:
                record.status = status
            if name is not None:
                record.name = name
            if started_at is not None:
                record.started_at = started_at
            if finished_at is not None:
                record.finished_at = finished_at
            if result is not None:
                record.result = result
            if error is not None:
                record.error = error
            if objective_value is not None:
                record.objective_value = objective_value
            if validation_status is not None:
                record.validation_status = validation_status
            if validation_report is not None:
                record.validation_report = validation_report
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_store.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add app/store.py tests/test_store.py
git commit -m "feat(store): support name, objective, validation fields and listing"
```

---

### Task 4: Add validation wrapper

**Files:**
- Create: `app/validation.py`
- Test: `tests/test_validation.py`

- [ ] **Step 1: Write the failing test**

```python
from app.validation import validate_solution


def test_validate_solution_returns_expected_shape():
    instance = {"depot": {}, "orders": []}
    solution = {"vehicles": [], "loaders": []}
    result = validate_solution(instance, solution)
    assert isinstance(result["passed"], bool)
    assert "violations" in result
    assert "report" in result
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_validation.py::test_validate_solution_returns_expected_shape -v`
Expected: FAIL — module or function does not exist

- [ ] **Step 3: Implement validation wrapper**

```python
import json
import subprocess
from pathlib import Path
from typing import Any


def validate_solution(instance: dict[str, Any], solution: dict[str, Any]) -> dict[str, Any]:
    """Validate a solution against an instance.

    Tries to invoke the existing `validator.py` CLI first. Falls back to a
    minimal structural check if the CLI is unavailable.
    """
    workdir = Path("/tmp/routeopt_validation")
    workdir.mkdir(parents=True, exist_ok=True)
    input_path = workdir / "input.json"
    result_path = workdir / "result.json"
    input_path.write_text(json.dumps(instance))
    result_path.write_text(json.dumps(solution))

    try:
        subprocess.run(
            [
                "python",
                "validator.py",
                "--dir",
                str(workdir),
                "--input_file",
                "input",
                "--result_file",
                "result",
            ],
            check=True,
            capture_output=True,
            text=True,
            timeout=30,
        )
        return {
            "passed": True,
            "objective_value": solution.get("objective_value"),
            "violations": [],
            "report": {"detail": "Validator exited successfully"},
        }
    except subprocess.CalledProcessError as exc:
        return {
            "passed": False,
            "objective_value": solution.get("objective_value"),
            "violations": [exc.stderr or "Validation failed"],
            "report": {"stdout": exc.stdout, "stderr": exc.stderr},
        }
    except FileNotFoundError:
        violations = []
        if not solution.get("vehicles") and not solution.get("loaders"):
            violations.append("Solution contains no routes")
        return {
            "passed": len(violations) == 0,
            "objective_value": solution.get("objective_value"),
            "violations": violations,
            "report": {"fallback": True},
        }
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_validation.py::test_validate_solution_returns_expected_shape -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add app/validation.py tests/test_validation.py
git commit -m "feat(validation): add validate_solution wrapper"
```

---

### Task 5: Extract objective_value in runner and support auto-validate

**Files:**
- Modify: `app/runner.py`
- Test: `tests/test_runner.py`

- [ ] **Step 1: Write the failing test**

```python
import pytest

from app.schemas import JobStatus
from app.store import JobStore


@pytest.mark.asyncio
async def test_runner_extracts_objective_value(monkeypatch):
    from app import runner as runner_module

    def fake_solve(instance, seed):
        return {"objective_value": 99.5, "vehicles": []}

    monkeypatch.setattr(runner_module, "_solve_sync", fake_solve)

    store = JobStore()
    record = store.create_job({"orders": []}, seed=1)
    await runner_module.run_solver(record.job_id, store, auto_validate=False)

    updated = store.get_job(record.job_id)
    assert updated.status == JobStatus.COMPLETED
    assert updated.objective_value == 99.5
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_runner.py::test_runner_extracts_objective_value -v`
Expected: FAIL — `objective_value` not set or `run_solver` lacks parameter

- [ ] **Step 3: Update runner**

```python
import asyncio
import contextlib
import io
import traceback
from datetime import datetime, timezone

from app.schemas import JobStatus, ValidationStatus
from app.store import JobStore
from app.validation import validate_solution


def _solve_sync(instance: dict, seed: int) -> dict | None:
    import main_mvp

    return main_mvp.solve(instance, seed)


def _extract_objective_value(result: dict | None) -> float | None:
    if result is None:
        return None
    return result.get("objective_value")


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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_runner.py::test_runner_extracts_objective_value -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add app/runner.py tests/test_runner.py
git commit -m "feat(runner): extract objective_value and support auto-validate"
```

---

### Task 6: Extend SolverService

**Files:**
- Modify: `app/service.py`
- Test: `tests/test_service.py`

- [ ] **Step 1: Write the failing test**

```python
import pytest

from app.service import SolverService
from app.store import JobStore


@pytest.mark.asyncio
async def test_service_submits_job_with_name_and_auto_validate(monkeypatch):
    calls = {}

    async def fake_runner(job_id, store, *, auto_validate=False):
        calls["auto_validate"] = auto_validate
        store.update_job(job_id, status="completed", result={"objective_value": 1.0})

    store = JobStore()
    service = SolverService(store=store, runner=fake_runner)
    response = await service.submit_job({"orders": []}, seed=1, name="my-job", auto_validate=True)
    assert response.name == "my-job"
    assert calls["auto_validate"] is True


def test_service_lists_jobs():
    store = JobStore()
    service = SolverService(store=store)
    service.submit_job({"orders": []}, seed=1, name="a")
    service.submit_job({"orders": []}, seed=1, name="b")
    items, total = service.list_jobs(page=1, page_size=10)
    assert total == 2
    assert len(items) == 2
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_service.py -v`
Expected: FAIL — missing parameters/methods

- [ ] **Step 3: Extend service**

```python
import asyncio
from typing import Any, Callable, Coroutine

from app.runner import run_solver
from app.schemas import JobListResponse, JobResponse, SolveResponse, ValidationResponse
from app.store import JobStore
from app.validation import validate_solution as _validate_solution


class SolverService:
    def __init__(
        self,
        store: JobStore | None = None,
        runner: Callable[..., Coroutine[Any, Any, None]] | None = None,
    ) -> None:
        self._store = store or JobStore()
        self._runner = runner or run_solver

    async def submit_job(
        self,
        instance: dict,
        seed: int,
        *,
        name: str | None = None,
        auto_validate: bool = False,
    ) -> SolveResponse:
        record = self._store.create_job(instance, seed, name=name)
        asyncio.create_task(self._runner(record.job_id, self._store, auto_validate=auto_validate))
        return SolveResponse(
            job_id=record.job_id,
            status=record.status,
            created_at=record.created_at,
            name=record.name,
        )

    def get_job(self, job_id: str) -> JobResponse | None:
        record = self._store.get_job(job_id)
        if record is None:
            return None
        return JobResponse(
            job_id=record.job_id,
            status=record.status,
            name=record.name,
            created_at=record.created_at,
            started_at=record.started_at,
            finished_at=record.finished_at,
            result=record.result,
            error=record.error,
            objective_value=record.objective_value,
            validation_status=record.validation_status,
            validation_report=record.validation_report,
        )

    def list_jobs(
        self,
        *,
        page: int = 1,
        page_size: int = 25,
        sort_by: str = "created_at",
        sort_desc: bool = True,
    ) -> JobListResponse:
        records, total = self._store.list_jobs(
            page=page,
            page_size=page_size,
            sort_by=sort_by,
            sort_desc=sort_desc,
        )
        return JobListResponse(
            items=[self.get_job(record.job_id) for record in records],
            total=total,
            page=page,
            page_size=page_size,
        )

    def validate_solution(self, instance: dict, solution: dict) -> ValidationResponse:
        result = _validate_solution(instance, solution)
        return ValidationResponse(**result)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_service.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add app/service.py tests/test_service.py
git commit -m "feat(service): support name, listing, auto-validate and validation"
```

---

### Task 7: Add new API endpoints

**Files:**
- Modify: `app/api.py`
- Test: `tests/test_api.py`

- [ ] **Step 1: Write the failing tests**

```python
def test_list_jobs(client):
    client.post("/solve?seed=1&name=a", json={"orders": []})
    client.post("/solve?seed=1&name=b", json={"orders": []})
    response = client.get("/jobs")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 2


def test_validate_endpoint(client):
    response = client.post(
        "/validate",
        json={"instance": {"orders": []}, "solution": {"vehicles": [], "loaders": []}},
    )
    assert response.status_code == 200
    assert "passed" in response.json()


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_api.py::test_list_jobs tests/test_api.py::test_validate_endpoint tests/test_api.py::test_health_endpoint -v`
Expected: FAIL — 404s

- [ ] **Step 3: Implement endpoints**

```python
from fastapi import APIRouter, Body, HTTPException, Query

from app.schemas import JobListResponse, JobResponse, SolveResponse, ValidationRequest, ValidationResponse
from app.service import SolverService

router = APIRouter()
service = SolverService()


@router.post("/solve", response_model=SolveResponse, status_code=202)
async def solve(
    instance: dict = Body(...),
    seed: int = Query(default=42, ge=0),
    name: str | None = Query(default=None),
    auto_validate: bool = Query(default=False),
) -> SolveResponse:
    return await service.submit_job(
        instance,
        seed,
        name=name,
        auto_validate=auto_validate,
    )


@router.get("/jobs", response_model=JobListResponse)
async def list_jobs(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=100),
    sort_by: str = Query(default="created_at"),
    sort_desc: bool = Query(default=True),
) -> JobListResponse:
    return service.list_jobs(page=page, page_size=page_size, sort_by=sort_by, sort_desc=sort_desc)


@router.get("/jobs/{job_id}", response_model=JobResponse)
async def get_job(job_id: str) -> JobResponse:
    job = service.get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.post("/validate", response_model=ValidationResponse)
async def validate(payload: ValidationRequest) -> ValidationResponse:
    return service.validate_solution(payload.instance, payload.solution)


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_api.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add app/api.py tests/test_api.py
git commit -m "feat(api): add GET /jobs, POST /validate, GET /health"
```

---

### Task 8: Update Docker Compose and Dockerfile

**Files:**
- Modify: `docker-compose.yml`
- Modify: `Dockerfile`

- [ ] **Step 1: Update docker-compose.yml**

```yaml
version: "3.9"

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - PYTHONUNBUFFERED=1
      - CORS_ORIGINS=http://localhost:5173,http://localhost:3000
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 10s
      timeout: 5s
      retries: 5

  frontend:
    build: ./frontend
    ports:
      - "3000:80"
    depends_on:
      - api
```

- [ ] **Step 2: Update Dockerfile to include curl**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

- [ ] **Step 3: Verify compose syntax**

Run: `docker compose config`
Expected: exit 0, services `api` and `frontend` defined

- [ ] **Step 4: Commit**

```bash
git add docker-compose.yml Dockerfile
git commit -m "chore(docker): update compose for api+frontend, add curl for healthchecks"
```

---

### Task 9: Run full test suite

- [ ] **Step 1: Run backend tests**

Run: `pytest -v`
Expected: all tests pass

- [ ] **Step 2: Commit if any final fixes were needed**

```bash
git add -A
git commit -m "test: green suite after backend API extensions"
```

---

## Self-Review Checklist

- [x] Spec coverage: CORS, schemas, store, validation, runner, service, new endpoints, Docker updates all map to tasks.
- [x] No placeholders: every task has exact file paths, code, commands, expected output.
- [x] Type consistency: `JobRecord`, `JobResponse`, `SolveResponse`, `ValidationStatus`, and service methods use matching field names.

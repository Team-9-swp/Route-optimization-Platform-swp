# MVP v1 — code-first implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.
> **Important:** do **not** commit directly to `main`. Create issue-linked branches and open PRs for review.

**Goal:** Довести MVP v1 до рабочего состояния: бэкенд предоставляет полный API для фронтенда, фронтенд работает с реальными данными, оба сервиса поднимаются через Docker Compose, весь код покрыт тестами.

**Architecture:** FastAPI-бэкенд с in-memory `JobStore` расширяется до полноценного REST API (CORS, listing, validation, health). React-фронтенд переписывается с мок-данных на Axios + polling. Сервисы упаковываются в Docker Compose с nginx-фронтендом, проксирующим `/api` на бэкенд.

**Tech Stack:** Python 3.11, FastAPI, Pydantic, pytest; React 18 + TypeScript + Vite + Tailwind CSS; Docker Compose + nginx.

---

## Part 1: Backend (первый приоритет)

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
  ```bash
  .venv/Scripts/python -m pytest tests/test_api.py::test_cors_preflight -v
  ```
  Expected: FAIL — `access-control-allow-origin` missing.

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
          version="1.0.0",
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
  ```bash
  .venv/Scripts/python -m pytest tests/test_api.py::test_cors_preflight -v
  ```
  Expected: PASS.

- [ ] **Step 5: Open PR**
  ```bash
  git checkout -b <issue-number>-cors-middleware
  git add app/main.py tests/test_api.py
  git commit -m "feat(api): add configurable CORS middleware"
  git push origin <issue-number>-cors-middleware
  # open PR, request review
  ```

---

### Task 2: Expand Pydantic schemas

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
  ```bash
  .venv/Scripts/python -m pytest tests/test_schemas.py::test_job_record_accepts_name_and_validation_fields -v
  ```
  Expected: FAIL — fields do not exist.

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
  ```bash
  .venv/Scripts/python -m pytest tests/test_schemas.py -v
  ```

- [ ] **Step 5: Open PR**
  ```bash
  git checkout -b <issue-number>-expand-schemas
  git add app/schemas.py tests/test_schemas.py
  git commit -m "feat(schemas): add name, objective, validation and listing fields"
  git push origin <issue-number>-expand-schemas
  ```

---

### Task 3: Extend JobStore

**Files:**
- Modify: `app/store.py`
- Test: `tests/test_store.py`

- [ ] **Step 1: Write the failing test**
  ```python
  from app.schemas import JobStatus, ValidationStatus
  from app.store import JobStore

  def test_store_updates_extended_fields():
      store = JobStore()
      record = store.create_job({"orders": []}, seed=1, name="job-name")
      store.update_job(
          record.job_id,
          status=JobStatus.COMPLETED,
          objective_value=42.0,
          validation_status=ValidationStatus.PASSED,
          validation_report={"ok": True},
      )
      updated = store.get_job(record.job_id)
      assert updated.name == "job-name"
      assert updated.objective_value == 42.0
      assert updated.validation_status == ValidationStatus.PASSED

  def test_store_lists_jobs_sorted_by_created_at():
      store = JobStore()
      a = store.create_job({"orders": []}, seed=1)
      b = store.create_job({"orders": []}, seed=1)
      items, total = store.list_jobs(page=1, page_size=10)
      assert total == 2
      assert items[0].created_at >= items[1].created_at
  ```

- [ ] **Step 2: Run test to verify it fails**
  ```bash
  .venv/Scripts/python -m pytest tests/test_store.py -v
  ```
  Expected: FAIL.

- [ ] **Step 3: Extend store**
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
          sort_desc: bool = True,
      ) -> tuple[list[JobRecord], int]:
          with self._lock:
              records = list(self._jobs.values())
          records.sort(key=lambda r: r.created_at, reverse=sort_desc)
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
  ```bash
  .venv/Scripts/python -m pytest tests/test_store.py -v
  ```

- [ ] **Step 5: Open PR**

---

### Task 4: Add validation wrapper

**Files:**
- Create: `app/validation.py`
- Test: `tests/test_validation.py`

- [ ] **Step 1: Write the failing test**
  ```python
  from app.validation import validate_solution

  def test_validate_solution_returns_expected_shape():
      instance = {"depot": {"x": 0, "y": 0, "load_time": 0}, "orders": [], "weights": {}}
      solution = {"vehicles": [], "loaders": []}
      result = validate_solution(instance, solution)
      assert isinstance(result["passed"], bool)
      assert "violations" in result
      assert "report" in result
  ```

- [ ] **Step 2: Run test to verify it fails**
  ```bash
  .venv/Scripts/python -m pytest tests/test_validation.py::test_validate_solution_returns_expected_shape -v
  ```

- [ ] **Step 3: Implement validation wrapper**
  ```python
  from typing import Any
  from validator import validate_solution as _validate_solution

  def validate_solution(instance: dict[str, Any], solution: dict[str, Any]) -> dict[str, Any]:
      result = _validate_solution(instance, solution, quiet=True)
      violations = []
      for key, count in result["violations"].items():
          if count > 0:
              violations.append(f"{key}: {count}")
      return {
          "passed": result["total_violations"] == 0,
          "objective_value": result["total_cost"] if result["total_violations"] == 0 else None,
          "violations": violations,
          "report": result,
      }
  ```

- [ ] **Step 4: Run test to verify it passes**
  ```bash
  .venv/Scripts/python -m pytest tests/test_validation.py -v
  ```

- [ ] **Step 5: Open PR**

---

### Task 5: Extract objective_value and support auto-validate in runner

**Files:**
- Modify: `app/runner.py`
- Test: `tests/test_runner.py`

- [ ] **Step 1: Write the failing test**
  ```python
  import pytest
  from app.schemas import JobStatus, ValidationStatus
  from app.store import JobStore

  @pytest.mark.asyncio
  async def test_runner_extracts_objective_value(monkeypatch):
      from app import runner as runner_module

      def fake_solve(instance, seed):
          return {"objective_value": 99.5, "vehicles": [], "loaders": []}

      monkeypatch.setattr(runner_module, "_solve_sync", fake_solve)
      store = JobStore()
      record = store.create_job({"orders": []}, seed=1)
      await runner_module.run_solver(record.job_id, store, auto_validate=False)

      updated = store.get_job(record.job_id)
      assert updated.status == JobStatus.COMPLETED
      assert updated.objective_value == 99.5
  ```

- [ ] **Step 2: Run test to verify it fails**
  ```bash
  .venv/Scripts/python -m pytest tests/test_runner.py::test_runner_extracts_objective_value -v
  ```

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

      store.update_job(job_id, status=JobStatus.RUNNING, started_at=datetime.now(timezone.utc))

      try:
          stdout_capture = io.StringIO()
          with contextlib.redirect_stdout(stdout_capture):
              result = await asyncio.to_thread(_solve_sync, record.input_data, record.seed)

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
  ```bash
  .venv/Scripts/python -m pytest tests/test_runner.py -v
  ```

- [ ] **Step 5: Open PR**

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
          store.update_job(job_id, status="completed", result={"objective_value": 1.0, "vehicles": [], "loaders": []})

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
      response = service.list_jobs(page=1, page_size=10)
      assert response.total == 2
      assert len(response.items) == 2
  ```

- [ ] **Step 2: Run test to verify it fails**
  ```bash
  .venv/Scripts/python -m pytest tests/test_service.py -v
  ```

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
          sort_desc: bool = True,
      ) -> JobListResponse:
          records, total = self._store.list_jobs(page=page, page_size=page_size, sort_desc=sort_desc)
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
  ```bash
  .venv/Scripts/python -m pytest tests/test_service.py -v
  ```

- [ ] **Step 5: Open PR**

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
          json={"instance": {"depot": {"x": 0, "y": 0, "load_time": 0}, "orders": [], "weights": {}},
                "solution": {"vehicles": [], "loaders": []}},
      )
      assert response.status_code == 200
      assert "passed" in response.json()

  def test_health_endpoint(client):
      response = client.get("/health")
      assert response.status_code == 200
      assert response.json()["status"] == "ok"
  ```

- [ ] **Step 2: Run tests to verify they fail**
  ```bash
  .venv/Scripts/python -m pytest tests/test_api.py::test_list_jobs tests/test_api.py::test_validate_endpoint tests/test_api.py::test_health_endpoint -v
  ```

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
      return await service.submit_job(instance, seed, name=name, auto_validate=auto_validate)

  @router.get("/jobs", response_model=JobListResponse)
  async def list_jobs(
      page: int = Query(default=1, ge=1),
      page_size: int = Query(default=25, ge=1, le=100),
      sort_desc: bool = Query(default=True),
  ) -> JobListResponse:
      return service.list_jobs(page=page, page_size=page_size, sort_desc=sort_desc)

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
  ```bash
  .venv/Scripts/python -m pytest tests/test_api.py -v
  ```

- [ ] **Step 5: Open PR**

---

### Task 8: Stabilize e2e test

**Files:**
- Modify: `tests/test_e2e.py`

- [ ] **Step 1: Replace large instance with tiny synthetic instance**
  ```python
  @pytest.mark.asyncio
  async def test_solve_t1_instance(client):
      instance = {
          "vehicle_capacity": 100,
          "vehicle_speed": 1,
          "loader_speed": 1,
          "vehicle_shift_size": 1000,
          "loader_shift_size": 1000,
          "depot": {"x": 0, "y": 0, "load_time": 0},
          "orders": [
              {"id": 1, "x": 3, "y": 4, "volume": 10, "time_window": [0, 100],
               "vehicle_service_time": 5, "loader_cnt": 0, "loader_service_time": 0, "optional": 0},
              {"id": 2, "x": 6, "y": 8, "volume": 5, "time_window": [0, 100],
               "vehicle_service_time": 5, "loader_cnt": 0, "loader_service_time": 0, "optional": 0},
          ],
          "weights": {
              "vehicle_salary": 1, "loader_salary": 1, "fuel_cost": 1,
              "loader_work": 1, "optional_order_penalty": 1,
          },
      }
      response = await client.post("/solve?seed=42", json=instance)
      assert response.status_code == 202
      job_id = response.json()["job_id"]

      for _ in range(60):
          response = await client.get(f"/jobs/{job_id}")
          data = response.json()
          if data["status"] in ("completed", "failed"):
              break
          await asyncio.sleep(0.1)

      assert response.status_code == 200
      data = response.json()
      assert data["status"] == "completed"
      assert "vehicles" in data["result"]
      assert "loaders" in data["result"]
  ```

- [ ] **Step 2: Run test**
  ```bash
  .venv/Scripts/python -m pytest tests/test_e2e.py -v
  ```

- [ ] **Step 3: Open PR**

---

## Part 2: Frontend (второй приоритет)

### Task 9: Add API client and types

**Files:**
- Create: `frontend/src/types/index.ts`
- Create: `frontend/src/api/client.ts`
- Create: `frontend/src/api/jobs.ts`
- Create: `frontend/src/api/validate.ts`
- Modify: `frontend/package.json`
- Modify: `frontend/vite.config.ts`

- [ ] **Step 1: Install axios**
  ```bash
  cd frontend
  npm install axios
  npm install -D @types/node
  ```

- [ ] **Step 2: Add types**
  ```typescript
  // frontend/src/types/index.ts
  export type JobStatus = "pending" | "running" | "completed" | "failed";
  export type ValidationStatus = "pending" | "passed" | "failed";

  export interface Job {
    job_id: string;
    status: JobStatus;
    name?: string;
    created_at: string;
    started_at?: string;
    finished_at?: string;
    result?: Record<string, unknown>;
    error?: string;
    objective_value?: number;
    validation_status?: ValidationStatus;
    validation_report?: Record<string, unknown>;
    seed?: number;
  }

  export interface JobListResponse {
    items: Job[];
    total: number;
    page: number;
    page_size: number;
  }

  export interface SolveResponse {
    job_id: string;
    status: JobStatus;
    created_at: string;
    name?: string;
  }

  export interface ValidationResponse {
    passed: boolean;
    objective_value?: number;
    violations: string[];
    report: Record<string, unknown>;
  }
  ```

- [ ] **Step 3: Add API client**
  ```typescript
  // frontend/src/api/client.ts
  import axios from "axios";
  export const api = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL || "/api",
    headers: { "Content-Type": "application/json" },
  });
  ```

- [ ] **Step 4: Add job API functions**
  ```typescript
  // frontend/src/api/jobs.ts
  import { api } from "./client";
  import type { Job, JobListResponse, SolveResponse } from "../types";

  export async function submitJob(
    instance: Record<string, unknown>,
    options: { seed?: number; name?: string; autoValidate?: boolean } = {},
  ): Promise<SolveResponse> {
    const params = new URLSearchParams();
    if (options.seed !== undefined) params.set("seed", String(options.seed));
    if (options.name) params.set("name", options.name);
    if (options.autoValidate) params.set("auto_validate", "true");
    const { data } = await api.post<SolveResponse>(`/solve?${params.toString()}`, instance);
    return data;
  }

  export async function getJob(jobId: string): Promise<Job> {
    const { data } = await api.get<Job>(`/jobs/${jobId}`);
    return data;
  }

  export async function listJobs(): Promise<JobListResponse> {
    const { data } = await api.get<JobListResponse>("/jobs");
    return data;
  }
  ```

- [ ] **Step 5: Add validation API function**
  ```typescript
  // frontend/src/api/validate.ts
  import { api } from "./client";
  import type { ValidationResponse } from "../types";

  export async function validateSolution(
    instance: Record<string, unknown>,
    solution: Record<string, unknown>,
  ): Promise<ValidationResponse> {
    const { data } = await api.post<ValidationResponse>("/validate", { instance, solution });
    return data;
  }
  ```

- [ ] **Step 6: Configure Vite proxy**
  ```typescript
  // frontend/vite.config.ts
  import { defineConfig } from "vite";
  import path from "path";
  import tailwindcss from "@tailwindcss/vite";
  import react from "@vitejs/plugin-react";

  export default defineConfig({
    plugins: [react(), tailwindcss()],
    resolve: {
      alias: { "@": path.resolve(__dirname, "./src") },
    },
    assetsInclude: ["**/*.svg", "**/*.csv"],
    server: {
      proxy: {
        "/api": {
          target: process.env.VITE_API_BASE_URL || "http://localhost:8000",
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api/, ""),
        },
      },
    },
  });
  ```

- [ ] **Step 7: Type-check**
  ```bash
  cd frontend
  npx tsc --noEmit
  ```

- [ ] **Step 8: Open PR**

---

### Task 10: Wire Dashboard to real API

**Files:**
- Modify: `frontend/src/app/components/Dashboard.tsx`

- [ ] **Step 1: Replace static `jobs` array with state + effect**
  ```tsx
  import { useEffect, useState } from "react";
  import { listJobs } from "../api/jobs";
  import type { Job } from "../types";

  export function Dashboard({ navigate }: Props) {
    const [jobs, setJobs] = useState<Job[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
      let cancelled = false;
      async function load() {
        try {
          const response = await listJobs();
          if (!cancelled) setJobs(response.items);
        } catch (err) {
          if (!cancelled) setError(err instanceof Error ? err.message : "Failed to load jobs");
        } finally {
          if (!cancelled) setIsLoading(false);
        }
      }
      load();
      const interval = setInterval(load, 2000);
      return () => {
        cancelled = true;
        clearInterval(interval);
      };
    }, []);

    if (isLoading) return <p>Loading jobs...</p>;
    if (error) return <p className="text-red-600">{error}</p>;
    // ... render table using real jobs data
  }
  ```

- [ ] **Step 2: Adapt table columns to real `Job` fields**
  - `job.job_id.slice(0, 8)`
  - `job.name || "—"`
  - `job.status`
  - `new Date(job.created_at).toLocaleString()`
  - `job.objective_value ?? "—"`
  - Link to `job-detail` uses `job.job_id`

- [ ] **Step 3: Type-check and dev test**
  ```bash
  cd frontend
  npx tsc --noEmit
  npm run dev
  ```
  - Verify Dashboard loads real jobs (need running backend).

- [ ] **Step 4: Open PR**

---

### Task 11: Wire NewJob to real API

**Files:**
- Modify: `frontend/src/app/components/NewJob.tsx`

- [ ] **Step 1: Replace fake submit with real API call**
  ```tsx
  import { submitJob } from "../api/jobs";

  async function handleSubmit() {
    setError("");
    if (!json.trim()) {
      setError("Please provide Instance JSON before running the solver.");
      return;
    }
    let instance: Record<string, unknown>;
    try {
      instance = JSON.parse(json);
    } catch {
      setError("Invalid JSON — please check the Instance JSON field.");
      return;
    }
    setSubmitting(true);
    try {
      const response = await submitJob(instance, {
        seed: Number(seed) || 42,
        name: name || undefined,
        autoValidate,
      });
      navigate({ name: "job-detail", id: response.job_id });
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to submit job");
    } finally {
      setSubmitting(false);
    }
  }
  ```

- [ ] **Step 2: Fix the placeholder JSON format**
  - Replace with a valid instance matching the solver schema (`vehicle_capacity`, `vehicle_speed`, `loader_speed`, `vehicle_shift_size`, `loader_shift_size`, `depot`, `orders`, `weights`).

- [ ] **Step 3: Type-check and test**
  ```bash
  cd frontend
  npx tsc --noEmit
  npm run dev
  ```

- [ ] **Step 4: Open PR**

---

### Task 12: Wire JobDetail to real API

**Files:**
- Modify: `frontend/src/app/components/JobDetail.tsx`

- [ ] **Step 1: Fetch real job with polling**
  ```tsx
  import { useEffect, useState } from "react";
  import { getJob } from "../api/jobs";
  import type { Job } from "../types";

  export function JobDetail({ id, navigate }: Props) {
    const [job, setJob] = useState<Job | null>(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [activeTab, setActiveTab] = useState<Tab>("Routes");

    useEffect(() => {
      let cancelled = false;
      async function load() {
        try {
          const data = await getJob(id);
          if (!cancelled) {
            setJob(data);
            setIsLoading(false);
          }
        } catch (err) {
          if (!cancelled) {
            setError(err instanceof Error ? err.message : "Job not found");
            setIsLoading(false);
          }
        }
      }
      load();
      const interval = setInterval(() => {
        if (job?.status === "completed" || job?.status === "failed") {
          clearInterval(interval);
          return;
        }
        load();
      }, 1000);
      return () => {
        cancelled = true;
        clearInterval(interval);
      };
    }, [id, job?.status]);

    if (isLoading) return <p>Loading job...</p>;
    if (error || !job) return <p className="text-red-600">{error || "Job not found"}</p>;
    // ... render
  }
  ```

- [ ] **Step 2: Render real data**
  - Header: `job.name || "Untitled job"`, `job.job_id`, `job.seed`, `job.objective_value`, `job.validation_status`.
  - Routes tab: `job.result?.vehicles`, `job.result?.loaders`.
  - Validation tab: `job.validation_report`.
  - Raw JSON tab: `job.result`.

- [ ] **Step 3: Type-check and test**
  ```bash
  cd frontend
  npx tsc --noEmit
  npm run dev
  ```

- [ ] **Step 4: Open PR**

---

### Task 13: Wire Validate page to real API

**Files:**
- Modify: `frontend/src/app/components/Validate.tsx`

- [ ] **Step 1: Replace fake validate with real API call**
  ```tsx
  import { useState } from "react";
  import { validateSolution } from "../api/validate";
  import type { ValidationResponse } from "../types";

  export function Validate() {
    const [instanceJson, setInstanceJson] = useState("");
    const [solutionJson, setSolutionJson] = useState("");
    const [validating, setValidating] = useState(false);
    const [result, setResult] = useState<ValidationResponse | null>(null);
    const [parseError, setParseError] = useState("");

    async function handleValidate() {
      setParseError("");
      setResult(null);
      if (!instanceJson.trim() || !solutionJson.trim()) {
        setParseError("Both Instance JSON and Solution JSON are required.");
        return;
      }
      let instance: Record<string, unknown>;
      let solution: Record<string, unknown>;
      try {
        instance = JSON.parse(instanceJson);
      } catch {
        setParseError("Instance JSON is not valid JSON.");
        return;
      }
      try {
        solution = JSON.parse(solutionJson);
      } catch {
        setParseError("Solution JSON is not valid JSON.");
        return;
      }
      setValidating(true);
      try {
        const data = await validateSolution(instance, solution);
        setResult(data);
      } catch (err) {
        setParseError(err instanceof Error ? err.message : "Validation failed");
      } finally {
        setValidating(false);
      }
    }
    // ... render result from real API
  }
  ```

- [ ] **Step 2: Type-check and test**
  ```bash
  cd frontend
  npx tsc --noEmit
  npm run dev
  ```

- [ ] **Step 3: Open PR**

---

## Part 3: Docker Compose (третий приоритет)

### Task 14: Add frontend Dockerfile and nginx config

**Files:**
- Create: `frontend/Dockerfile`
- Create: `frontend/nginx.conf`

- [ ] **Step 1: Create `frontend/Dockerfile`**
  ```dockerfile
  FROM node:20-alpine AS builder
  WORKDIR /app
  COPY package*.json ./
  RUN npm ci
  COPY . .
  RUN npm run build

  FROM nginx:alpine
  COPY --from=builder /app/dist /usr/share/nginx/html
  COPY nginx.conf /etc/nginx/conf.d/default.conf
  EXPOSE 80
  CMD ["nginx", "-g", "daemon off;"]
  ```

- [ ] **Step 2: Create `frontend/nginx.conf`**
  ```nginx
  server {
    listen 80;
    server_name localhost;

    location / {
      root /usr/share/nginx/html;
      try_files $uri $uri/ /index.html;
    }

    location /api/ {
      proxy_pass http://api:8000/;
      proxy_set_header Host $host;
      proxy_set_header X-Real-IP $remote_addr;
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
  }
  ```

- [ ] **Step 3: Verify frontend builds locally**
  ```bash
  cd frontend
  npm run build
  ```

- [ ] **Step 4: Open PR**

---

### Task 15: Update root Dockerfile and docker-compose.yml

**Files:**
- Modify: `Dockerfile`
- Modify: `docker-compose.yml`

- [ ] **Step 1: Update `Dockerfile`**
  Add `curl` for healthchecks:
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

- [ ] **Step 2: Update `docker-compose.yml`**
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

- [ ] **Step 3: Validate compose config**
  ```bash
  docker compose config
  ```

- [ ] **Step 4: Smoke test**
  ```bash
  docker compose up --build -d
  curl http://localhost:8000/health
  curl http://localhost:3000
  docker compose down
  ```

- [ ] **Step 5: Open PR**

---

## Part 4: Documentation (последний приоритет)

### Task 16: Update README.md

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Update quick start**
  - Указать, что `docker compose up --build` поднимает и API, и фронтенд.
  - Ссылки: `http://localhost:8000/docs` и `http://localhost:3000`.

- [ ] **Step 2: Update local development**
  - Backend: `python -m uvicorn app.main:app --reload`
  - Frontend: `cd frontend && npm install && npm run dev`
  - Указать, что Vite проксирует `/api` на `localhost:8000`.

- [ ] **Step 3: Open PR**

---

### Task 17: Update CHANGELOG.md for MVP v1

**Files:**
- Modify: `CHANGELOG.md`

- [ ] **Step 1: Add `## [1.0.0] - <date>` section**
  ```markdown
  ## [1.0.0] - 2026-06-XX

  ### Added
  - CORS middleware for frontend integration
  - `GET /jobs`, `POST /validate`, `GET /health` endpoints
  - Job name, objective value, and validation status tracking
  - React frontend connected to real API (Dashboard, New Job, Job Detail, Validate)
  - Docker Compose setup with `api` and `frontend` services
  - Full solution validator (`validator.py`)

  ### Changed
  - `POST /solve` accepts optional `name` and `auto_validate` parameters
  ```

- [ ] **Step 2: Open PR**

---

### Task 18: Sync docs/user-stories.md with current state

**Files:**
- Modify: `docs/user-stories.md`

- [ ] **Step 1: Update Work Status for implemented stories**
  - US-01a, US-01b, US-02, US-03, US-04 → `Done`
  - Остальные активные → `To Do` или `Ready` по факту.

- [ ] **Step 2: Add supporting PBIs**
  - PBI-01 API extensions
  - PBI-02 CORS middleware
  - PBI-03 Frontend Dashboard
  - PBI-04 Frontend New Job
  - PBI-05 Frontend Job Detail
  - PBI-06 Docker Compose api+frontend
  - PBI-07 Release v1.0.0

- [ ] **Step 3: Open PR**

---

### Task 19: Create docs/roadmap.md

**Files:**
- Create: `docs/roadmap.md`

- [ ] **Step 1: Write roadmap**
  - Current Sprint: MVP v1 — API + frontend + Docker.
  - Next Sprint: MVP v2 — persistent storage, advanced visualization, skipped optional orders report.
  - Future: MVP v3 — auth, multi-tenancy, benchmarking.

- [ ] **Step 2: Open PR**

---

### Task 20: Create reports/week3/ structure

**Files:**
- Create: `reports/week3/README.md`
- Create: `reports/week3/customer-review-summary.md`
- Create: `reports/week3/reflection.md`
- Create: `reports/week3/retrospective.md`
- Create: `reports/week3/llm-report.md`
- Create: `reports/week3/images/`

- [ ] **Step 1: Fill `reports/week3/README.md`**
  - Все обязательные пункты из Assignment 3.
  - Contribution traceability table.
  - Скриншоты из `reports/week3/images/`.

- [ ] **Step 2: Fill remaining files**
  - `customer-review-summary.md`: дата, участники, scope, feedback, approvals, action points.
  - `reflection.md`: learning points, validated assumptions, friction and gaps, planned response.
  - `retrospective.md`: 3 хороших, 3 плохих, 1–2 action points.
  - `llm-report.md`: использование AI/LLM.

- [ ] **Step 3: Open PR**

---

## Final verification checklist

- [ ] All backend tests pass: `.venv/Scripts/python -m pytest -v`
- [ ] Frontend type-check passes: `cd frontend && npx tsc --noEmit`
- [ ] Frontend build passes: `cd frontend && npm run build`
- [ ] Docker Compose smoke test passes
- [ ] All required endpoints work:
  - `POST /solve?name=...&auto_validate=true`
  - `GET /jobs`
  - `GET /jobs/{id}`
  - `POST /validate`
  - `GET /health`
- [ ] Frontend Dashboard shows real jobs
- [ ] Frontend New Job creates a job and redirects to Job Detail
- [ ] Frontend Job Detail polls until completed and shows routes/validation/raw JSON
- [ ] Frontend Validate page calls `/validate` and shows real result
- [ ] CHANGELOG updated for v1.0.0
- [ ] README updated with run/deployment instructions

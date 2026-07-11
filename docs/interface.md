# Route Optimization Platform — Interface Documentation

## Interface type

The product exposes two interfaces:

1. **Web user interface (primary interface)** — a React + TypeScript single-page application for dispatchers and managers. The interactive prototype is published on Figma.
2. **REST API (supporting)** — a FastAPI service that the web UI consumes. The API can also be used directly by technical users and integrations.

The current increment (`v1.3.0` / MVP v2) implements the React web UI and the REST API, with PostgreSQL-backed persistent job history, solution export, standalone validation, and a health endpoint. The Figma prototype remains the original design reference.

### Interactive prototype

A clickable Figma prototype of the web interface is available here:

**[Figma prototype — Route Optimizer](https://carry-race-78764713.figma.site/)**

The prototype demonstrates the four main screens and the navigation between them:

1. **Dashboard** — browse recent optimization jobs with status badges and quick actions.
2. **New Job** — upload or paste a JSON instance, set the seed and job name, and start the solver.
3. **Job Detail** — view job status, objective value, validation result, route map, route tables, and raw JSON.
4. **Validate** — submit an instance and a solution to check constraints and objective value.

The Figma file is publicly viewable (not editable) and will remain accessible until the course has been graded.

## Intended users

- **Dispatcher / logistics manager** — uses the web UI to upload problem instances, run the solver, view routes on a map, and validate results.
- **Developer / technical user** — uses the REST API or Swagger UI to submit jobs and retrieve solutions programmatically.

## Web interface

### Pages and navigation

| Page | Route | Purpose |
|------|-------|---------|
| Dashboard | `/` | Browse recent optimization jobs and their status. |
| New Job | `/jobs/new` | Upload or paste a JSON instance, set seed and job name, start the solver. |
| Job Detail | `/jobs/:id` | View job status, objective value, validation result, route map, route tables, and raw JSON. |
| Validate | `/validate` | Upload an instance and a solution to run the validator independently. |
| API Docs | external `/docs` | Link to FastAPI Swagger UI. |

### Key workflows

#### Submit a new optimization job

1. Open **New Job**.
2. Upload a JSON instance file or paste the JSON into the textarea.
3. Optionally set a job name and seed.
4. Optionally enable auto-validate.
5. Click **Run Solver**.
6. The UI redirects to **Job Detail** and polls the job status until it completes.

#### View routes on a map

1. Open a completed job on **Job Detail**.
2. The map shows the depot, order locations, vehicle routes as colored polylines, and loader routes as dashed polylines.
3. Switch to the **Routes** tab for detailed vehicle and loader route tables.

#### Validate a solution

1. Open **Validate**.
2. Paste the instance JSON and the solution JSON.
3. Click **Validate**.
4. The UI shows whether the solution passed, the objective value, and any constraint violations.

## REST API

### Base URL

- Local development: `http://localhost:8000`
- Hosted university VM: `http://10.93.26.188:8000` (accessible from the university network)
- In Docker Compose the API is reachable at `http://api:8000` from the frontend service.

### Authentication

No authentication is required in the current course increment.

### Endpoints

#### `POST /solve`

Submit a problem instance to the solver.

**Query parameters:**

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `seed` | integer | `42` | Random seed for reproducible runs. |
| `time_limit` | number | backend default | Solver wall-clock budget in seconds (must be > 0). |
| `name` | string | — | Optional human-readable job name. |
| `auto_validate` | boolean | `false` | Validate the solution automatically once the solver finishes. |

**Request body:** raw instance JSON (see `Assignment_02.md` for the input format).

**Response (202 Accepted):**

```json
{
  "job_id": "0192c6a0-...",
  "status": "pending",
  "created_at": "2026-06-13T13:00:00Z"
}
```

**Error example (422 Unprocessable Entity):**

```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body"],
      "msg": "Field required"
    }
  ]
}
```

#### `GET /jobs/{job_id}`

Retrieve a job by ID.

**Response (200 OK) for a completed job:**

```json
{
  "job_id": "0192c6a0-...",
  "status": "completed",
  "created_at": "2026-06-13T13:00:00Z",
  "started_at": "2026-06-13T13:00:01Z",
  "finished_at": "2026-06-13T13:00:05Z",
  "result": {
    "vehicles": [...],
    "loaders": [...]
  },
  "error": null
}
```

**Response (404 Not Found):**

```json
{
  "detail": "Job not found"
}
```

#### `GET /jobs`

List submitted jobs (paginated).

**Query parameters:** `page` (default 1), `page_size` (default 25), `sort_desc` (default true).

**Response (200 OK):** `{ "items": [JobResponse, ...], "total", "page", "page_size" }`.

#### `POST /validate`

Validate an instance/solution pair independently of the solver.

**Request body:** `{ "instance": <instance JSON>, "solution": { "vehicles": [...], "loaders": [...] } }`.

**Response (200 OK):** `{ "passed": true, "objective_value": <number>, "violations": [], "report": {...} }`. A failing solution returns `passed: false` with a list of violation strings in `violations`.

#### `GET /jobs/{job_id}/solution` and `GET /jobs/{job_id}/export`

Return a validator-compatible solution (`vehicles`, `loaders`, `unserved_optional`) for a completed job, dropping internal-only fields. Returns `404` for a missing job and `400` for a non-completed job. (`/solution` is the canonical path; `/export` is kept as an alias.)

#### `GET /health`

Liveness probe used by deployment and Docker health checks.

**Response (200 OK):** `{ "status": "ok" }`.

### OpenAPI and Postman artifacts

- OpenAPI specification: [`api/openapi.yaml`](../api/openapi.yaml)
- Postman collection: [`api/postman_collection.json`](../api/postman_collection.json)
- Rendered Swagger UI: `http://localhost:8000/docs`

## Input and output formats

The solver accepts the JSON instance format described in `Assignment_02.md` and produces a JSON solution with `vehicles` and `loaders` arrays. See `Assignment_02.md` / `sec4.md` for field definitions.

## Configuration

- `CORS_ORIGINS` — comma-separated list of origins allowed to call the API from a browser.

## Implemented vs. planned

| Capability | MVP v1 | MVP v2 (`v1.3.0`, current) |
|------------|--------|----------------------------|
| `POST /solve` (with `seed`, `time_limit`, `name`, `auto_validate`) | Implemented | Implemented |
| `GET /jobs/{job_id}` (with `loaders`, `unserved_optional`) | Implemented | Implemented |
| `GET /jobs` listing | Implemented | Implemented |
| `POST /validate` | Implemented | Implemented |
| `GET /health` | Implemented | Implemented |
| `GET /jobs/{job_id}/solution` and `/export` | — | Implemented |
| Web UI (Dashboard, New Job, Job Detail with route map, Validate) | Implemented (React SPA) | Implemented |
| Persistent PostgreSQL storage | Implemented | Implemented |
| Gantt schedule view on Job Detail | — | In progress (Assignment 6 Sprint 4) |

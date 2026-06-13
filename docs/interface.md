# Route Optimization Platform — Interface Documentation

## Interface type

The product exposes two interfaces:

1. **Web user interface (primary interface for MVP v1)** — a React + TypeScript single-page application for dispatchers and managers. The interactive prototype is published on Figma.
2. **REST API (supporting)** — a FastAPI service that the web UI consumes. The API can also be used directly by technical users and integrations.

The current MVP v0 implements the REST API. The web UI is in design (Figma prototype) and will be implemented in the next iteration.

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

No authentication is required in MVP v0 and the initial MVP v1 iteration.

### Endpoints

#### `POST /solve`

Submit a problem instance to the solver.

**Query parameters:**

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `seed` | integer | `42` | Random seed for reproducible runs. |

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

### OpenAPI and Postman artifacts

- OpenAPI specification: [`api/openapi.yaml`](../api/openapi.yaml)
- Postman collection: [`api/postman_collection.json`](../api/postman_collection.json)
- Rendered Swagger UI: `http://localhost:8000/docs`

## Input and output formats

The solver accepts the JSON instance format described in `Assignment_02.md` and produces a JSON solution with `vehicles` and `loaders` arrays. See `Assignment_02.md` / `sec4.md` for field definitions.

## Configuration

- `CORS_ORIGINS` — comma-separated list of origins allowed to call the API from a browser.

## Implemented vs. planned

| Capability | MVP v0 | MVP v1 (planned) |
|------------|--------|------------------|
| `POST /solve` | Implemented | Implemented |
| `GET /jobs/{job_id}` | Implemented | Implemented |
| `GET /jobs` listing | Not implemented | Planned |
| `POST /validate` | Not implemented | Planned |
| `GET /health` | Not implemented | Planned |
| Web UI prototype | Figma prototype | Implemented as React app in MVP v1 |
| Persistent storage | Not implemented | Planned (PostgreSQL) |

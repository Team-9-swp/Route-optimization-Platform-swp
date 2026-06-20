# Route Optimization Frontend Design

Date: 2026-06-13
Topic: Full-featured React frontend for the Route Optimization Platform

## Goal

Replace the current CLI-only interface with a browser-based frontend that allows logistics dispatchers and managers to upload problem instances, run the solver, view optimized vehicle and loader routes on an interactive map, validate results, and browse the history of optimization jobs.

## Background

The project already contains:

- `main_mvp.py` — a CVRPTW solver that accepts a JSON instance and returns routes.
- `app/` — a FastAPI microservice exposing `POST /solve` and `GET /jobs/{job_id}`.
- `validator.py` — an existing validator that checks solutions.
- `test_cases/` and `instances/` — sample JSON instances.

The frontend will be built as a separate React + TypeScript application that communicates with the existing FastAPI backend.

## Chosen Approach

**Immediate iteration:** Separate React frontend + FastAPI backend with the current in-memory job store.

**Planned iteration:** Add PostgreSQL persistence so jobs survive API restarts and enable richer history/dashboard features.

Reasons:

- Clean separation between UI and computation.
- React ecosystem provides excellent data visualization libraries (Leaflet, Recharts).
- We can build and test the UI immediately without forcing a database migration.
- PostgreSQL will be introduced later with SQLAlchemy + Alembic.

## Architecture (Immediate)

```
┌─────────────────┐      HTTP/REST       ┌─────────────────┐
│   React SPA     │  <────────────────>  │   FastAPI API   │
│   (frontend/)   │                      │   (app/)        │
│                 │                      │ In-memory store │
└─────────────────┘                      └─────────────────┘
```

## Architecture (Planned)

```
┌─────────────────┐      HTTP/REST       ┌─────────────────┐
│   React SPA     │  <────────────────>  │   FastAPI API   │
│   (frontend/)   │                      │   (app/)        │
└─────────────────┘                      └────────┬────────┘
                                                  │
                                                  │ SQLAlchemy
                                                  ▼
                                         ┌─────────────────┐
                                         │   PostgreSQL    │
                                         └─────────────────┘
```

## Tech Stack

- **Frontend:** React 18, TypeScript, Vite, React Router, TanStack Query (React Query), Axios
- **UI Library:** Tailwind CSS, Headless UI or Radix UI for accessible components
- **Map Visualization:** Leaflet with `react-leaflet`
- **Charts/Tables:** Recharts or TanStack Table
- **Backend:** Existing FastAPI app (Python) with in-memory store
- **Future persistence:** SQLAlchemy 2.x, Alembic, PostgreSQL 16
- **Deployment:** Docker Compose with `api` and `frontend` services; PostgreSQL added later

## Environment Variables

| Variable | Used By | Default | Purpose |
|----------|---------|---------|---------|
| `CORS_ORIGINS` | API | `http://localhost:5173,http://localhost:3000` | Comma-separated allowed origins |
| `LOG_LEVEL` | API | `info` | Uvicorn / app log level |
| `VITE_API_BASE_URL` | Frontend | `http://localhost:8000` | Base URL for Axios in dev |
| `NODE_ENV` | Frontend | `development` | Build mode |

Future (PostgreSQL):

| Variable | Used By | Default | Purpose |
|----------|---------|---------|---------|
| `DATABASE_URL` | API | `postgresql+asyncpg://routeopt:routeopt@postgres/routeopt` | Async SQLAlchemy connection string |

Vite will proxy `/api` to the backend in development so the frontend can call relative paths.

## Frontend Pages

### 1. Dashboard (`/`)

- Table of all optimization jobs known to the backend.
- Columns: ID, name, created at, status, vehicles, loaders, objective, actions.
- Quick action buttons: "New Job", "Validate".
- Auto-refresh running jobs every 2 seconds with exponential backoff up to 10 seconds.
- **Limitation in immediate iteration:** jobs are lost when the API process restarts.

### 2. New Job (`/jobs/new`)

- File dropzone for JSON instance upload.
- Textarea for pasting JSON directly.
- Inputs: seed, optional job name.
- Checkbox: auto-validate after solve.
- Submit button starts job and redirects to Job Detail.

### 3. Job Detail (`/jobs/:id`)

- Header: job ID, name, seed, status, timestamps.
- Summary card: vehicles count, loaders count, objective value, validation status.
- Interactive map: depot marker, order markers, colored polylines for vehicle routes.
- Loader route representation: dashed polylines in a secondary color and a dedicated "Loader Routes" table.
- Tabs:
  - **Routes:** vehicle and loader route tables.
  - **Validation:** validator output, violations list, objective breakdown.
  - **Raw JSON:** formatted input instance and output solution.
- Actions: download result JSON, re-run with same instance.
- Polling every 1 second while status is `pending` or `running`.

### 4. Validate (`/validate`)

- Upload instance JSON and solution JSON.
- Run validator via `POST /validate`.
- Show validation report: pass/fail, violations, objective value.

### 5. API Docs (`/docs` external or `/api-docs`)

- Link to FastAPI Swagger UI (`/docs`) opened in a new tab.

## Backend Changes (Immediate)

### Dependencies

No new Python dependencies are required for the immediate iteration beyond what is already installed.

### CORS

Configure `CORSMiddleware` in `app/main.py` with origins from `CORS_ORIGINS` so the Vite dev server and production frontend can call the API.

### API Endpoints

Keep existing:

- `POST /solve?seed=42&auto_validate=true` — accepts instance JSON as body, creates job, returns `SolveResponse`.
- `GET /jobs/{job_id}` — returns full job record including `name`, `objective_value`, `validation_status`, `validation_report`.

Add:

- `GET /jobs?page=1&page_size=25&sort_by=created_at&sort_desc=true` — list jobs from the in-memory store with pagination and sorting.
- `POST /validate` — accepts `{instance, solution}`, runs the existing `validator.py`, returns `{passed, objective_value, violations, report}`.
- `GET /health` — health check.

### Error Response Shape

Use FastAPI defaults:

- `HTTPException` → `{"detail": "..."}` with appropriate status codes.
- Request validation errors → `{"detail": [...]}`.
- Frontend client parses `detail` and shows a toast.

### Runner Update

`app/runner.py` continues to update the in-memory store. When PostgreSQL is introduced later, the store will be replaced by a SQLAlchemy-backed repository.

## Data Flow

### Starting a Job

1. User uploads/pastes instance JSON on New Job page.
2. Frontend `POST /solve?seed=42&auto_validate=true` with instance as body.
3. Backend creates a job in the in-memory store with `status=pending`.
4. Background task calls `main_mvp.solve(instance, seed)`.
5. On completion, backend updates the job with `result`, `objective_value`, and `status=completed`.
6. If `auto_validate=true`, backend calls `validator.py` and updates `validation_status` and `validation_report`.
7. Frontend polls `GET /jobs/{job_id}` every 1 second until status is terminal.

### Validation

1. User uploads instance and solution on Validate page.
2. Frontend `POST /validate`.
3. Backend runs the existing `validator.py`.
4. Backend returns `{passed, objective_value, violations, report}`.

## Component Structure

```
frontend/
├── src/
│   ├── api/
│   │   ├── client.ts          # Axios instance with base URL
│   │   ├── jobs.ts            # Job API calls
│   │   └── validate.ts        # Validator API calls
│   ├── components/
│   │   ├── Layout.tsx         # Top navigation
│   │   ├── JobStatusBadge.tsx
│   │   ├── RouteMap.tsx       # Leaflet map component
│   │   ├── VehicleRoutesTable.tsx
│   │   ├── LoaderRoutesTable.tsx
│   │   ├── ValidationReport.tsx
│   │   └── JsonEditor.tsx
│   ├── hooks/
│   │   ├── useJobs.ts
│   │   ├── useJob.ts
│   │   └── usePolling.ts
│   ├── pages/
│   │   ├── DashboardPage.tsx
│   │   ├── NewJobPage.tsx
│   │   ├── JobDetailPage.tsx
│   │   └── ValidatePage.tsx
│   ├── types/
│   │   └── index.ts
│   ├── App.tsx
│   └── main.tsx
├── index.html
├── package.json
├── tsconfig.json
├── tailwind.config.js
├── Dockerfile
└── nginx.conf          # Serve built SPA and proxy /api in production
```

## Docker Compose (Immediate)

```yaml
services:
  api:
    build: .
    environment:
      CORS_ORIGINS: http://localhost:5173,http://localhost:3000
    ports:
      - "8000:8000"
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

## Docker Compose (Planned)

When PostgreSQL is introduced:

```yaml
services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: routeopt
      POSTGRES_PASSWORD: routeopt
      POSTGRES_DB: routeopt
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U routeopt -d routeopt"]
      interval: 5s
      timeout: 5s
      retries: 5

  migrate:
    build: .
    command: ["alembic", "upgrade", "head"]
    environment:
      DATABASE_URL: postgresql+asyncpg://routeopt:routeopt@postgres/routeopt
    depends_on:
      postgres:
        condition: service_healthy

  api:
    build: .
    environment:
      DATABASE_URL: postgresql+asyncpg://routeopt:routeopt@postgres/routeopt
      CORS_ORIGINS: http://localhost:5173,http://localhost:3000
    ports:
      - "8000:8000"
    depends_on:
      migrate:
        condition: service_completed_successfully
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

volumes:
  postgres_data:
```

## Error Handling

- Invalid JSON on upload → inline validation error.
- Solver fails → Job Detail shows error message and raw input.
- Validation fails → Validation tab shows violation list.
- Network errors → toast notifications.
- Backend returns `{"detail": "..."}`; frontend parses `detail` consistently.

## Testing

- **Frontend unit tests:** Vitest for components and hooks.
- **Frontend E2E tests:** Playwright for full upload-solve-view flow.
- **Backend tests:** extend existing pytest suite with in-memory store tests for the new endpoints.
- **Future:** add SQLAlchemy-backed store tests and Docker Compose smoke test after PostgreSQL is introduced.

## Out of Scope for First Iteration

- Authentication and authorization.
- Real-time WebSocket updates (use polling).
- Advanced route comparison and benchmarking.
- User management or multi-tenancy.
- Persistent PostgreSQL storage (planned for a follow-up iteration).

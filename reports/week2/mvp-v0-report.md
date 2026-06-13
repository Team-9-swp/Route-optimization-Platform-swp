# MVP v0 Report

## Purpose

MVP v0 establishes a runnable technical foundation for the Route Optimization Platform. It exposes the existing CVRPTW solver as an asynchronous REST service that accepts a problem instance, runs the solver in the background, and returns the generated vehicle and loader routes. The service is packaged with Docker so it can be started with a single command.

## What MVP v0 includes

1. **FastAPI microservice** (`app/`) with the following endpoints:
   - `POST /solve?seed=42` — submit a JSON instance and receive a job ID.
   - `GET /jobs/{job_id}` — retrieve job status, result, or error.
2. **Asynchronous solver runner** that executes `main_mvp.solve` in a background thread.
3. **In-memory job store** for tracking pending, running, completed, and failed jobs.
4. **Docker packaging** (`Dockerfile`, `docker-compose.yml`) for reproducible local deployment.
5. **Test suite** covering endpoint behavior and an end-to-end solve flow on `test_cases/t1.json`.

## What MVP v0 does not include

- Persistent database (jobs are stored in memory and lost on restart).
- Web frontend (planned for MVP v1).
- Validation endpoint and auto-validation (planned for the next backend iteration).
- Pagination and job listing endpoint (planned for the frontend iteration).

## Repository and runnable artifact

- **Repository:** `https://github.com/Team-9-swp/Route-optimization-Platform-swp`
- **Docker Compose:** `docker-compose up --build` from the repository root.
- **Hosted instance:** `http://10.93.26.188:8000` (accessible from the university network; Swagger UI is available at `/docs`).

## Local setup instructions

1. Clone the repository.
2. Ensure Docker and Docker Compose are installed.
3. Run:

   ```bash
   docker compose up --build
   ```

4. Open Swagger UI at `http://localhost:8000/docs`.

## Repeatable smoke-check scenario

1. Start the services locally:

   ```bash
   docker-compose up --build
   ```

   Alternatively, use the hosted instance at `http://10.93.26.188:8000` (university network access required).

2. Submit a test instance:

   ```bash
   curl -X POST "http://localhost:8000/solve?seed=42" \
        -H "Content-Type: application/json" \
        -d @test_cases/t1.json
   ```

   Expected response (example):

   ```json
   {
     "job_id": "<uuid>",
     "status": "pending",
     "created_at": "2026-06-13T13:00:00Z"
   }
   ```

3. Poll the job until it is terminal:

   ```bash
   curl "http://localhost:8000/jobs/<job_id>"
   ```

   Expected final status: `completed`, with `result` containing `vehicles` and `loaders` arrays.

4. Verify the result JSON contains valid route structures matching the output format described in `Assignment_02.md`.

When running the smoke check against the hosted VM, replace `http://localhost:8000` with `http://10.93.26.188:8000`.

## Video demonstration

A public video demonstration of MVP v0 has been recorded (shorter than two minutes). The public link will be inserted here once it is available from the hosting platform:

```
[VIDEO_LINK_PLACEHOLDER]
```

## Relationship to MVP v1

MVP v0 provides the backend foundation for the following user stories:

- [US-01: Vehicle route and schedule](./user-stories.md#us-01-vehicle-route-and-schedule)
- [US-02: Loader route](./user-stories.md#us-02-loader-route)
- [US-03: Hard constraint validation](./user-stories.md#us-03-hard-constraint-validation) — foundation for the validator integration.
- [US-04: Docker execution](./user-stories.md#us-04-docker-execution)
- [US-10: Route visualization](./user-stories.md#us-10-route-visualization) — the data and API foundation that a future visualization layer can consume.

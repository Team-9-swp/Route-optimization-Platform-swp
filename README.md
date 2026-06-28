# Route Optimization Platform

A logistics optimization system for the BIA CVRPTW problem variant. The product provides a FastAPI backend, PostgreSQL-backed job history, a PyVRP/Nevergrad solver pipeline, validation, skipped optional order reporting, and a React web interface.

## Quick Start

Run the full stack with Docker Compose:

```bash
docker compose up --build
```

Then open:

- Swagger UI: `http://localhost:8000/docs`
- Web interface: `http://localhost:3000`

PostgreSQL is required for persistent job storage. The Compose stack starts a `db` service and the API uses:

```text
postgresql+asyncpg://optimizer:optimizer@db:5432/optimizer
```

## Database and Migrations

For local backend development, start PostgreSQL and apply migrations before running integration tests:

```bash
docker compose up -d db
alembic upgrade head
```

The default local database URL is:

```text
postgresql+asyncpg://optimizer:optimizer@localhost:5432/optimizer
```

Override it with `DATABASE_URL` when using another database.

## Backend Development

```bash
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

Submit a sample solver job:

```bash
curl -X POST "http://localhost:8000/solve?seed=42&time_limit=60&auto_validate=true" \
  -H "Content-Type: application/json" \
  -d @test_cases/t1.json
```

Important API changes in Assignment 4:

- `POST /solve` supports `seed`, `time_limit`, `name`, and `auto_validate`.
- `max_restarts` was removed.
- Completed job responses include `unserved_optional` when optional orders are skipped.
- Failed solver jobs return a user-safe error message instead of raw internal exceptions.

## Frontend Development

```bash
cd frontend
npm install
npm run dev
```

The Vite dev server proxies `/api` to `http://localhost:8000`.

CI runs both frontend type checking and the production build:

```bash
npm run typecheck
npm run build
```

## Testing

Run the default fast backend test suite:

```bash
pytest
```

Run backend unit and integration coverage the same way CI does:

```bash
pytest tests/ --ignore=tests/quality --ignore=tests/test_e2e.py -m "not slow" --cov=app --cov-report=term-missing --cov-report=xml
```

Run Assignment 4 Quality Requirement Tests:

```bash
pytest tests/quality/ -m "qrt" -q
pytest tests/quality/ -m "quality" -q
```

Integration and QRT commands require a PostgreSQL database configured through `DATABASE_URL`.

Run the additional QA security check:

```bash
bandit -r app/ -ll
```

## Solver Benchmarking

Benchmark the current solver on all `instances/i*.json` fixtures:

```bash
python scripts/benchmark.py --time-limit 60
```

The Assignment 4 benchmark report is in [reports/week4/solver-benchmark.md](./reports/week4/solver-benchmark.md).

## Deployment Status

The product is runnable with Docker Compose. The university VM deployment has been reported as reachable only from the Innopolis University network, so customer access from outside that network is not verified in the public repository.

An externally reachable tunnel such as ngrok may be used only as an agreed access method during a live session; the command itself is not deployment evidence:

```bash
ngrok http 3000
```

Issue [#90](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/90) remains the tracking item for deployment/customer access. GitHub Release [`v1.2.0`](https://github.com/Team-9-swp/Route-optimization-Platform-swp/releases/tag/v1.2.0) is published from protected `main`.

## Assignment Reports

- [Week 2 report index](./reports/week2/README.md)
- [MVP v1 / Week 3 report](./reports/week3/README.md)
- [Week 4 Assignment 4 public submission index](./reports/week4/README.md)
- [Quality requirements](./docs/quality-requirements.md)
- [Quality requirement tests](./docs/quality-requirement-tests.md)
- [Testing strategy and status](./docs/testing.md)
- [User acceptance tests](./docs/user-acceptance-tests.md)
- [Definition of Done](./docs/definition-of-done.md)
- [Roadmap](./docs/roadmap.md)

## License

[MIT](./LICENSE)

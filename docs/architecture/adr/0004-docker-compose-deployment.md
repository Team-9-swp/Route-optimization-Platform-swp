# ADR-0004: Deploy as a Docker Compose stack of db, api, and frontend

- **Status:** Accepted
- **Date:** 2026-07-04
- **Addresses:** Deployment model (supports QR-FC-01, QR-PE-01, QR-RE-01, QR-SE-01 by providing the verifiable runtime)

## Context

The customer and graders must be able to run and inspect the product with a single, reproducible command, and the team must be able to reproduce the same environment in CI. The product has three distinct runtime concerns:

- a stateful PostgreSQL database for persistent job history (QR-RE-01);
- a Python/FastAPI backend that runs the API and the solver;
- a React frontend that must be served to the browser.

Each has a different build and lifecycle, and the database must survive restarts.

## Decision

We deploy the product as a **Docker Compose** stack with three services defined in `docker-compose.yml`, overridable for production through `docker-compose.prod.yml`.

Concretely:

- **`db`** — `postgres:16-alpine` with a named volume `pgdata` and a `pg_isready` health check.
- **`api`** — built from `app/Dockerfile`, exposes `8000`, depends on a healthy `db`, and exposes a `/health` endpoint used by its own health check.
- **`frontend`** — built from `frontend/Dockerfile` (Vite production build served by nginx), exposes `3000:80`, and proxies API traffic to `api`.
- The production override adds `restart: unless-stopped`, a production `CORS_ORIGINS`, and `LOG_LEVEL=warning`.
- Configuration is supplied through environment variables (`DATABASE_URL`, `CORS_ORIGINS`, `LOG_LEVEL`, `VITE_API_BASE_URL`); real production secrets are injected by the deployment environment or GitHub Secrets, never committed.

## Consequences

- **Positive:** The whole product starts with `docker compose up --build`, which is reproducible for customers, graders, and CI.
- **Positive:** The database volume keeps job history across container restarts, supporting QR-RE-01.
- **Positive:** Health checks make deployment and CI failures observable.
- **Negative:** The Compose model targets a single host; horizontal scaling and managed databases are out of scope for this increment.
- **Negative:** Image build time and external library dependencies (PyVRP, Nevergrad) must be kept healthy in CI.

## Alternatives considered

- **Managed cloud database + PaaS backend:** rejected for this increment because the customer must be able to run the system directly and reproducibly.
- **Single combined image:** rejected because the frontend (static nginx assets), the Python backend, and the database have fundamentally different lifecycles and build chains.

## Follow-up work

Automatic deployment from protected `main` (issue #130) is implemented: after the `backend` and `frontend` CI jobs pass, a `deploy` job runs on a **self-hosted GitHub Actions runner that lives on the VM**, rebuilds the Compose stack, applies migrations, and runs a post-deploy health check. The VM has no public IP, so the runner connects to GitHub outbound over HTTPS. See [`docs/deployment.md`](../../deployment.md) for the runner setup, required configuration, manual redeploy, and rollback.

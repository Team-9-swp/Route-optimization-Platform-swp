# Roadmap

## Current Sprint: MVP v1 — API + frontend + Docker

**Goal:** Deliver a working end-to-end route-optimization platform that can be started with `docker compose up --build` and provides a web UI for submitting jobs, viewing results and validating solutions.

**Status:** In review (all PBIs implemented, stacked PRs open).

### Delivered in MVP v1
- Full REST API: `POST /solve`, `GET /jobs`, `GET /jobs/{id}`, `POST /validate`, `GET /health`
- CORS, job names, auto-validation, objective value tracking
- Configurable solver time limit and restart count
- React SPA wired to the API (Dashboard, New Job, Job Detail, Validate)
- Docker Compose setup with `api` and `frontend` services
- Full solution validator (`validator.py`)

## Next Sprint: MVP v2 — Persistence and visualization

**Goal:** Improve observability and robustness of the platform.

### Planned work
- Persistent job storage (replace in-memory store with SQLite/PostgreSQL)
- Advanced route visualization on a map
- Skipped optional orders report
- User authentication and basic audit logging
- Performance benchmarking page

## Future: MVP v3 — Enterprise readiness

**Goal:** Make the platform multi-tenant and production-grade.

### Planned work
- Auth with role-based access control
- Multi-tenancy and resource quotas
- Async worker queue (Redis + Celery/RQ)
- CI/CD pipeline for automated tests and deployments

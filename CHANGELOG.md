# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Automatic deployment from protected `main` in the CI pipeline: a `deploy` job runs on a self-hosted runner on the VM after the `backend` and `frontend` jobs pass, applies migrations, and verifies the API with a post-deploy health check. See `docs/deployment.md` for runner setup, manual redeploy, and rollback.

## [1.2.0] - 2026-06-29

### Added

- PostgreSQL-backed persistent job and result storage via SQLAlchemy async models and Alembic migrations.
- Async `JobRepository` for submitted jobs, completed results, validation metadata, and job history.
- Skipped optional orders report in solver output, API job responses, and frontend result views.
- PyVRP + Nevergrad solver pipeline integrated with the async job runner.
- Reproducible solver benchmark report under `reports/week4/solver-benchmark.md`.
- Assignment 4 automated Quality Requirement Tests under `tests/quality/` for functional correctness, time behaviour, recoverability, and confidentiality.
- `docs/testing.md`, `docs/definition-of-done.md`, and Week 4 public evidence documentation for Assignment 4 quality gates.
- Frontend TypeScript type-check command for CI: `npm run typecheck`.
- Coverage and JUnit XML artifact upload from the backend CI job.

### Changed

- FastAPI application version is prepared as `1.2.0`.
- Backend CI now treats Ruff linting and Black formatting as blocking checks.
- Backend CI runs unit and integration tests with coverage, required QRTs, and Bandit.
- Frontend CI runs type checking before the production build.
- Docker, database, migration, and testing instructions now describe the PostgreSQL-backed stack.
- `docs/quality-requirements.md` and `docs/quality-requirement-tests.md` use the Assignment 4 `900` second performance threshold.

### Removed

- Legacy in-memory job storage from the active product stack.
- `max_restarts` as a `POST /solve` API parameter.

### Fixed

- Solver runner stores a user-safe failure message instead of exposing raw exception details.
- QRTs no longer pass by silently skipping a required committed fixture.
- Recoverability QRT verifies completed-result persistence through repository/application recreation.
- Safe-error QRT injects traceback-like internal failures and checks public responses for leaks.

### Security

- Failed solver jobs must not expose stack traces, internal file paths, or injected fake secrets through public API responses.
- Bandit remains the selected additional QA check for medium/high severity security findings in `app/`.

## [1.1.0] - 2026-06-27

### Added

- Quality requirements document covering four measurable ISO/IEC 25010 sub-characteristics (`docs/quality-requirements.md`).
- Automated quality requirement test specifications for each quality requirement (`docs/quality-requirement-tests.md`).
- Assignment 4 sprint plan, goal, and selected outcomes in `docs/roadmap.md`.

### Changed

- Roadmap restructured with current sprint, previous increment, and future direction sections.

## [1.0.0] - 2026-06-19

### Added

- OR-Tools-based CVRPTW solver with greedy/Simulated Annealing loader optimization (`beta_code`).
- CORS middleware for frontend integration.
- `GET /jobs`, `POST /validate`, `GET /health` endpoints.
- Job name, objective value, and validation status tracking.
- React frontend connected to real API (Dashboard, New Job, Job Detail, Validate).
- Docker Compose setup with `api` and `frontend` services.
- Full solution validator (`backup/validator.py`).
- Week 3 assignment reports under `reports/week3/`.
- `docs/roadmap.md`.

### Changed

- `POST /solve` accepts optional `name`, `auto_validate`, `time_limit` and `max_restarts` parameters.
- Root `README.md` describes backend and frontend local development.
- Repository layout: legacy scripts moved to `backup/`, API `Dockerfile` moved to `app/Dockerfile`.

### Fixed

- JobDetail route map: custom SVG zoom/pan, per-route visibility filter, color legend and body-scroll lock on hover.

[Unreleased]: https://github.com/Team-9-swp/Route-optimization-Platform-swp/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/Team-9-swp/Route-optimization-Platform-swp/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/Team-9-swp/Route-optimization-Platform-swp/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/Team-9-swp/Route-optimization-Platform-swp/releases/tag/v1.0.0

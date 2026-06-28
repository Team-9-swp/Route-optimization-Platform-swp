# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Persistent PostgreSQL storage for jobs and results via SQLAlchemy 2.0 async models and Alembic migrations
- Async `JobRepository` replacing the previous in-memory store
- Integration tests covering job persistence across application restarts
- Skipped optional orders report returned in solver output and exposed in the frontend
- `skip_loader_refinement` solver option and `scripts/benchmark.py` for comparing the greedy loader stage against the full pipeline
- Assignment 4 Quality Requirement Tests under `tests/quality/`
- Week 4 benchmark and analysis reports under `reports/week4/`

### Changed
- `POST /solve` no longer accepts `max_restarts`
- `README.md` updated with database setup, test commands, and benchmarking instructions

### Removed
- In-memory `app/store.py` and the `max_restarts` API parameter

### Fixed
- Solver runner now stores a user-safe error message instead of the raw exception details

### Security
- Failed solver jobs no longer leak stack traces, file paths, or injected secrets through the API

### Deprecated

## [1.0.0] - 2026-06-19

### Added
- OR-Tools-based CVRPTW solver with greedy/Simulated Annealing loader optimization (`beta_code`)
- CORS middleware for frontend integration
- `GET /jobs`, `POST /validate`, `GET /health` endpoints
- Job name, objective value, and validation status tracking
- React frontend connected to real API (Dashboard, New Job, Job Detail, Validate)
- Docker Compose setup with `api` and `frontend` services
- Full solution validator (`backup/validator.py`)
- Week 3 assignment reports under `reports/week3/`
- `docs/roadmap.md`

### Changed
- `POST /solve` accepts optional `name`, `auto_validate`, `time_limit` and `max_restarts` parameters
- Root `README.md` now describes both backend and frontend local development
- Repository layout: legacy scripts moved to `backup/`, API `Dockerfile` moved to `app/Dockerfile`

### Fixed
- JobDetail route map: custom SVG zoom/pan, per-route visibility filter, color legend and body-scroll lock on hover

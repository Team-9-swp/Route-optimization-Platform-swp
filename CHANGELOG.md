# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

### Changed

### Deprecated

### Removed

### Fixed

### Security

## [1.1.0] - 2026-06-27

### Added
- Quality requirements document covering 4 measurable ISO/IEC 25010 sub-characteristics (`docs/quality-requirements.md`)
- Automated quality requirement test specifications for each quality requirement (`docs/quality-requirement-tests.md`)
- Assignment 4 sprint plan, goal, and selected outcomes in `docs/roadmap.md`

### Changed
- Roadmap restructured with current sprint, previous increment, and future direction sections

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

[Unreleased]: https://github.com/Team-9-swp/Route-optimization-Platform-swp/compare/v1.1.0...HEAD
[1.1.0]: https://github.com/Team-9-swp/Route-optimization-Platform-swp/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/Team-9-swp/Route-optimization-Platform-swp/releases/tag/v1.0.0

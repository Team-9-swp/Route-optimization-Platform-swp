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

## [1.0.0] - 2026-06-19

### Added
- CORS middleware for frontend integration
- `GET /jobs`, `POST /validate`, `GET /health` endpoints
- Job name, objective value, and validation status tracking
- React frontend connected to real API (Dashboard, New Job, Job Detail, Validate)
- Docker Compose setup with `api` and `frontend` services
- Full solution validator (`validator.py`)
- Week 3 assignment reports under `reports/week3/`
- `docs/roadmap.md`

### Changed
- `POST /solve` accepts optional `name`, `auto_validate`, `time_limit` and `max_restarts` parameters
- Root `README.md` now describes both backend and frontend local development

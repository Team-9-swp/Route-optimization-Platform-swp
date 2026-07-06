# Route Optimization Platform — Documentation

Welcome to the Route Optimization Platform documentation.

---

## Quick Links

- [Repository](https://github.com/Team-9-swp/Route-optimization-Platform-swp)
- [Changelog](../CHANGELOG.md)
- [License](../LICENSE)

---

## Product Documentation

- [Interface Documentation](interface.md) — Web UI and REST API description
- [User Stories](user-stories.md) — Product backlog user stories
- [Roadmap](roadmap.md) — Product roadmap and future plans

---

## Quality & Testing

- [Quality Requirements](quality-requirements.md) — Measurable quality requirements
- [Quality Requirement Tests](quality-requirement-tests.md) — Test specifications
- [Testing Strategy](testing.md) — Testing approach and coverage
- [Definition of Done](definition-of-done.md) — Completion criteria

---

## Development Process

- [Development Process](development-process.md) — Workflow and configuration management

---

## User Acceptance Tests

- [User Acceptance Tests](user-acceptance-tests.md) — UAT scenarios and results

---

## Architecture Documentation

- [Architecture Overview](architecture/README.md)
- [Static View (Component Diagram)](architecture/static-view/)
- [Dynamic View (Sequence Diagram)](architecture/dynamic-view/)
- [Deployment View](architecture/deployment-view/)
- [Architecture Decision Records (ADRs)](architecture/adr/)

---

## Assignment Planning

- [Assignment 5 Sprint 5 Planning](assignment5-sprint5-planning.md)

---

## Interface Documentation

### Web User Interface

- **Framework:** React + TypeScript
- **Primary users:** Dispatchers and logistics managers
- **Figma Prototype:** [Interactive prototype](https://carry-race-78764713.figma.site/)

### REST API

- **Framework:** FastAPI
- **Base URL (local):** `http://localhost:8000`
- **Swagger UI:** `http://localhost:8000/docs`
- **OpenAPI spec:** `api/openapi.yaml`

---

## Current Status

| Component | Status |
|-----------|--------|
| REST API | Implemented (MVP v1) |
| Web UI | Figma prototype, React implementation in progress |
| Persistent Storage | Planned (PostgreSQL) |
| Solver | PyVRP + Nevergrad |

---

*This documentation is maintained as part of the Route Optimization Platform project.*

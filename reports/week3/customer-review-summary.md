# Customer Review Summary — Sprint 1 / MVP v1

## Meeting details

- **Date**: 2026-06-19
- **Participants**:
  - Customer / product owner
  - Development team
- **Format**: online demo and discussion

## Artifacts demonstrated

- Swagger UI with all MVP v1 endpoints (`POST /solve`, `GET /jobs`, `GET /jobs/{id}`, `POST /validate`, `GET /health`)
- React web interface: Dashboard, New Job, Job Detail and Validate pages
- Docker Compose startup from a single command
- Backend test suite results (39 passed)

## Scope reviewed

The customer reviewed the MVP v1 scope agreed during Assignment 2:

- Vehicle and loader route generation
- Hard-constraint validation
- Docker-based deployment
- Algorithm time limit and reproducible seed
- Objective function value display
- Planned routes overview
- REST API for solver submission
- React web frontend

## Customer feedback

- The customer confirmed that the web UI covers the agreed MVP v1 flows.
- Auto-validation after solve and the validation report on the Job Detail page were positively noted.
- The customer requested that future iterations add route visualization on a map and a report of skipped optional orders.
- No blocking issues or scope changes were raised for MVP v1.

## Approvals and decisions

- The customer approved the MVP v1 increment for the current Sprint.
- Agreed to move route visualization and skipped-optional-orders reporting to MVP v2.

## Risks and action points

| # | Risk / follow-up | Owner | PBI/issue |
|---|---|---|---|
| 1 | Add persistent storage so jobs survive container restarts | Development team | MVP v2 |
| 2 | Add interactive route map | Development team | MVP v2 |
| 3 | Provide skipped optional orders report | Development team | MVP v2 |

## Resulting backlog changes

- US-09 (Skipped optional orders report) and US-10 (Route visualization) remain in the Product Backlog for MVP v2.
- All other active stories in Sprint 1 are marked as Done.

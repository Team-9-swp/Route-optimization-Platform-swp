# Week 3 Report — Assignment 3

## Project

**Route Optimization Platform** — a logistics optimization system that generates vehicle and loader routes for the BIA CVRPTW problem variant.  
License: [MIT](../../LICENSE)

## Summary of scope since Assignment 2

All active user stories from Assignment 2 were migrated into GitHub Issues and refined into the Sprint 1 backlog. The agreed MVP v1 scope focuses on a working end-to-end platform: a FastAPI backend with full REST endpoints, a React frontend connected to the API, and a Docker Compose setup that starts both services.

- Current user-story index: [`docs/user-stories.md`](../../docs/user-stories.md)
- Historical Assignment 2 stories: [`reports/week2/user-stories.md`](../week2/user-stories.md)

## Customer feedback addressed in MVP v1

The main feedback from Assignment 2 was that the solver needed to be accessible through a web UI and that the API should expose validation and listing capabilities. MVP v1 addresses this with:

- REST endpoints for solving, listing, validating and health checks.
- A React SPA for submitting jobs, viewing the job list, inspecting job details and validating solutions.
- Docker Compose packaging so the whole system runs from a single command.

## Backlog and Sprint views

- **Product Backlog** (MVP v1 issues): https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues?q=is%3Aopen+label%3Amvp-v1
- **Sprint Backlog** (Sprint 1 milestone): https://github.com/Team-9-swp/Route-optimization-Platform-swp/milestone/2
- **Sprint milestone**: https://github.com/Team-9-swp/Route-optimization-Platform-swp/milestone/2
- **MVP v1 view**: https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues?q=is%3Aopen+label%3Amvp-v1

> Note: `Team-9-swp` uses GitHub Issues search and milestone views as the inspectable backlog boards. A dedicated GitHub Project board was not configured because issue/milestone queries provide the same visibility.

## Estimates

- **Total Product Backlog size**: 34 Story Points
- **Total Sprint 1 size**: 34 Story Points

## Selected MVP v1 scope

MVP v1 contains the following PBIs, all linked to Sprint 1 and labeled `mvp-v1`:

- Backend: CORS, expanded schemas, extended store, validation wrapper, runner improvements, service extensions, new API endpoints, e2e stabilization.
- Frontend: API client/types, Dashboard, New Job, Job Detail, Validate pages.
- DevOps: frontend Dockerfile/nginx config, root Dockerfile update, Docker Compose update.
- Docs: README, CHANGELOG, user-stories, roadmap, Week 3 reports.

## PBI tracking approach

- **Type**: user stories are prefixed `US-xxx`; supporting technical PBIs are prefixed `PBI-xx`.
- **Status**: Work Status follows the canonical values (`To Do`, `In Progress`, `Ready`, `Done`).
- **Priority**: MoSCoW (`Must Have`, `Should Have`, `Could Have`).
- **Sprint**: all MVP v1 PBIs are assigned to the `Sprint 1` milestone.
- **MVP version**: tracked with the `mvp-v1` label.
- **Decomposition**: every user story selected for MVP v1 was split into small, issue-linked technical PBIs.

## Roadmap

See [`docs/roadmap.md`](../../docs/roadmap.md). The current Sprint delivers MVP v1; the next Sprint will add persistent storage, route visualization and a skipped-optional-orders report.

## Verification evidence

- Backend tests: `.venv/Scripts/python -m pytest tests/` — 39 passed.
- Frontend type-check: `cd frontend && npx tsc --noEmit` — no errors.
- Frontend build: `cd frontend && npm run build` — succeeds.
- Reviewed issue-linked PRs are listed below.

## Current product status

All MVP v1 PBIs have been implemented and are awaiting review in stacked PRs. The backend test suite is green, the frontend builds successfully, and the Docker Compose configuration is ready.

## Next steps

1. Complete peer review and merge the stacked PRs.
2. Tag the merged main branch as `v1.0.0`.
3. Deploy the Docker Compose stack to the university VM.
4. Record and publish the public video demonstration.

## Contribution traceability

| Team member | GitHub username | Role | Issues / PBIs | PRs | Reviews |
|---|---|---|---|---|---|
| *(to be filled by team)* | *(to be filled)* | *(to be filled)* | *(to be filled)* | *(to be filled)* | *(to be filled)* |

## Release and changelog

- **SemVer release**: https://github.com/Team-9-swp/Route-optimization-Platform-swp/releases/tag/v1.0.0
- **CHANGELOG**: [CHANGELOG.md](../../CHANGELOG.md)

## Process and templates

- [Process Requirements](../../Process_Requirements.md)
- [Definition of Done](../../docs/definition-of-done.md)
- [Roadmap](../../docs/roadmap.md)
- [Issue templates](../../.github/ISSUE_TEMPLATE)
- [Extended PR template](../../.github/pull_request_template.md)

## Reviewed issue-linked PRs

- Backend PRs
  - #45 — validator merge
  - #46 — CORS middleware (#30)
  - #47 — expanded schemas (#31)
  - #48 — extended store (#32)
  - #49 — validation wrapper (#33)
  - #50 — runner auto-validate (#34)
  - #51 — extended SolverService (#35)
  - #52 — new API endpoints (#36)
  - #53 — e2e stabilization (#37)
- Frontend PRs
  - #54 — frontend API client (#38)
  - #55 — Dashboard (#39)
  - #56 — New Job (#40)
  - #57 — Job Detail (#41)
  - #58 — Validate page (#42)
- DevOps/docs PRs
  - #59 — frontend Dockerfile/nginx (#43)
  - #60 — release v1.0.0 / Docker Compose and docs (#44)

## Delivered MVP v1

- Deployment/run instructions: [README.md](../../README.md)
- Swagger UI (when running): `http://localhost:8000/docs`
- Web UI (when running): `http://localhost:3000`

## Video demonstration

- *(link to be added after recording)*

## Screenshots

See [`reports/week3/images/`](./images/). The following screenshots should be added before final submission:

- Product Backlog view
- Sprint Backlog view
- Sprint milestone
- MVP v1 labeled view
- SemVer release
- Delivered MVP v1 (Swagger + web UI)
- Example reviewed issue-linked PR

## Customer review

- [Customer review summary](./customer-review-summary.md)
- [Customer review transcript](./customer-review-transcript.md) *(if publication permitted)*

## Reflection and retrospective

- [Reflection](./reflection.md)
- [Retrospective](./retrospective.md)
- [LLM report](./llm-report.md)

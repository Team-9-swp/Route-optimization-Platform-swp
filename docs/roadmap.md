# Roadmap

## Current Sprint — Sprint 5 / MVP v2

**Sprint dates:** 2026-06-29 — 2026-07-05

**Sprint Goal:** Deliver MVP v2 with improved solution usability and maintainability by fixing validator-compatible JSON export, improving loader workload distribution, adding Gantt schedule visualization, investigating stronger optimization approaches, documenting the architecture and development process, and automating deployment from the protected main branch.

### Planned MVP v2 product work

- Validator-compatible solution JSON export.
- Improved loader workload balance.
- Gantt schedule visualization.
- Known bug fix, with reproduction details required before implementation starts.
- Solver pipeline and greedy-stage analysis, using closed issues [#23](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/23) and [#97](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/97) only as historical context.
- Column-generation research spike for the current route-optimization variant.
- Automatic deployment from protected `main`.

### Architecture and process work

- Maintained development-process and configuration-management documentation.
- Static, dynamic, and deployment architecture views.
- At least three linked Architecture Decision Records.
- Extended tests, quality evidence, and Definition of Done for MVP v2.
- Hosted documentation site.

### Sprint delivery evidence

- Customer-accessible MVP v2.
- New and updated UAT scenarios.
- Recorded Sprint Review and customer UAT.
- Public sanitized demo video.
- Week 5 public report.
- SemVer release mapped to MVP v2.

### Planning and traceability notes

- The selected Sprint 5 PBIs are planned for the `Sprint 5 — MVP v2` milestone. GitHub Project field and view setup requires project-scope access.
- Every selected PBI must include a clear expected outcome, testable acceptance criteria, Story Points, implementer, different reviewer, priority, MVP version `MVP v2`, and Work Status `To Do`.
- Completion is measured by accepted, tested, reviewed, and Done Sprint outcomes, not by the number of created issues.

## Previous Sprint: Assignment 4 - Quality, Reliability, and Customer Feedback

**Sprint dates:** 22 June 2026 - 3 July 2026

**Sprint Goal:** Deliver a more reliable and verifiable Route Optimization Platform by addressing selected customer feedback, preserving submitted jobs across restarts, improving solver robustness, and enforcing automated quality gates through tests and CI.

### Selected Sprint Outcomes

| Outcome | Current public status |
|---|---|
| Add a skipped optional orders report for completed solutions. | Implemented through solver/API/frontend result data and linked to [#13](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/13). |
| Persist jobs and results so they survive application restarts. | Implemented with PostgreSQL-backed `app/repository.py` and linked to [#85](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/85). |
| Fix solver parameter handling and prevent internal tracebacks from being exposed through the API. | Implemented; `max_restarts` is removed and safe error QRTs inject internal failures. |
| Define measurable quality requirements using distinct ISO/IEC 25010 sub-characteristics. | Implemented in `docs/quality-requirements.md`. |
| Automate at least one quality requirement test for each quality requirement. | Implemented under `tests/quality/`; protected-main CI passed all required QRTs. |
| Add unit tests, integration tests, critical-module coverage reporting, and an additional automated QA check. | Implemented in workflow and tests; protected-main CI reports 94% total `app/` coverage and Bandit passed. |
| Configure CI quality gates and protected-default-branch rules. | CI workflow updated; branch-protection evidence still requires organization-admin verification. |
| Update deployment access and create a SemVer release for the Sprint increment. | GitHub Release `v1.2.0` is published from protected `main`; deployment/customer access verification remains open. |
| Conduct customer UAT and preserve sanitized evidence. | The 27 June recorded customer session included UAT-01, UAT-02, and UAT-03; private recording URL, timecodes, and permission evidence are Moodle-only. |
| Conduct Sprint Review and preserve evidence. | The 27 June recorded customer session included Sprint Review discussion and customer UAT execution; public notes are sanitized. |
| Prepare the Week 4 report, public demo video, and project presentation. | Public report index, screenshots, demo video link, and `presentation.pdf` are included. |

### Scope Rationale

The Sprint prioritizes customer value, product reliability, and risk reduction. Persistent storage and skipped-order reporting respond directly to customer needs. Automated tests, QRTs, coverage, CI, and branch-protection requirements reduce regression risk and become maintained project assets for later Sprints.

### Deferred Work

- Broad solver refactoring for guaranteed feasibility and performance on very large instances remains in [#23](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/23).
- Deeper baseline comparison, greedy-stage impact analysis, and repeated-run reproducibility remain follow-up solver-quality work.
- Authentication, multi-tenancy, resource quotas, and asynchronous worker queues are outside Assignment 4 scope.
- Automatic job retention and cleanup policies are deferred.
- Deployment observability and backup procedures remain future production-readiness work.

## Previous Increment: MVP v1 - API, Frontend, and Docker

MVP v1 was released as `v1.0.0`. It delivered the REST API, React SPA, route visualization, solution validation, configurable solver controls, and Docker Compose packaging for the API and frontend.

The `v1.1.0` release contains Assignment 4 planning and quality-documentation work. GitHub Release `v1.2.0` contains the final Assignment 4 increment and was published from protected `main`.

## Expected next increment

Work likely to continue after Sprint 5 includes solver redesign if the greedy-stage analysis shows that fixed early decisions materially reduce quality, deferred column-generation implementation if the research spike is accepted, performance improvements on larger scenarios, deployment hardening beyond the first automatic protected-`main` workflow, and customer feedback that is not completed in MVP v2.

### Expected Work

- Continue any MVP v2 customer feedback not completed during Sprint 5.
- Refine solver performance targets using reproducible benchmark datasets and fixed random seeds.
- Decide whether to redesign the solver pipeline around more joint optimization.
- Turn the column-generation spike into an implementation PBI only if the ADR decision accepts or proposes that direction.
- Improve solution quality, execution time, and loader balance without bypassing maintained quality gates.
- Harden deployment observability, logging, rollback, backup, and recovery procedures.

## Future Direction: Production Readiness

- Authentication and role-based access control.
- Multi-tenancy and resource quotas.
- Asynchronous worker queue.
- Database backup, restore, and migration procedures.
- Deployment monitoring and operational alerts.
- Stronger security and performance testing.

## Maintained Quality and Automation Assets

The following assets remain mandatory for later project work:

- `docs/quality-requirements.md`
- `docs/quality-requirement-tests.md`
- `docs/testing.md`
- `docs/definition-of-done.md`
- automated unit and integration tests
- automated quality requirement tests
- critical-module coverage checks
- CI quality gates
- protected-default-branch required checks once organization-admin verification is complete

Later PBIs must maintain or strengthen these assets instead of disabling or bypassing them.

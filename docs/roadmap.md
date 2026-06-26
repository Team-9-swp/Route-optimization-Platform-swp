# Roadmap

## Current Sprint: Assignment 4 — Quality, Reliability, and Customer Feedback

**Sprint dates:** 22 June 2026 – 3 July 2026

**Sprint Goal:** Deliver a more reliable and verifiable Route Optimization Platform by addressing selected customer feedback, preserving submitted jobs across restarts, improving solver robustness, and enforcing automated quality gates through tests and CI.

### Selected Sprint outcomes

- Add a skipped optional orders report for completed solutions.
- Persist jobs and results so they survive application restarts.
- Fix solver parameter handling and prevent internal tracebacks from being exposed through the API.
- Define measurable quality requirements using distinct ISO/IEC 25010 sub-characteristics.
- Automate at least one quality requirement test for each quality requirement.
- Add unit tests, integration tests, critical-module coverage reporting, and an additional automated QA check.
- Configure CI quality gates and protected-default-branch rules.
- Update the university VM deployment and create a SemVer release for the Sprint increment.
- Conduct customer UAT and a Sprint Review, then preserve sanitized evidence.
- Prepare the Week 4 report, public demo video, and project presentation.

### Scope rationale

The Sprint prioritizes customer value, product reliability, and risk reduction rather than the number of closed issues. Persistent storage and skipped-order reporting respond to customer needs. Automated tests, quality requirement tests, coverage, CI, and branch protection reduce regression risk and become maintained project assets for later Sprints.

### Deferred work

- The broad solver-refactoring PBI for guaranteed feasibility and performance on instances with up to 1,000 delivery points remains in the Product Backlog. It requires benchmarking and scope refinement before implementation.
- Authentication, multi-tenancy, resource quotas, and an asynchronous worker queue are not selected for this Sprint.
- Further map improvements are deferred unless customer UAT identifies a blocking usability problem.

## Previous Increment: MVP v1 — API, Frontend, and Docker

MVP v1 was completed and released as `v1.0.0`. It delivered the REST API, React SPA, route visualization, solution validation, configurable solver controls, and Docker Compose packaging for the API and frontend.

## Next Sprint: Product Hardening and Scalability

**Goal:** Improve solver scalability and operational readiness using the measurement and automation baseline established in Assignment 4.

### Expected work

- Refine solver performance targets using reproducible benchmark datasets.
- Improve solution quality and execution time without bypassing Assignment 4 quality gates.
- Add job retention and cleanup policies for persistent storage.
- Address issues created from Assignment 4 UAT and Sprint Review.
- Extend frontend automated testing where coverage remains weak.
- Improve deployment observability, logging, and recovery procedures.

## Future Direction: Production Readiness

### Planned work

- Authentication and role-based access control.
- Multi-tenancy and resource quotas.
- Asynchronous worker queue.
- Database migration and backup procedures.
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
- protected-default-branch rules

Later PBIs must maintain or strengthen these assets instead of disabling or bypassing them.

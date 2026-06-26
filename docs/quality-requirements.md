# Quality Requirements

## Purpose

This document defines measurable quality requirements for the Route Optimization Platform.  
Each requirement has a stable identifier, a measurable threshold, a rationale, and traceability to backlog items and automated quality requirement tests.

## Scope

The requirements apply to:

- the route optimization solver;
- the backend API;
- persistent job storage;
- error handling;
- the deployed Assignment 4 increment.

## Quality Requirements Summary

| ID | ISO/IEC 25010 characteristic | Sub-characteristic | Requirement |
|---|---|---|---|
| QR-FC-01 | Functional suitability | Functional correctness | Solver output must satisfy all hard constraints for valid supported input instances. |
| QR-PE-01 | Performance efficiency | Time behaviour | A fixed CI benchmark must complete within 30 seconds, and the configured solver time limit must be respected. |
| QR-RE-01 | Reliability | Recoverability | Submitted jobs and completed results must remain available after an application restart. |
| QR-SE-01 | Security | Confidentiality | API responses must not expose stack traces, internal file paths, or implementation details. |

---

## QR-FC-01 — Solver Functional Correctness

**ISO/IEC 25010 sub-characteristic:** Functional correctness

### Requirement

For every valid supported test instance used in automated verification, the solver must return a solution that passes the project validator with **zero hard-constraint violations**.

### Measurement

The solution is checked by the existing validation logic.

The requirement passes when:

- the solver returns a completed solution;
- the validator reports the solution as valid;
- the number of hard-constraint violations is `0`;
- all mandatory orders are assigned exactly as required;
- vehicle and loader routes satisfy capacity, timing, and assignment constraints.

### Test data

At minimum:

- one small deterministic reference instance;
- one instance containing optional orders;
- one instance requiring loader assignments.

The exact fixtures are listed in `docs/quality-requirement-tests.md`.

### Rationale

A low objective value is not useful if the generated route violates mandatory constraints. Correctness is therefore the primary quality requirement for the optimization result.

### Traceability

- Product area: solver and validator
- Related issues:
  - [#23 — Refactor route optimization algorithm](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/23)
  - [#13 — Skipped optional orders report](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/13)
- Planned automated evidence: `QRT-FC-01`

---

## QR-PE-01 — Solver Time Behaviour

**ISO/IEC 25010 sub-characteristic:** Time behaviour

### Requirement

A fixed small reference instance must be solved and validated within **30 seconds** in GitHub Actions under the standard CI configuration.

The solver must also respect the configured execution limit:

- the solver runtime must not exceed `configured time limit + 10 seconds`;
- timeout handling must return a controlled job status instead of leaving the job permanently in progress.

### Measurement

Measure elapsed wall-clock time from the start of the solver call until:

- a completed solution is returned; or
- a controlled failure/timeout state is recorded.

The CI requirement passes when:

- the fixed benchmark completes within 30 seconds;
- the job reaches a terminal state;
- the configured limit is not exceeded by more than 10 seconds.

### Test environment

- GitHub Actions Linux runner;
- fixed input fixture;
- fixed random seed;
- no external network dependency;
- standard project dependencies.

### Rationale

The customer needs to run and validate the system directly. Predictable execution time is required for practical use and for reliable automated verification.

### Traceability

- Product area: solver runner and API job lifecycle
- Related issues:
  - [#23 — Refactor route optimization algorithm](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/23)
  - [#86 — Improve solver parameter and error handling](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/86)
- Planned automated evidence: `QRT-PE-01`

### Limitation

The 30-second CI threshold applies to the fixed Assignment 4 reference fixture, not to every possible instance with up to 1,000 delivery points. Large-instance benchmarking remains separate Product Backlog work under issue #23.

---

## QR-RE-01 — Job Recoverability

**ISO/IEC 25010 sub-characteristic:** Recoverability

### Requirement

Submitted jobs and completed results must remain retrievable after the backend application and storage component are recreated using the same persistent database.

### Measurement

The requirement passes when an automated test:

1. creates a job;
2. stores a completed result;
3. closes the current application/store instance;
4. creates a new application/store instance using the same database;
5. retrieves the job by its original identifier;
6. confirms that the job status and result are unchanged.

No completed job may disappear only because the application process or container restarted.

### Rationale

The customer requested calculation history. In-memory storage loses all jobs after a restart and therefore cannot provide reliable history.

### Traceability

- Product area: job storage and job API
- Related issue:
  - [#85 — Persist jobs and results across restarts](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/85)
- Planned automated evidence: `QRT-RE-01`

### Limitation

Automatic deletion, retention periods, backups, and multi-user storage are outside the Assignment 4 scope.

---

## QR-SE-01 — Safe Error Confidentiality

**ISO/IEC 25010 sub-characteristic:** Confidentiality

### Requirement

Public API responses and stored job error fields must not expose:

- Python stack traces;
- absolute internal file paths;
- source-code locations;
- environment variables;
- credentials or secrets;
- raw unhandled exception details.

A failed job must expose only a controlled, user-safe error message and error category. Detailed diagnostic information may be written to server-side logs.

### Measurement

The requirement passes when automated tests trigger a controlled solver failure and confirm that the serialized API response does not contain patterns such as:

- `Traceback (most recent call last)`;
- `/app/`;
- `.py", line`;
- environment-variable or credential values.

### Rationale

Internal diagnostics can reveal implementation details and sensitive deployment information. Users need a useful failure message without receiving server internals.

### Traceability

- Product area: solver runner, service layer, API serialization
- Related issue:
  - [#86 — Improve solver parameter and error handling](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/86)
- Planned automated evidence: `QRT-SE-01`

---

## Acceptance of This Document

This document is complete for Assignment 4 when:

- at least three requirements use different ISO/IEC 25010 sub-characteristics;
- every requirement has a measurable threshold;
- every requirement has a rationale;
- every requirement is linked to a backlog item or documented product area;
- every requirement has at least one automated QRT defined in `docs/quality-requirement-tests.md`;
- the document is reviewed through an issue-linked pull request.

## Change Control

Any change to a threshold must be:

- justified in the related issue or pull request;
- reviewed by another team member;
- reflected in the corresponding QRT;
- recorded in the Week 4 report if it affects submitted evidence.

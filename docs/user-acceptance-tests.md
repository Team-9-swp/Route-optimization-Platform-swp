# User Acceptance Tests

## Purpose

This document defines end-user-facing acceptance test scenarios for the Route Optimization Platform and records sanitized public execution results. Private recording links, exact timecodes, customer identity, credentials, and private access details are intentionally excluded from the repository.

## Timeline

| Date | Event | Public status |
|---|---|---|
| 27 June 2026 | Combined recorded Sprint Review and customer UAT session | The session included Sprint Review discussion and execution of UAT-01, UAT-02, and UAT-03. Private recording URL, exact timecodes, and recording permission evidence are supplied through Moodle only. |

## Active Scenarios

| ID | Title | Public result | Priority | Traceability |
|---|---|---|---|---|
| UAT-01 | Submit a delivery instance and receive an optimized solution | Passed in the 27 June combined Sprint Review/UAT session | High | US-01a, US-01b, US-02, US-07, US-08; QR-FC-01 |
| UAT-02 | Validate a custom solution through the validator | Passed in the 27 June combined Sprint Review/UAT session | High | US-03; QR-FC-01; QR-SE-01 |
| UAT-03 | Retrieve previously submitted solutions from history | Passed in the 27 June combined Sprint Review/UAT session | High | US-08; QR-RE-01 |

## UAT-01: Submit a Delivery Instance and Receive an Optimized Solution

**Stable ID:** UAT-01

**Title:** Submit a delivery instance and receive an optimized solution

**Traceability:**

- [US-01a - Vehicle route output](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/18)
- [US-01b - Vehicle arrival schedule](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/19)
- [US-02 - Loader route](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/6)
- [US-07 - Objective function value](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/11)
- [US-08 - Planned routes overview](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/12)
- [QR-FC-01 - Solver functional correctness](quality-requirements.md#qr-fc-01--solver-functional-correctness)

### Preconditions

1. The product is available through an agreed customer access method or local Docker run.
2. The customer has a valid CVRPTW problem instance JSON such as `test_cases/t1.json`.

### Steps

1. Open the web interface.
2. Open the New Job page.
3. Upload or paste the problem instance JSON.
4. Optionally set job name, seed, and time limit.
5. Submit the job.
6. Wait for the job to reach a terminal state.
7. Open the completed job details.

### Expected Result

1. The job reaches `completed`.
2. The solution is automatically validated when requested.
3. The Job Detail view displays objective value, vehicle routes, loader routes, route timing, and skipped optional orders where applicable.
4. The validation report has zero hard-constraint violations.

### Execution Record

| Field | Value |
|---|---|
| Execution date | 27 June 2026 |
| Customer role | Customer representative |
| Public result | Passed according to sanitized combined Sprint Review/UAT notes |
| Sanitized public evidence | A recorded 27 June customer session included Sprint Review discussion and UAT execution; repository contains only this sanitized summary. |
| Private evidence required | Recording URL, exact UAT/Sprint Review timecodes, and recording permission evidence for Moodle/private submission. |

## UAT-02: Validate a Custom Solution Through the Validator

**Stable ID:** UAT-02

**Title:** Validate a custom solution through the validator

**Traceability:**

- [US-03 - Hard constraint validation](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/7)
- [QR-FC-01 - Solver functional correctness](quality-requirements.md#qr-fc-01--solver-functional-correctness)
- [QR-SE-01 - Safe error confidentiality](quality-requirements.md#qr-se-01--safe-error-confidentiality)

### Preconditions

1. The product is available through an agreed customer access method or local Docker run.
2. The customer has a problem instance JSON and a candidate solution JSON.

### Steps

1. Open the web interface.
2. Open the Validate page.
3. Paste or upload the problem instance JSON.
4. Paste or upload the candidate solution JSON.
5. Run validation.

### Expected Result

1. The validator returns a clear pass/fail result.
2. Valid solutions show a successful validation status and zero hard-constraint violations.
3. Invalid solutions show specific violation details.
4. Public responses do not expose stack traces, internal file paths, or private implementation details.

### Execution Record

| Field | Value |
|---|---|
| Execution date | 27 June 2026 |
| Customer role | Customer representative |
| Public result | Passed according to sanitized combined Sprint Review/UAT notes |
| Sanitized public evidence | A recorded 27 June customer session included Sprint Review discussion and UAT execution; repository contains only this sanitized summary. |
| Private evidence required | Recording URL, exact UAT/Sprint Review timecodes, and recording permission evidence for Moodle/private submission. |

## UAT-03: Retrieve Previously Submitted Solutions from History

**Stable ID:** UAT-03

**Title:** Retrieve previously submitted solutions from history

**Traceability:**

- [US-08 - Planned routes overview](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/12)
- [QR-RE-01 - Job recoverability](quality-requirements.md#qr-re-01--job-recoverability)
- [#85 - Persist jobs and results across restarts](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/85)

### Preconditions

1. The product is available through an agreed customer access method or local Docker run.
2. At least one job has previously been submitted and completed.
3. PostgreSQL persistence is enabled.

### Steps

1. Open the web interface.
2. Open the Dashboard page.
3. Review the list of previously submitted jobs.
4. Open a completed historical job.
5. Where possible, verify the history remains after application restart.

### Expected Result

1. The Dashboard lists previously submitted jobs with status, name, and creation time.
2. Opening a completed historical job displays the stored solution, validation status, objective value, route visualization, and route tables.
3. Completed job data remains available when the application is recreated with the same PostgreSQL database.

### Execution Record

| Field | Value |
|---|---|
| Execution date | 27 June 2026 |
| Customer role | Customer representative |
| Public result | Passed according to sanitized combined Sprint Review/UAT notes |
| Sanitized public evidence | A recorded 27 June customer session included Sprint Review discussion and UAT execution; repository contains only this sanitized summary. |
| Private evidence required | Recording URL, exact UAT/Sprint Review timecodes, and recording permission evidence for Moodle/private submission. |

## Resulting Backlog Items

| Feedback or observation | Resulting issue | Public status |
|---|---|---|
| Customer access must be reliable outside the university network or explicitly agreed through another method. | [#90](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/90) | Still open until deployment/access criteria are verified. |
| Combined Sprint Review/UAT evidence must remain available privately without exposing customer identity or links publicly. | [#91](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/91), [#92](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/92) | Private recording details are supplied through Moodle only and are intentionally excluded from the repository. |

## Private Moodle Checklist

Do not commit the following to the public repository:

- recording URL;
- exact UAT timecodes;
- recording permission evidence;
- customer identity;
- credentials or private access instructions.

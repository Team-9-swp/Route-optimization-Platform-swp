# User Acceptance Tests

## Purpose

This document defines end-user-facing acceptance test scenarios for the Route Optimization Platform. Each scenario has a stable identifier, traceability to requirements, and an execution history recorded during customer UAT sessions.

## Active Scenarios

| ID | Title | Status | Priority | Traceability |
|---|---|---|---|---|---|
| UAT-01 | Submit a delivery instance and receive an optimised solution | Passed | High | US-01a, US-01b, US-02, US-07, US-08; QR-FC-01 |
| UAT-02 | Validate a custom solution through the validator | Passed | High | US-03; QR-FC-01 |
| UAT-03 | Retrieve previously submitted solutions from history | Passed | High | US-08; QR-RE-01 |

---

## UAT-01: Submit a delivery instance and receive an optimised solution

**Title:** Submit a delivery instance and receive an optimised solution

**Status:** Passed

**Priority:** High

**Traceability:**
- User stories: [US-01a — Vehicle route output](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/18), [US-01b — Vehicle arrival schedule](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/19), [US-02 — Loader route](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/6), [US-07 — Objective function value](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/11), [US-08 — Planned routes overview](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/12)
- Quality requirements: [QR-FC-01 — Solver functional correctness](quality-requirements.md#qr-fc-01--solver-functional-correctness)

### Preconditions

1. The application is running (Docker Compose or local dev).
2. The user has a valid CVRPTW problem instance JSON file (e.g. `test_cases/t1.json`).

### Test steps

1. Open the web interface at `http://localhost:3000`.
2. Navigate to the **New Job** page.
3. Upload or paste the problem instance JSON.
4. Optionally set a job name, seed, and time limit.
5. Submit the job.
6. Wait for the solver to complete (the dashboard polls automatically).
7. Open the completed job from the **Dashboard**.

### Expected results

1. The job completes with status `completed`.
2. The solution is automatically validated — validation status shows `valid`.
3. The **Job Detail** page displays:
   - objective function value;
   - a route map with vehicle and loader routes;
   - a route table for each vehicle (stops, arrival times, load);
   - a route table for each loader (assigned vehicles, schedule).
4. All displayed routes satisfy hard constraints (capacity, time windows, shift length).

### Execution history

| Date | Tester | Result | Evidence |
|---|---|---|---|
| 2026-06-27 | Customer | Passed — all expected results confirmed. Solution completed, auto-validated as valid, route map and tables displayed correctly. | Private UAT recording (submitted via Moodle) |

---

## UAT-02: Validate a custom solution through the validator

**Title:** Validate a custom solution through the validator

**Status:** Passed

**Priority:** High

**Traceability:**
- User stories: [US-03 — Hard constraint validation](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/7)
- Quality requirements: [QR-FC-01 — Solver functional correctness](quality-requirements.md#qr-fc-01--solver-functional-correctness)

### Preconditions

1. The application is running.
2. The user has a problem instance JSON and a candidate solution JSON.

### Test steps

1. Open the web interface.
2. Navigate to the **Validate** page.
3. Paste or upload the problem instance JSON in the left panel.
4. Paste or upload the candidate solution JSON in the right panel.
5. Click **Validate**.

### Expected results

1. The validator returns a clear pass/fail result.
2. If the solution is valid: a green `valid` status with zero hard-constraint violations is displayed.
3. If the solution is invalid: a red `invalid` status with specific violation details is displayed (which orders, vehicles, or constraints are violated).
4. The response does not expose stack traces or internal file paths.

### Execution history

| Date | Tester | Result | Evidence |
|---|---|---|---|
| 2026-06-27 | Customer | Passed — both valid and invalid solutions correctly identified. Valid solution displayed green status; invalid solution showed specific violation details. No internal details exposed. | Private UAT recording (submitted via Moodle) |

---

## UAT-03: Retrieve previously submitted solutions from history

**Title:** Retrieve previously submitted solutions from history

**Status:** Passed

**Priority:** High

**Traceability:**
- User stories: [US-08 — Planned routes overview](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/12)
- Quality requirements: [QR-RE-01 — Job recoverability](quality-requirements.md#qr-re-01--job-recoverability)

### Preconditions

1. The application is running.
2. At least one job has been previously submitted and completed.

### Test steps

1. Open the web interface.
2. Navigate to the **Dashboard** page.
3. Observe the list of previously submitted jobs.
4. Click on a historical job to view its details.

### Expected results

1. The Dashboard shows all previously submitted jobs with their status, name, and submission time.
2. Clicking a completed job opens the full **Job Detail** view with:
   - the original solution data;
   - validation status;
   - route map and route tables.
3. After an application restart, previously completed jobs remain accessible and their data is unchanged.

### Execution history

| Date | Tester | Result | Evidence |
|---|---|---|---|
| 2026-06-27 | Customer | Passed — dashboard displayed all previous jobs. Completed job details (solution, validation, map) fully accessible. | Private UAT recording (submitted via Moodle) |

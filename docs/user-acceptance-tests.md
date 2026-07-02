# User Acceptance Tests

## Purpose

This document defines end-user-facing acceptance test scenarios for the Route Optimization Platform. Each scenario has a stable identifier, traceability to requirements, and an execution history recorded during customer UAT sessions.

## Table of Contents

- [Active Scenarios](#active-scenarios)
- [UAT-01: Submit a delivery instance and receive an optimised solution](#uat-01-submit-a-delivery-instance-and-receive-an-optimised-solution)
- [UAT-02: Validate a custom solution through the validator](#uat-02-validate-a-custom-solution-through-the-validator)
- [UAT-03: Retrieve previously submitted solutions from history](#uat-03-retrieve-previously-submitted-solutions-from-history)
- [UAT-04: View route visualization for each vehicle and loader](#uat-04-view-route-visualization-for-each-vehicle-and-loader)
- [UAT-05: Review the skipped optional orders report](#uat-05-review-the-skipped-optional-orders-report)
- [Sprint 3 UAT Summary](#sprint-3-uat-summary)

## Active Scenarios

| ID | Title | Status | Priority | Traceability |
|---|---|---|---|---|
| UAT-01 | Submit a delivery instance and receive an optimised solution | Passed | High | US-01a, US-01b, US-02, US-07, US-08; QR-FC-01 |
| UAT-02 | Validate a custom solution through the validator | Passed | High | US-03; QR-FC-01 |
| UAT-03 | Retrieve previously submitted solutions from history | Passed | High | US-08; QR-RE-01 |
| UAT-04 | View route visualization for each vehicle and loader | Passed | High | US-10; QR-FC-01 |
| UAT-05 | Review the skipped optional orders report | Passed | Medium | US-09 |

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
   - a route table for each loader (assigned vehicles, schedule);
   - skipped optional orders report if applicable.
4. All displayed routes satisfy hard constraints (capacity, time windows, shift length).

### Execution history

| Date | Tester | Result | Evidence |
|---|---|---|---|
| 2026-06-27 | Customer | Passed — all expected results confirmed. Solution completed, auto-validated as valid, route map and tables displayed correctly. | Private UAT recording (submitted via Moodle) |
| 2026-07-02 | Customer | Passed — all original results confirmed. Skipped optional orders report now correctly displayed alongside existing detail. | Private UAT recording (submitted via Moodle) |

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
| 2026-07-02 | Customer | Passed — validator continues to work correctly with no regressions. | Private UAT recording (submitted via Moodle) |

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
   - route map and route tables;
   - skipped optional orders report if applicable.
3. After an application restart, previously completed jobs remain accessible and their data is unchanged.

### Execution history

| Date | Tester | Result | Evidence |
|---|---|---|---|
| 2026-06-27 | Customer | Passed — dashboard displayed all previous jobs. Completed job details (solution, validation, map) fully accessible. | Private UAT recording (submitted via Moodle) |
| 2026-07-02 | Customer | Passed — all historical jobs accessible after restart. Persistence confirmed. Skipped orders data preserved. | Private UAT recording (submitted via Moodle) |

---

## UAT-04: View route visualization for each vehicle and loader

**Title:** View route visualization for each vehicle and loader

**Status:** Passed

**Priority:** High

**Traceability:**
- User story: [US-10 — Route visualization](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/14)
- Quality requirements: [QR-FC-01 — Solver functional correctness](quality-requirements.md#qr-fc-01--solver-functional-correctness)

### Preconditions

1. The application is running.
2. A completed job exists with vehicle and loader routes (e.g. from UAT-01).

### Test steps

1. Open the web interface at `http://localhost:3000`.
2. Navigate to the **Dashboard**.
3. Click on a completed job to open the **Job Detail** view.
4. Observe the **Route Map** area at the top of the page.
5. Interact with the route map:
   - Zoom in using the **+** button.
   - Zoom out using the **-** button.
   - Reset the view using the **Reset** button.
   - Scroll to zoom in/out on the map.
   - Drag to pan the map.
6. In the **Route Filter** panel (top-left corner):
   - Toggle the **Vehicles** section to show/hide all vehicle routes.
   - Toggle individual vehicle checkboxes to show/hide specific vehicle routes.
   - Toggle the **Loaders** section to show/hide all loader routes.
   - Toggle individual loader checkboxes to show/hide specific loader routes.
7. Scroll through the **Route List** panel (bottom-right corner) to verify order counts per visible route.
8. View the **Vehicle Routes** table below the map — verify route sequences and start times.
9. View the **Loader Routes** table below the map — verify route sequences.

### Expected results

1. The route map displays all vehicle routes as dashed polylines and loader routes as solid polylines.
2. Each vehicle route is drawn in a distinct color from the vehicle palette.
3. Each loader route is drawn in a distinct color from the loader palette.
4. The depot is shown as a blue marker labeled **Depot**.
5. Each order location is shown as a numbered circle.
6. Zoom, pan, and reset controls work correctly and the map stays responsive.
7. Route filter checkboxes correctly toggle visibility of individual routes and route groups.
8. The route list shows the order count for every visible vehicle and loader.
9. The route tables below the map accurately list stop sequences and times.
10. When all routes are hidden, a placeholder message is displayed: *"No route data available for the selected layer."*

### Execution history

| Date | Tester | Result | Evidence |
|---|---|---|---|
| 2026-07-02 | Customer | Passed — route map displayed all vehicle and loader routes in distinct colors. Zoom, pan, and filter controls worked correctly. The customer confirmed the visualization makes route analysis practical. | Private UAT recording (submitted via Moodle) |

---

## UAT-05: Review the skipped optional orders report

**Title:** Review the skipped optional orders report

**Status:** Passed

**Priority:** Medium

**Traceability:**
- User story: [US-09 — Skipped optional orders report](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/13)

### Preconditions

1. The application is running.
2. A problem instance JSON that includes at least one optional order (`"optional": 1`) is available.

### Test steps

#### Part A — Scenario with skipped optional orders

1. Open the web interface at `http://localhost:3000`.
2. Navigate to the **New Job** page.
3. Upload or paste a problem instance that contains optional orders (e.g. an instance where the time window or capacity constraints may cause some optional orders to be skipped).
4. Submit the job.
5. Wait for the solver to complete.
6. Open the completed job from the **Dashboard**.
7. Observe the area above the route map for the **Skipped optional orders** banner.

#### Part B — Scenario where all optional orders are served

8. Upload an instance where all optional orders fit within constraints.
9. Submit the job.
10. Open the completed job.
11. Observe that no skipped orders banner appears, or a message says *"No optional orders were skipped."*

### Expected results

1. For Part A: a yellow banner is displayed with the heading **Skipped optional orders** followed by a comma-separated list of skipped order IDs.
2. For Part B: either no banner is shown or a neutral message indicates no orders were skipped.
3. The skipped orders list is consistent with the solver's objective function (which includes a penalty per skipped optional order).
4. Downloading the job JSON via the **Download JSON** button includes the `unserved_optional` field in the result data.

### Execution history

| Date | Tester | Result | Evidence |
|---|---|---|---|
| 2026-07-02 | Customer | Passed — skipped optional orders correctly identified and displayed in a clear yellow banner. The customer confirmed this addresses prior feedback about transparency in which orders were not served. | Private UAT recording (submitted via Moodle) |

---

## Sprint 3 UAT Summary

**Session date:** 2026-07-02

**Tester:** Customer

**Recording:** Private UAT recording (submitted via Moodle)

### Scenarios executed

| ID | Title | Result |
|---|---|---|
| UAT-01 | Submit a delivery instance and receive an optimised solution | Passed |
| UAT-02 | Validate a custom solution through the validator | Passed |
| UAT-03 | Retrieve previously submitted solutions from history | Passed |
| UAT-04 | View route visualization for each vehicle and loader | Passed |
| UAT-05 | Review the skipped optional orders report | Passed |

### Summary of results

| Total | Passed | Failed | Blocked |
|---|---|---|---|
| 5 | 5 | 0 | 0 |

All 5 scenarios — 3 carry-over from MVP v1 and 2 new for Sprint 3 — passed without critical failures.

### Customer feedback points

1. **Route visualization was well received.** The customer confirmed that color-coded vehicle and loader routes on a single map make route analysis practical for daily use.
2. **Zoom, pan, and filter controls were intuitive.** The customer noted that being able to toggle individual route layers reduces visual clutter on complex instances.
3. **Skipped orders report addresses prior feedback.** The customer confirmed that the yellow banner clearly communicates which optional orders were not served, resolving the transparency concern raised in the Week 3 sprint review.
4. **Request for instance-level export.** The customer suggested adding a one-click export of the full job (input + result + validation) for offline review and reporting.
5. **Improved solver quality.** The customer observed that the new PyVRP-based solver produces noticeably better routes than the earlier OR-Tools version used in MVP v1.

### Items still needing improvement

1. **Job detail page responsiveness.** On large instances (hundreds of orders), the route map SVG rendering causes noticeable lag. Optimization of the SVG rendering pipeline is deferred to the next sprint.
2. **Map coordinate labels.** The current map does not display coordinate axis labels. The customer noted this is acceptable for MVP v2 but would be helpful for advanced analysis.

### Resulting PBIs and issues for the Product Backlog

| ID | Title | Priority | Notes |
|---|---|---|---|
| PBI-UAT-01 | Add one-click job export (input + result + validation) | Medium | Customer requested offline review capability. |
| PBI-UAT-02 | Optimize route map SVG rendering for large instances | Low | Acceptable for MVP v2; needed for scalability. |
| PBI-UAT-03 | Add coordinate axis labels to route map | Low | Nice-to-have for advanced analysis. |

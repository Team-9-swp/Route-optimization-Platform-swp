# User Acceptance Tests

## Purpose

This document defines end-user-facing acceptance test scenarios for the Route Optimization Platform and records sanitized public execution results. Private recording links, exact timecodes, customer identity, credentials, and private access details are intentionally excluded from the repository.

## Table of Contents

- [Active Scenarios](#active-scenarios)
- [UAT-01: Submit a delivery instance and receive an optimized solution](#uat-01-submit-a-delivery-instance-and-receive-an-optimized-solution)
- [UAT-02: Validate a custom solution through the validator](#uat-02-validate-a-custom-solution-through-the-validator)
- [UAT-03: Retrieve previously submitted solutions from history](#uat-03-retrieve-previously-submitted-solutions-from-history)
- [UAT-04: View route visualization for each vehicle and loader](#uat-04-view-route-visualization-for-each-vehicle-and-loader)
- [UAT-05: Review the skipped optional orders report](#uat-05-review-the-skipped-optional-orders-report)
- [UAT-06: Reproducible solver results with fixed seed](#uat-06-reproducible-solver-results-with-fixed-seed)
- [Sprint 5 UAT Summary](#sprint-5-uat-summary)
- [Week 6 UAT Summary](#week-6-uat-summary)
- [Week 7 Review Record](#week-7-review-record)

## Active Scenarios

| ID | Title | Status | Priority | Traceability |
|---|---|---|---|---|
| UAT-01 | Submit a delivery instance and receive an optimised solution | Passed | High | US-01a, US-01b, US-02, US-07, US-08; QR-FC-01 |
| UAT-02 | Validate a custom solution through the validator | Passed | High | US-03; QR-FC-01 |
| UAT-03 | Retrieve previously submitted solutions from history | Passed | High | US-08; QR-RE-01 |
| UAT-04 | View route visualization for each vehicle and loader | Passed | High | US-10; QR-FC-01 |
| UAT-05 | Review the skipped optional orders report | Passed | Medium | US-09 |
| UAT-06 | Reproducible solver results with fixed seed | Passed | Medium | US-06 |

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

1. The job completes with status `completed`.
2. The solution is automatically validated — validation status shows `valid`.
3. The **Job Detail** page displays:
   - objective function value;
   - a route map with vehicle and loader routes;
   - a route table for each vehicle (stops, arrival times, load);
   - a route table for each loader (assigned vehicles, schedule);
   - skipped optional orders report if applicable.
4. All displayed routes satisfy hard constraints (capacity, time windows, shift length).

### Execution Record

| Date | Tester | Result | Evidence |
|---|---|---|---|
| 2026-06-27 | Customer | Passed — all expected results confirmed. Solution completed, auto-validated as valid, route map and tables displayed correctly. | Private UAT recording (submitted via Moodle) |
| 2026-07-02 | Customer | Passed — all original results confirmed. Skipped optional orders report now correctly displayed alongside existing detail. | Private UAT recording (submitted via Moodle) |
| 2026-07-10 | Customer | Passed — Week 6 trial reconfirmed. All expected results unchanged; solution completes, auto-validates, route map and tables display correctly. Customer confirmed acceptance. | Private UAT recording (submitted via Moodle) |

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

| Date | Tester | Result | Evidence |
|---|---|---|---|
| 2026-06-27 | Customer | Passed — both valid and invalid solutions correctly identified. Valid solution displayed green status; invalid solution showed specific violation details. No internal details exposed. | Private UAT recording (submitted via Moodle) |
| 2026-07-02 | Customer | Passed — validator continues to work correctly with no regressions. | Private UAT recording (submitted via Moodle) |
| 2026-07-10 | Customer | Passed — Week 6 trial reconfirmed. Valid and invalid solutions correctly identified; no internal details exposed. Customer confirmed acceptance. | Private UAT recording (submitted via Moodle) |

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

| Date | Tester | Result | Evidence |
|---|---|---|---|
| 2026-06-27 | Customer | Passed — dashboard displayed all previous jobs. Completed job details (solution, validation, map) fully accessible. | Private UAT recording (submitted via Moodle) |
| 2026-07-02 | Customer | Passed — all historical jobs accessible after restart. Persistence confirmed. Skipped orders data preserved. | Private UAT recording (submitted via Moodle) |
| 2026-07-10 | Customer | Passed — Week 6 trial reconfirmed. Dashboard lists all jobs; historical data complete after restart. Customer confirmed acceptance. | Private UAT recording (submitted via Moodle) |

Private recording URLs, exact UAT/Sprint Review timecodes, customer identity, and recording permission evidence are submitted through Moodle only and are intentionally excluded from the public repository.

### Resulting Backlog Items

| Feedback or observation | Resulting issue | Public status |
|---|---|---|
| Customer access must be reliable outside the university network or explicitly agreed through another method. | [#90](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/90) | Still open until deployment/access criteria are verified. |
| Combined Sprint Review/UAT evidence must remain available privately without exposing customer identity or links publicly. | [#91](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/91), [#92](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/92) | Private recording details are supplied through Moodle only and are intentionally excluded from the repository. |

---

## UAT-04: View Route Visualization for Each Vehicle and Loader

**Stable ID:** UAT-04

**Title:** View route visualization for each vehicle and loader

**Traceability:**
- User story: [US-10 — Route visualization](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/14)
- Quality requirements: [QR-FC-01 — Solver functional correctness](quality-requirements.md#qr-fc-01--solver-functional-correctness)

### Preconditions

1. The application is running.
2. A completed job exists with vehicle and loader routes (e.g. from UAT-01).

### Steps

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

### Expected Result

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

### Execution Record

| Date | Tester | Result | Evidence |
|---|---|---|---|
| 2026-07-02 | Customer | Passed — route map displayed all vehicle and loader routes in distinct colors. Zoom, pan, and filter controls worked correctly. The customer confirmed the visualization makes route analysis practical. | Private UAT recording (submitted via Moodle) |
| 2026-07-10 | Customer | Passed — Week 6 trial reconfirmed. Route map, filters, and tables function correctly. Customer confirmed acceptance. | Private UAT recording (submitted via Moodle) |

---

## UAT-05: Review the Skipped Optional Orders Report

**Stable ID:** UAT-05

**Title:** Review the skipped optional orders report

**Traceability:**
- User story: [US-09 — Skipped optional orders report](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/13)

### Preconditions

1. The application is running.
2. A problem instance JSON that includes at least one optional order (`"optional": 1`) is available.

### Steps

#### Part A — Scenario with skipped optional orders

1. Open the web interface at `http://localhost:3000`.
2. Navigate to the **New Job** page.
3. Upload or paste a problem instance that contains optional orders and may leave some unserved because of its constraints.
4. Submit the job and wait for completion.
5. Open the completed job from the **Dashboard**.
6. Review the **Skipped optional orders** banner above the route map.

#### Part B — Scenario where all optional orders are served

7. Submit an instance where all optional orders fit within constraints.
8. Open the completed job.
9. Confirm that no skipped-orders warning is shown, or that the interface states that no optional orders were skipped.

### Expected Result

1. For Part A, a warning identifies the skipped optional order IDs.
2. For Part B, no warning is shown or a neutral message confirms that no optional orders were skipped.
3. The report is consistent with the solver result's `unserved_optional` data.
4. Downloaded job JSON includes `unserved_optional` in the result data.

### Execution Record

| Date | Tester | Result | Evidence |
|---|---|---|---|
| 2026-07-02 | Customer | Passed — skipped optional orders were identified and displayed clearly; the customer confirmed that this addressed the earlier transparency feedback. | Private UAT recording (submitted via Moodle) |

---

## UAT-06: Reproducible Solver Results with Fixed Seed

**Stable ID:** UAT-06

**Title:** Reproducible solver results with fixed seed

**Traceability:**
- User story: [US-06 — Reproducible random seed](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/10)

### Preconditions

1. The application is running.
2. A problem instance JSON (e.g. `test_cases/t1.json`) is available.

### Steps

#### Part A — Deterministic results with the same seed

1. Open the web interface at `http://localhost:3000`.
2. Navigate to the **New Job** page.
3. Upload or paste the problem instance JSON.
4. Set **Seed** to `42` and **Name** to `"Run A"`.
5. Submit the job and wait for completion.
6. Open the completed job and record the objective value and route structure.
7. Repeat steps 2–6 with **Seed** still `42` and **Name** set to `"Run B"`.
8. Compare the results of Run A and Run B.

#### Part B — Different seed produces a different result

9. Submit a third run with **Seed** set to a different value (e.g. `123`) and **Name** set to `"Run C"`.
10. Wait for completion and compare objective value and route structure with Run A.

### Expected Result

1. **Part A:** Run A and Run B produce identical objective values and identical route structures (vehicle routes, loader routes, unserved optional orders).
2. **Part B:** Run C may produce a different objective value or route structure compared to Run A, confirming that the seed influences the randomized parts of the solver.
3. The **Seed** field is visible in the **Job Detail** header.
4. The seed parameter is accepted by the API and persisted with the job record.

### Execution Record

| Date | Tester | Result | Evidence |
|---|---|---|---|
| 2026-07-02 | Customer | Passed — same seed produced identical results across two runs; different seed produced a different route structure. The customer confirmed that reproducibility enables consistent benchmarking and debugging. | Private UAT recording (submitted via Moodle) |
| 2026-07-10 | Customer | Passed — Week 6 trial reconfirmed. Same seed produces identical results; different seed yields different routes. Customer confirmed acceptance. | Private UAT recording (submitted via Moodle) |

---

## Sprint 5 UAT Summary

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
| UAT-06 | Reproducible solver results with fixed seed | Passed |

### Summary of results

| Total | Passed | Failed | Blocked |
|---|---|---|---|
| 6 | 6 | 0 | 0 |

All 6 scenarios passed without critical failures. The stable IDs now preserve skipped-orders reporting as UAT-05 and identify fixed-seed reproducibility separately as UAT-06.

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

---

## Week 6 UAT Summary

**Session date:** 2026-07-10

**Tester:** Customer

**Recording:** Private UAT recording (submitted via Moodle)

### Scenarios executed

| ID | Title | Result |
|---|---|---|
| UAT-01 | Submit a delivery instance and receive an optimised solution | Passed |
| UAT-02 | Validate a custom solution through the validator | Passed |
| UAT-03 | Retrieve previously submitted solutions from history | Passed |
| UAT-04 | View route visualization for each vehicle and loader | Passed |
| UAT-06 | Reproducible solver results with fixed seed | Passed |

### Summary of results

| Total | Passed | Failed | Blocked |
|---|---|---|---|
| 5 | 5 | 0 | 0 |

All 5 scenarios were reconfirmed during the Week 6 trial session. All scenarios passed — no regressions were observed since the Sprint 5 UAT (2026-07-02).

### Customer feedback points

1. **All 5 scenarios accepted.** The customer confirmed that all acceptance criteria remain satisfied and the product meets the expected behavior for trial use.
2. **Solver determinism verified.** The customer noted that same-seed reproducibility now works correctly (previously inconsistent in Sprint 5 review), confirming the fix from commits `d3181fe` and `da1bb98`.
3. **Product access via screen sharing.** The customer acknowledged that external deployment access is still pending but screen sharing remains an acceptable interim method for the trial.

### Items still needing improvement

1. **External customer access.** Deployment access outside the university network is still unresolved and tracked in [#90](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/90). The customer confirmed this is acceptable for the Week 6 trial but expects a resolution for Week 7 transition.
2. **Route map responsiveness on large instances.** Previously noted SVG rendering lag on large instances remains deferred; acceptable for trial use.

### Resulting PBIs and issues for the Product Backlog

| ID | Title | Priority | Notes |
|---|---|---|---|
| PBI-W6-01 | Resolve external customer deployment access for Week 7 transition | High | Customer confirmed this is the critical path for transition confirmation. |

---

## Week 7 Review Record

**Session date:** 2026-07-16

**Evidence type:** Sanitized meeting notes derived from the private recording transcript. This was a discussion/review record, not a complete customer execution of the final product.

| Changed behavior or transition topic | Result | Evidence and follow-up |
|---|---|---|
| Actual execution-duration display on Job Detail | Discussed | The team told the customer the duration display had been added. No customer-side execution was recorded. Implementation evidence is [PR #205](https://github.com/Team-9-swp/Route-optimization-Platform-swp/pull/205). |
| Two-decimal Objective display | Discussed | The team told the customer rounding had been added to avoid long floating-point tails. No customer-side execution was recorded. Implementation evidence is [PR #205](https://github.com/Team-9-swp/Route-optimization-Platform-swp/pull/205). |
| Finished interactive route and schedule visualization | Blocked | The visualization was still being finalized and was not demonstrated in its finished state during the meeting. The merged implementation is team-verified; that does not turn it into customer-executed UAT. |
| Customer-side reproduction and transition | Not executed | The customer emphasized reproducing the product and obtaining comparable results in their own internal/local environment. Successful customer-side deployment or operation is not verified; follow-up remains in [#187](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/187). |

**Handover level:** `Ready for independent use`

**Customer-confirmation status at the Sprint Review:** `Accepted with follow-up items`

The discussion supports readiness and usefulness, but it does not replace customer execution of the changed behavior. Private recording links, exact timecodes, customer identity, and consent evidence remain outside the public repository.

### Final Week 7 confirmation

| Confirmation area | Result | Scope |
|---|---|---|
| Customer-facing documentation set | Reviewed/Accepted | Root README, handover, deployment, usage, troubleshooting/support, and known limitations were confirmed sufficient. |
| Reached handover scope and transition model | Reviewed/Accepted | The customer accepted `Ready for independent use` and the documented source/Compose handover path. |
| Final corrections and Assignment 6 result | Reviewed/Accepted | The final changes and reached product state were accepted. |
| Merged product behavior | Team-verified | Repository CI/build/test evidence verifies merged changes; this is not relabelled as customer execution. |
| Customer-side deployment and independent reproduction | Not executed | No inspectable customer-side execution evidence is available. |

**Final handover level:** `Ready for independent use`

**Final customer-confirmation status:** `Accepted`

The final confirmation closes the documentation and administrative acceptance questions. It does not change any product scenario to `Passed by customer` unless the customer actually executed that scenario.

# Customer Feedback Response

## Sources

- Customer Sprint Review — 19 June 2026.
- Assignment 4 customer meeting — 26 June 2026.

The 26 June 2026 meeting recording was not saved because of a technical recording failure. The response below is based on the team notes and the feedback points recorded after the meeting.

## Feedback response table

| Feedback point | Resulting PBI or issue | Status | Response |
|---|---|---|---|
| The customer requested a clear two-dimensional route visualization instead of a real geographic map. | [#14 — Route visualization](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/14) | Done | The coordinate-plane route visualization was implemented, verified against the acceptance criteria, and closed as work from the previous increment. |
| The customer requested visibility into optional orders that were not served. | [#13 — Skipped optional orders report](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/13) | Selected for Assignment 4 | The team selected a skipped optional orders report for the current Sprint. The completed result should identify optional orders that were not assigned to any route. |
| The customer requested calculation history and confirmed that persistent storage is appropriate for a dynamic interface. | [#85 — Persist jobs and results across restarts](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/85) | Selected for Assignment 4 | The team selected persistent storage so submitted jobs and completed results remain available after application or container restarts. Retention and automatic cleanup are deferred. |
| The customer requested measurement of solver execution time. | [#87 — Define quality requirements and QRT specifications](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/87), [#88 — Add automated tests, coverage, and QA checks](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/88) | Selected for Assignment 4 | The measurable quality requirement and QRT specification were completed in #87. Automated test, coverage, and CI evidence remain planned through #88. |
| The customer requested improving solver quality, especially for scenarios where the current result is weaker than the baseline. | [#23 — Solver refactoring and performance](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/23), [#97 — Compare solver with baseline and analyze greedy-stage impact](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/97) | Follow-up required | The broad solver refactor remains in the Product Backlog as #23. A smaller investigation PBI, #97, now captures the reproducible baseline comparison before implementation decisions are made. |
| The customer recommended comparing the current solver with the baseline on the same scenarios and metrics. | [#97 — Compare solver with baseline and analyze greedy-stage impact](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/97) | Follow-up required | The team will run the current solver and the baseline on the same selected scenarios, with the same input data, runtime limit, and evaluation metric, then record objective values and execution times. |
| The customer suggested that the greedy stage may cause weaker objective values. | [#97 — Compare solver with baseline and analyze greedy-stage impact](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/97) | Follow-up required | The new investigation PBI asks the team to compare results with and without the greedy improvement stage where technically possible and document whether that stage improves or degrades solution quality. |
| The customer suggested considering vehicle routing, loader assignment, and optional-order selection more jointly instead of solving the major parts mainly in sequence. | [#23 — Solver refactoring and performance](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/23) | Deferred | A more joint optimization approach may improve solution quality but requires algorithm redesign and benchmarking. It is kept as broader Product Backlog work and is not planned as completed Assignment 4 work. |
| The customer could not access the deployed website because it is available only inside the Innopolis University network. | [#90 — Update VM deployment and create the Sprint release](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/90) | Selected for Assignment 4 | The deployment issue now requires either external customer access or another explicitly agreed remote access method, verified Docker run instructions as a fallback, and customer access testing before UAT. |
| The customer can run the application using Docker. | [#90 — Update VM deployment and create the Sprint release](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/90) | Selected for Assignment 4 | Docker remains the fallback access path. The Sprint release work must keep the Docker run instructions verified and usable if network access is still limited. |
| The customer suggested reproducibility comparison between repeated runs. | [#97 — Compare solver with baseline and analyze greedy-stage impact](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/97) | Not planned for this Sprint | The selected follow-up focuses first on same-scenario baseline comparison and greedy-stage impact. Dedicated repeated-run tooling is postponed until the baseline comparison clarifies whether it is needed. |
| The customer suggested Gantt-style schedules and workload-balancing visibility. | No current Sprint issue | Not planned for this Sprint | This was treated as lower priority than solver quality, deployment access, and the main visualization/reporting workflow. It may be reconsidered in a later Sprint. |

## Backlog updates completed

- Updated [#90 — Update VM deployment and create the Sprint release](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/90) with customer-access, Docker fallback, and pre-UAT access verification acceptance criteria.
- Updated [#23 — Solver refactoring and performance](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/23) with the 26 June 2026 solver feedback.
- Created [#97 — Compare solver with baseline and analyze greedy-stage impact](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/97) as a focused Product Backlog investigation item.

## Decisions

### Addressed or selected for Assignment 4

- Route visualization verification.
- Skipped optional orders report.
- Persistent job and result storage.
- Measurable solver correctness and execution-time requirements.
- Automated QRT, test, coverage, and QA evidence.
- Improved deployment accessibility or an explicitly agreed remote access method.
- Verified Docker run instructions as a fallback access path.

### Deferred or follow-up work

- Broad solver redesign.
- Joint vehicle-route, loader-assignment, and optional-order optimization.
- Greedy-stage redesign until #97 provides comparison evidence.
- Specialized optimization for smaller scenarios.
- Repeated-run reproducibility tooling.
- Gantt-style schedule and workload-balancing views.
- Automatic history-retention policies.

## Verification against issue #84

- Previous customer feedback was reviewed and included in the table.
- New Assignment 4 feedback from 26 June 2026 was recorded.
- Addressed feedback is linked to concrete issues.
- Deferred feedback includes a reason.
- The Week 4 report includes the required feedback response table directly.

# Customer Feedback Response

## Sources

- Customer Sprint Review - 19 June 2026.
- Combined recorded Sprint Review and customer UAT - 27 June 2026. Public files contain only sanitized summaries; private recording details are supplied through Moodle only.

## Feedback Response Table

| Feedback point | Resulting PBI or issue | Status | Response |
|---|---|---|---|
| The customer requested a clear two-dimensional route visualization instead of a real geographic map. | [#14 - Route visualization](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/14) | Done in earlier increment | The coordinate-plane route visualization was implemented and remains part of the product. |
| The customer requested visibility into optional orders that were not served. | [#13 - Skipped optional orders report](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/13) | Implemented | Solver output and public job responses now expose skipped optional orders through `unserved_optional`. |
| The customer requested calculation history and confirmed that persistent storage is appropriate for a dynamic interface. | [#85 - Persist jobs and results across restarts](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/85) | Implemented | Jobs, results, and validation metadata are stored in PostgreSQL through `app/repository.py`. Retention and automatic cleanup are deferred. |
| The customer requested measurement of solver execution time. | [#87](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/87), [#88](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/88) | Implemented and verified in CI | `QR-PE-01` and `QRT-PE-01` use a 900 second fixed benchmark threshold; PR #106 QRT CI passed. |
| The customer requested improving solver quality, especially for scenarios where the current result is weaker than the baseline. | [#23 - Solver refactoring and performance](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/23), [#97 - Compare solver with baseline and analyze greedy-stage impact](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/97) | Partially addressed; broader work deferred | The current solver benchmark is recorded in `reports/week4/solver-benchmark.md`. Broader solver redesign and deeper baseline interpretation remain Product Backlog work. |
| The customer recommended comparing the current solver with the baseline on the same scenarios and metrics. | [#97](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/97) | Evidence prepared through benchmark report | The public benchmark records current solver objective values, runtimes, and skipped optional orders on the `instances/i*.json` fixtures with fixed seed and time limit. |
| The customer suggested that the greedy stage may cause weaker objective values. | [#97](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/97), [#23](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/23) | Follow-up analysis | Greedy-stage impact remains a solver-quality investigation topic and should not be treated as fixed by documentation alone. |
| The customer suggested considering vehicle routing, loader assignment, and optional-order selection more jointly instead of solving the major parts mainly in sequence. | [#23](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/23) | Deferred | A more joint optimization approach may improve solution quality but requires algorithm redesign and additional benchmarking. |
| The customer could not access the deployed website because it was available only inside the Innopolis University network. | [#90 - Update VM deployment and create the Sprint release](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/90) | Open | The repository documents Docker Compose as the runnable fallback. External or explicitly agreed customer access and release evidence still need verification. |
| The customer can run the application using Docker. | [#90](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/90) | Documented | Root `README.md` contains Docker Compose, PostgreSQL, and migration instructions. |
| The customer suggested reproducibility comparison between repeated runs. | [#97](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/97) | Deferred beyond required gate | The selected Assignment 4 evidence uses fixed input and fixed seed. Dedicated repeated-run tooling is postponed. |
| The customer suggested Gantt-style schedules and workload-balancing visibility. | No current Sprint issue | Not planned for this Sprint | This was treated as lower priority than solver quality, deployment access, and core route/result workflows. |

## Backlog Updates

- [#13](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/13) is represented by skipped optional order reporting.
- [#85](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/85) is represented by PostgreSQL persistence and recoverability tests.
- [#87](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/87) is represented by quality requirements and QRT specifications.
- [#88](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/88) is represented by QRT implementation, CI workflow updates, and protected-main CI evidence from PR #106.
- [#90](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/90) remains open until deployment/customer access is actually verified.
- [#91](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/91) and [#92](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/92) track private Moodle-only recording evidence and public reporting consistency for the combined Sprint Review/UAT session.

## Deferred Feedback

The following feedback remains Product Backlog or follow-up work:

- broad solver redesign for quality and scalability;
- deeper baseline and greedy-stage analysis;
- repeated-run reproducibility tooling;
- joint optimization of vehicles, loaders, and optional order selection;
- workload-balancing and Gantt-style schedule views;
- automatic job retention and cleanup policies.

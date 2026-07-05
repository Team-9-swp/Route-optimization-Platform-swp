# Week 5 Report — MVP v2

## Assignment 5 Evidence Index

| Requirement area | Public evidence |
|---|---|
| Sprint 5 planning | [Roadmap](../../docs/roadmap.md), [Sprint 5 planning artifact](../../docs/assignment5-sprint5-planning.md) |
| Customer feedback response | [Customer Feedback Response](#customer-feedback-response) |
| Development process | [Development process](../../docs/development-process.md) |
| Architecture views | [Architecture documentation](../../docs/architecture/README.md) |
| ADRs | [ADR index](../../docs/architecture/adr/README.md) |
| Testing / QA / DoD | [Testing strategy](../../docs/testing.md), [Definition of Done](../../docs/definition-of-done.md) |
| UAT | [User Acceptance Tests](../../docs/user-acceptance-tests.md) |
| Sprint Review | [Sprint 5 Review Summary](sprint-review-summary.md) |
| Retrospective | [Retrospective](retrospective.md) |
| Reflection | [Reflection](reflection.md) |
| LLM usage | [LLM usage report](llm-report.md) |
| Hosted documentation | [Hosted documentation](https://team-9-swp.github.io/Route-optimization-Platform-swp/) |
| Demo video | [MVP v2 demo](https://disk.yandex.ru/i/CXjgSum-9lTAjg) |
| Release | GitHub Release: [v1.3.0](https://github.com/Team-9-swp/Route-optimization-Platform-swp/releases/tag/v1.3.0) |

## Customer Feedback Response

Public sources reviewed:

- [Week 2 customer meeting summary](../week2/customer-meeting-summary.md)
- [Week 2 sanitized customer meeting transcript](../week2/customer-meeting-transcript.md)
- [Week 3 customer review summary](../week3/customer-review-summary.md)
- [Week 3 sanitized customer review transcript](../week3/customer-review-transcript.md)
- [Week 4 customer feedback response](../week4/customer-feedback-response.md)
- [Week 4 customer review notes](../week4/customer-review-notes.md)
- [Week 4 customer review summary](../week4/customer-review-summary.md)
- [User acceptance tests](../../docs/user-acceptance-tests.md)
- [Roadmap](../../docs/roadmap.md)

Private recording links, customer identity, credentials, exact timecodes, and private access details are intentionally excluded from this public report.

| Feedback point | Resulting PBI or issue | Status | Response |
|---|---|---|---|
| The customer requested route visualization suitable for benchmark coordinates rather than a real geographic map. | [#14](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/14) | Done in an earlier Sprint | Coordinate-plane route visualization was completed earlier and remains part of the maintained product. |
| The customer requested visibility into optional orders that were not served. | [#13](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/13) | Done in an earlier Sprint | Skipped optional orders are reported in solver/API results; Sprint 5 keeps this as maintained product behavior. |
| The customer requested calculation history and confirmed that persistent storage is appropriate for a dynamic interface. | [#85](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/85) | Done in an earlier Sprint | Jobs, results, and validation metadata were moved to PostgreSQL-backed persistence. Retention and cleanup policy work remains outside this Part 2 task. |
| The customer requested measurement of solver execution time. | [#87](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/87), [#88](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/88) | Done in an earlier Sprint | Assignment 4 quality requirements and QRTs include solver time behaviour evidence; this report does not claim new Sprint 5 implementation. |
| The customer requested comparison with the baseline and investigation of whether the greedy stage weakens objective values. | [#97](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/97), [#127](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/127) | Continued in Sprint 5 | Closed issue #97 is historical benchmark context only. Sprint 5 continues the investigation in #127 with fixed scenarios, seeds, metrics, and at least one modified solver alternative. |
| The customer recommended considering a more joint approach to vehicle routes, loader assignments, and optional-order selection. | [#23](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/23), [#127](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/127) | Continued in Sprint 5 | Closed issue #23 is historical context only. Sprint 5 uses #127 to document current fixed decisions and decide whether the solver pipeline should be changed. |
| The customer needed product access outside the university network or another explicitly agreed remote access method. | [#90](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/90), [#115](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/115) | Continued in Sprint 5 | Issue #90 records the Assignment 4 deployment/release work and is now closed. Sprint 5 keeps customer-accessible deployment and release evidence in #115. |
| The customer described balanced driver/loader workload as a possible later-stage business requirement. | [#124](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/124) | Planned for Sprint 5 | Sprint 5 plans to define a workload-balance metric, reproduce current behavior, and add solver/regression evidence before claiming a product change. |
| The customer discussed Gantt-style schedules as a way to show vehicle/loader activity and idle time. | [#125](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/125) | Planned for Sprint 5 | Sprint 5 plans a Gantt schedule visualization; the issue remains open and no implementation is claimed here. |
| The customer recommended reviewing column generation as a potentially stronger optimization approach, while noting implementation complexity. | [#128](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/128) | Research spike | Sprint 5 treats column generation as research only: analysis, small prototype where feasible, comparison on small scenarios, limitations, and an ADR decision. |
| The customer suggested comparing repeated runs or reproducibility beyond a single fixed benchmark. | [#127](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/127) | Deferred | Sprint 5 #127 uses fixed scenarios and seeds for a reproducible baseline. Dedicated repeated-run stability tooling is deferred until the baseline and greedy-stage analysis are reviewed. |

## Internal MVP v2 Improvements

The following Sprint 5 items are internal product, architecture, delivery, or research improvements rather than direct customer feedback:

- [#126](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/126) — validator-compatible solution JSON export; this improves product interoperability and regression coverage, but the inspected feedback does not explicitly request downloaded solution JSON compatibility.
- [#129](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/129) — known product bug fix; the issue requires reproduction details before implementation starts and is not attributed to customer feedback here.
- [#130](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/130) — automatic deployment from protected `main`; this supports delivery reliability, but the inspected customer feedback asks for accessible product access, not this specific automation workflow.

## Documentation

📖 **[View the Hosted Documentation](https://team-9-swp.github.io/Route-optimization-Platform-swp/)**

## Sprint Review

- [Sprint 5 Review Summary](sprint-review-summary.md)
- Combined Sprint Review and UAT recording: private Moodle submission only.
- Exact recording timecodes, recording permission evidence, and private access details are intentionally excluded from the public repository.

## Demo

**[view Demo](https://disk.yandex.ru/i/CXjgSum-9lTAjg)**

## MVP v2 Release and Deployment

MVP v2 is released as `v1.3.0`.

Public release evidence:
- GitHub Release: TBD
- Changelog: [CHANGELOG.md](../../CHANGELOG.md)
- Hosted documentation: https://team-9-swp.github.io/Route-optimization-Platform-swp/
- Demo video: https://disk.yandex.ru/i/CXjgSum-9lTAjg

Private access details, exact deployment access instructions, recording links, and exact timecodes are submitted through Moodle only.

## Deferred and Follow-up Work

| Item | Issue | Sprint 5 decision |
|---|---|---|
| Gantt schedule visualization | #125 | Deferred to the next Sprint. |
| Loader workload balance | #124 | Kept as future work. |
| Solver pipeline and greedy-stage impact | #127 | Continued next week because more investigation time is required. |
| Column generation | #128 | Investigated and considered not useful enough for the current problem scope. |

## Contribution Traceability

| Team member | Assignment 5 responsibility | Technical / process contribution |
|---|---|---|
| Elvina Belorusova | Parts 1, 2, 9, Week 5 report / Moodle report | Sprint planning, customer feedback traceability, Sprint Review evidence, final reporting |
| Adelia | Parts 7, 10, 11, 12, 13, 14 | Release support, retrospective, hosted docs, reflection, demo video, LLM report |
| Matvey | Part 6 | Testing, QA, Definition of Done |
| Aidar | Part 8 | UAT scenarios and customer-facing validation |
| Valera | Parts 3, 4, 5 | Development process, architecture documentation, ADRs |

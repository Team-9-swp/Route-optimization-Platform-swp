# Week 4 Report — Assignment 4

## Project

**Route Optimization Platform** — a logistics optimisation system that generates vehicle and loader routes for the BIA CVRPTW problem variant.
License: [MIT](../../LICENSE)

## Solver benchmark

- [`solver-benchmark.md`](./solver-benchmark.md) — reproducible objective/runtime comparison across all `instances/i*.json` fixtures using the new PyVRP + Nevergrad solver.

| Feedback point | Resulting PBI or issue | Status | Response |
|---|---|---|---|
| The customer requested a clear two-dimensional route visualization instead of a real geographic map. | [#14 — Route visualization](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/14) | Done | The coordinate-plane route visualization was implemented, verified against the acceptance criteria, and closed as work from the previous increment. |
| The customer requested visibility into optional orders that were not served. | [#13 — Skipped optional orders report](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/13) | Selected for Assignment 4 | The team selected a skipped optional orders report for the current Sprint. The completed result identifies optional orders that were not assigned to any route. |
| The customer requested calculation history and confirmed that persistent storage is appropriate for a dynamic interface. | [#85 — Persist jobs and results across restarts](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/85) | Selected for Assignment 4 | The team selected persistent storage so submitted jobs and completed results remain available after application or container restarts. Retention and automatic cleanup are deferred. |
| The customer requested measurement of solver execution time. | [#87 — Define quality requirements and QRT specifications](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/87), [#88 — Add automated tests, coverage, and QA checks](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/88) | Selected for Assignment 4 | The measurable quality requirement and QRT specification were completed in #87. Automated QRTs are implemented in `tests/quality/`. |
| The customer requested improving solver quality, especially for scenarios where the current result is weaker than the baseline. | [#23 — Solver refactoring and performance](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/23), [#97 — Compare solver with baseline and analyze greedy-stage impact](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/97) | Follow-up required | The broad solver refactor remains in the Product Backlog as #23. A reproducible benchmark is now in `reports/week4/solver-benchmark.md`. |
| The customer recommended comparing the current solver with the baseline on the same scenarios and metrics. | [#97 — Compare solver with baseline and analyze greedy-stage impact](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/97) | Follow-up required | The team runs the current solver on the official `instances/i*.json` fixtures with a fixed seed and time limit, recording objective values and execution times. |
| The customer suggested considering vehicle routing, loader assignment, and optional-order selection more jointly instead of solving the major parts mainly in sequence. | [#23 — Solver refactoring and performance](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/23) | Deferred | A more joint optimization approach may improve solution quality but requires algorithm redesign and benchmarking. It is kept as broader Product Backlog work and is not planned as completed Assignment 4 work. |
| The customer could not access the deployed website because it is available only inside the Innopolis University network. | [#90 — Update VM deployment and create the Sprint release](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/90) | Selected for Assignment 4 | The deployment issue now requires either external customer access or another explicitly agreed remote access method, verified Docker run instructions as a fallback, and customer access testing before UAT. |
| The customer can run the application using Docker. | [#90 — Update VM deployment and create the Sprint release](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/90) | Selected for Assignment 4 | Docker remains the fallback access path. The Sprint release work must keep the Docker run instructions verified and usable if network access is still limited. |
| The customer suggested reproducibility comparison between repeated runs. | [#97 — Compare solver with baseline and analyze greedy-stage impact](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/97) | Not planned for this Sprint | The selected follow-up focuses first on same-scenario baseline comparison. Dedicated repeated-run tooling is postponed until the baseline comparison clarifies whether it is needed. |
| The customer suggested Gantt-style schedules and workload-balancing visibility. | No current Sprint issue | Not planned for this Sprint | This was treated as lower priority than solver quality, deployment access, and the main visualization/reporting workflow. It may be reconsidered in a later Sprint. |

## Demo Video

[Public sanitized demo video](https://drive.google.com/file/d/15Dh_azNvTxptEjW1XX4S__jnOmg84rHg/view?usp=sharing)

## Quality Requirements

The quality model follows ISO/IEC 25010. The following sub-characteristics were selected for Assignment 4:

| ID | Sub-characteristic | Requirement |
|---|---|---|
| QR-FC-01 | Functional correctness | Solver output must satisfy all hard constraints for valid supported input instances. |
| QR-PE-01 | Time behaviour | Fixed CI benchmark must complete within the configured time limit plus tolerance. |
| QR-RE-01 | Recoverability | Submitted jobs and completed results must remain available after application restart. |
| QR-SE-01 | Confidentiality | API responses must not expose stack traces, internal file paths, or implementation details. |

See [docs/quality-requirements.md](../../docs/quality-requirements.md) for full definitions.

## Testing Status

### Critical Modules and Coverage

| Critical module | Why critical | Required coverage | Current coverage |
|---|---|---|---|
| `app/service.py` | Core orchestration of solver jobs and validation | 30% | TBD |
| `app/repository.py` | Persistent job storage | 30% | TBD |
| `app/api.py` | Public-facing REST endpoints and request validation | 30% | TBD |

### Test Suites

| Test type | Scope | Location | Status |
|---|---|---|---|
| Unit/integration tests | Schemas, Repository, Validation, Service, Runner, API | [tests/](../../tests/) | Passing |
| Automated QRTs | QR-FC-01, QR-PE-01, QR-RE-01, QR-SE-01 | [tests/quality/](../../tests/quality/) | 9 passing |

See [docs/testing.md](../../docs/testing.md) for full details.

## CI Pipeline

The CI pipeline runs on every PR and push to `main` via GitHub Actions:

- **Backend job:** Python setup, Ruff linting, Black format check, pytest with coverage, QRTs, Bandit security scan
- **Frontend job:** Node.js setup, dependency install, Vite production build

**Pipeline:** [ci.yml](../../.github/workflows/ci.yml)

### Continued Governance

All Assignment 4 quality gates remain active for later project work:

- Ruff linting and Black formatting are required checks before merge
- Unit, integration, and QRTs run automatically on every PR and push to `main`
- Critical modules must maintain >=30% line coverage
- Bandit security scan runs as the additional QA check

## Sprint Review status

A customer meeting was conducted on 26 June 2026. The recording was not saved because of a technical recording failure.

The customer could not access the hosted application because the current university VM deployment is limited to the Innopolis University network. As a result, customer-executed UAT and final acceptance were not completed.

- [Customer review notes](customer-review-notes.md)
- [Customer review summary](customer-review-summary.md)

A follow-up recorded Sprint Review and customer-executed UAT session is required after customer access is available.

[#92](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/92) remains open until the follow-up Sprint Review and all required review evidence are complete.

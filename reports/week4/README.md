# Week 4 Public Submission Index - Assignment 4

## Project

**Route Optimization Platform** is a logistics optimization system for the BIA CVRPTW problem variant. It provides a FastAPI backend, PostgreSQL-backed job history, a PyVRP/Nevergrad solver pipeline, validation, skipped optional order reporting, and a React web interface.

License: [MIT](../../LICENSE)

## Planning Links

| Item | Public link |
|---|---|
| Product Backlog | [GitHub Project Product Backlog](https://github.com/orgs/Team-9-swp/projects/1/views/1) |
| Assignment 4 Sprint Backlog | [GitHub Project Sprint Backlog](https://github.com/orgs/Team-9-swp/projects/1/views/3) |
| Assignment 4 milestone | [Assignment 4 Sprint milestone](https://github.com/Team-9-swp/Route-optimization-Platform-swp/milestone/5) |
| Roadmap | [docs/roadmap.md](../../docs/roadmap.md) |

**Sprint dates:** 22 June 2026 - 3 July 2026

**Sprint Goal:** Deliver a more reliable and verifiable Route Optimization Platform by addressing selected customer feedback, preserving submitted jobs across restarts, improving solver robustness, and enforcing automated quality gates through tests and CI.

**Selected Assignment 4 scope:** skipped optional order reporting, PostgreSQL persistence, solver robustness, quality requirements, automated QRTs, CI/test/coverage gates, deployment/release preparation, customer UAT evidence, Sprint Review evidence, and public Week 4 reporting.

**Total selected Story Points:** 46, derived from the Assignment 4 milestone scope inspected during PR #95 planning.

<!--
Screenshots to be added manually before submission:
reports/week4/images/sprint-milestone.png
reports/week4/images/protected-main-ci.png
reports/week4/images/branch-protection.png
reports/week4/images/coverage-tests.png
reports/week4/images/additional-qa-bandit.png
reports/week4/images/semver-release.png
reports/week4/images/reviewed-pr.png
reports/week4/images/product-backlog.png
reports/week4/images/sprint-backlog.png
-->

## Delivered Product Changes

| Change | Evidence |
|---|---|
| PostgreSQL persistence for jobs, results, validation metadata, and history. | [#85](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/85), [PR #105](https://github.com/Team-9-swp/Route-optimization-Platform-swp/pull/105), `app/repository.py` |
| Skipped optional orders returned in solver output and API responses. | [#13](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/13), [PR #105](https://github.com/Team-9-swp/Route-optimization-Platform-swp/pull/105) |
| PyVRP/Nevergrad solver integrated with async runner. | [PR #105](https://github.com/Team-9-swp/Route-optimization-Platform-swp/pull/105), [solver benchmark](./solver-benchmark.md) |
| Safe solver failure handling. | [#86](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/86), `tests/quality/test_qrt_confidentiality.py` |
| Assignment 4 quality requirements and QRT specifications. | [quality requirements](../../docs/quality-requirements.md), [QRT specification](../../docs/quality-requirement-tests.md) |
| Blocking CI lint/format gates and frontend type checking. | [CI workflow](../../.github/workflows/ci.yml), [frontend/package.json](../../frontend/package.json) |
| Draft `v1.2.0` release notes. | [release-notes-v1.2.0.md](./release-notes-v1.2.0.md), [CHANGELOG.md](../../CHANGELOG.md) |

## Deployment and Runnable Product Status

The product is runnable through Docker Compose:

```bash
docker compose up --build
```

Open:

- API docs: `http://localhost:8000/docs`
- Web app: `http://localhost:3000`

PostgreSQL and migrations for local development:

```bash
docker compose up -d db
alembic upgrade head
python -m uvicorn app.main:app --reload
```

Current access status:

- Docker Compose is the documented runnable fallback.
- The university VM deployment is documented as limited to the Innopolis University network.
- Customer access from outside that network is not publicly verified.
- An ngrok or similar tunnel is only evidence if it is explicitly agreed and verified during a customer session.
- [#90](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/90) remains open until deployment/access and the final post-merge release are verified.

## Customer Feedback Response

See also [customer-feedback-response.md](./customer-feedback-response.md).

| Feedback point | Resulting PBI or issue | Status | Response |
|---|---|---|---|
| Show skipped optional orders. | [#13](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/13) | Implemented | Completed solutions expose `unserved_optional`. |
| Preserve calculation history. | [#85](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/85) | Implemented | Jobs/results are persisted in PostgreSQL. |
| Measure solver execution time. | [#87](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/87), [#88](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/88) | Implemented in code; final PR CI evidence pending | `QR-PE-01` and `QRT-PE-01` use a 900 second threshold. |
| Compare solver quality and investigate greedy-stage impact. | [#97](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/97), [#23](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/23) | Benchmark prepared; broader work deferred | Current solver benchmark is recorded in [solver-benchmark.md](./solver-benchmark.md). |
| Provide accessible deployment or another agreed customer access method. | [#90](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/90) | Open | Docker fallback is documented; external access verification is still required. |
| Consider joint vehicle/loader/optional-order optimization. | [#23](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/23) | Deferred | Requires solver redesign and additional benchmarking. |

## Definition of Done and Quality Model

| Artifact | Link |
|---|---|
| Definition of Done | [docs/definition-of-done.md](../../docs/definition-of-done.md) |
| Quality requirements | [docs/quality-requirements.md](../../docs/quality-requirements.md) |
| Quality requirement tests | [docs/quality-requirement-tests.md](../../docs/quality-requirement-tests.md) |
| Testing strategy and status | [docs/testing.md](../../docs/testing.md) |
| User acceptance tests | [docs/user-acceptance-tests.md](../../docs/user-acceptance-tests.md) |

Quality-model summary:

| ID | ISO/IEC 25010 characteristic | Sub-characteristic | Automated evidence |
|---|---|---|---|
| `QR-FC-01` | Functional suitability | Functional correctness | `QRT-FC-01` |
| `QR-PE-01` | Performance efficiency | Time behaviour | `QRT-PE-01`, 900 second threshold |
| `QR-RE-01` | Reliability | Recoverability | `QRT-RE-01` |
| `QR-SE-01` | Security | Confidentiality | `QRT-SE-01` |

## Coverage and Test Evidence

Latest local non-integration coverage command:

```bash
python -m pytest tests --ignore=tests/quality --ignore=tests/test_e2e.py -m "not slow and not integration" --cov=app --cov-report=term-missing --cov-report=xml
```

Latest local result on 28 June 2026:

- `14 passed`
- `26 deselected`
- coverage XML written to `coverage.xml`

| Critical module | Required coverage | Latest local non-integration coverage | Gate status |
|---|---:|---:|---|
| `app/service.py` | 30% | 53% | Meets local threshold |
| `app/repository.py` | 30% | 25% | Needs PR CI with PostgreSQL integration tests |
| `app/api.py` | 30% | 70% | Meets local threshold |

The final Assignment 4 coverage evidence must come from PR CI or protected-main CI after PostgreSQL integration tests run.

Test links:

- Unit and integration tests: [tests/](../../tests/)
- Repository integration tests: [tests/test_repository.py](../../tests/test_repository.py)
- API persistence tests: [tests/test_api_persistence.py](../../tests/test_api_persistence.py)
- Validator integration tests: [tests/test_validator.py](../../tests/test_validator.py)
- QRTs: [tests/quality/](../../tests/quality/)

QRT result table:

| QRT | Files | Threshold | Latest local evidence | Final evidence status |
|---|---|---|---|---|
| `QRT-FC-01` | `test_qrt_functional_correctness.py`, `test_solver_correctness.py` | Completed solver job validates with zero hard-constraint violations | Direct solver support included in `5 passed` run | API/PostgreSQL QRT must run in PR CI |
| `QRT-PE-01` | `test_qrt_time_behaviour.py`, `test_solver_time_behaviour.py` | Fixed benchmark <= 900 s; configured limit terminal within limit + 10 s | Direct solver support included in `5 passed` run, total 147.18 s | API/PostgreSQL QRT must run in PR CI |
| `QRT-RE-01` | `test_job_recoverability.py` | Completed job/result/validation metadata survive repository/application recreation | Collected under both markers | PostgreSQL QRT must run in PR CI |
| `QRT-SE-01` | `test_qrt_confidentiality.py`, `test_safe_error_confidentiality.py` | Public response contains no traceback, internal path, or fake secret | Collected under both markers | API/PostgreSQL QRT must run in PR CI |

Marker discovery:

- `pytest tests/quality -m "qrt" --collect-only -q`: 15 tests collected.
- `pytest tests/quality -m "quality" --collect-only -q`: 15 tests collected.

## CI and QA Status

| Gate | Status |
|---|---|
| CI workflow | [ci.yml](../../.github/workflows/ci.yml) updated |
| Latest protected-main CI run before this PR | [CI Pipeline run 28332128956](https://github.com/Team-9-swp/Route-optimization-Platform-swp/actions/runs/28332128956); this predates the current blocking-gate fixes |
| Latest protected-main link check before this PR | [Link Check run 28332128943](https://github.com/Team-9-swp/Route-optimization-Platform-swp/actions/runs/28332128943) |
| Ruff | Passing locally and blocking in workflow |
| Black | Passing locally and blocking in workflow |
| Backend fast tests | Passing locally: 14 passed |
| Backend full integration tests | Pending PR CI |
| QRT execution | Direct solver support passed locally; full PostgreSQL QRT pending PR CI |
| Coverage artifact upload | Configured in workflow |
| Bandit | Passing locally: no medium/high severity issues across 537 lines |
| Frontend typecheck | Configured; pending PR CI because local Node/npm are unavailable |
| Frontend build | Configured; pending PR CI because local Node/npm are unavailable |
| Branch protection / required checks | Pending organization-admin verification |

Continued governance:

- Ruff and Black must remain blocking.
- Unit, integration, and QRT suites must keep running on PRs and pushes to `main`.
- Critical modules must maintain at least 30% coverage after integration tests run.
- Bandit remains the additional QA gate for medium/high severity findings.
- Branch protection should require the backend and frontend CI jobs once an organization admin verifies the settings.

## Release Status

The existing `v1.1.0` release predates PR #105 and does not contain the final Assignment 4 increment.

Prepared release:

- planned version: `v1.2.0`;
- draft notes: [release-notes-v1.2.0.md](./release-notes-v1.2.0.md);
- changelog: [CHANGELOG.md](../../CHANGELOG.md).

Final release status: post-merge pending. The GitHub release must be created from the merge commit on `main`, not from this PR branch.

Post-merge command:

```bash
gh release create v1.2.0 --target main --title "v1.2.0 - Assignment 4 Quality Gates and Persistent Jobs" --notes-file reports/week4/release-notes-v1.2.0.md
```

## Demo, Presentation, and Reports

| Artifact | Link |
|---|---|
| Public sanitized demo video | [Google Drive video](https://drive.google.com/file/d/15Dh_azNvTxptEjW1XX4S__jnOmg84rHg/view?usp=sharing) |
| Presentation | [presentation.pdf](./presentation.pdf) |
| Customer review notes | [customer-review-notes.md](./customer-review-notes.md) |
| Customer review summary | [customer-review-summary.md](./customer-review-summary.md) |
| Retrospective | [retrospective.md](./retrospective.md) |
| Reflection | [reflection.md](./reflection.md) |
| LLM usage report | [llm-report.md](./llm-report.md) |
| Solver benchmark | [solver-benchmark.md](./solver-benchmark.md) |

No public customer-review transcript is included because publication permission for a transcript is not documented.

## UAT and Sprint Review Status

UAT timeline:

- 26 June 2026: UAT was not completed because customer access to the hosted product was blocked.
- 27 June 2026: a separate recorded customer UAT session exists.

Sanitized UAT summary:

| Scenario | Result | Public evidence | Private evidence required |
|---|---|---|---|
| UAT-01 - Submit a delivery instance and receive an optimized solution | Passed according to sanitized UAT notes | [docs/user-acceptance-tests.md](../../docs/user-acceptance-tests.md) | Recording URL, exact timecodes, permission evidence |
| UAT-02 - Validate a custom solution through the validator | Passed according to sanitized UAT notes | [docs/user-acceptance-tests.md](../../docs/user-acceptance-tests.md) | Recording URL, exact timecodes, permission evidence |
| UAT-03 - Retrieve previously submitted solutions from history | Passed according to sanitized UAT notes | [docs/user-acceptance-tests.md](../../docs/user-acceptance-tests.md) | Recording URL, exact timecodes, permission evidence |

Sprint Review status:

- 26 June notes are partial Sprint Review evidence only.
- The 26 June recording was not saved.
- The public notes do not verify that the 27 June recording covers all required Sprint Review topics.
- [#92](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/92) should remain open unless private evidence verifies the full Sprint Review agenda or a follow-up review is recorded.

Resulting PBIs:

- deployment/access and release: [#90](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/90);
- UAT private evidence: [#91](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/91);
- Sprint Review evidence: [#92](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/92);
- solver-quality follow-up: [#23](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/23), [#97](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/97).

## Current Product Status

Implemented:

- PostgreSQL job persistence;
- skipped optional orders;
- current PyVRP/Nevergrad solver integration;
- user-safe solver failure messages;
- QRT implementation and marker discovery;
- CI workflow updates for blocking lint/format, backend tests, QRTs, Bandit, frontend typecheck, and frontend build;
- draft `v1.2.0` release documentation.

Pending:

- push branch and open PR after Codex elevated-action limit resets;
- PR CI full verification;
- branch-protection / required-check verification;
- manually added screenshots;
- private UAT recording metadata;
- final Sprint Review verification;
- deployment/customer-access verification;
- post-merge `v1.2.0` GitHub release.

## Contribution Traceability

This table maps repository accounts to public evidence visible in git history, issues, or PRs. It does not invent private work.

| Contributor/account | Evidence | Area |
|---|---|---|
| `quaaow` | [PR #105](https://github.com/Team-9-swp/Route-optimization-Platform-swp/pull/105), [PR #102](https://github.com/Team-9-swp/Route-optimization-Platform-swp/pull/102), commits for PostgreSQL repository, QRTs, CI, benchmark, and solver/API integration | Backend implementation, persistence, tests, CI, benchmark, quality gates |
| `belelvser` | [PR #95](https://github.com/Team-9-swp/Route-optimization-Platform-swp/pull/95), [PR #96](https://github.com/Team-9-swp/Route-optimization-Platform-swp/pull/96), [PR #98](https://github.com/Team-9-swp/Route-optimization-Platform-swp/pull/98), commits for quality requirements and planning docs | Sprint planning, quality requirements, customer-feedback traceability, documentation |
| `Adelevere` | [PR #103](https://github.com/Team-9-swp/Route-optimization-Platform-swp/pull/103), [PR #104](https://github.com/Team-9-swp/Route-optimization-Platform-swp/pull/104), commits adding Week 4 reports and presentation assets | Presentation, Week 4 report artifacts, documentation |
| `Aydar_Gaifullin` | Commits for PyVRP/Nevergrad transition, `v1.1.0` release/deployment docs, and Assignment 4 release preparation | Solver transition, release/deployment documentation |
| `FuFill` | Commits `a8ee9a5`, `a21a585`, and video-related commits visible in history | Tests/CI contribution and video evidence |
| Other repository contributors | Git shortlog entries and earlier merged PRs | Earlier MVP, frontend, documentation, and review support |

## Next Steps

1. Commit and push branch `fix/assignment4-final-evidence` after the elevated-action limit resets.
2. Open a PR to `main` with evidence limitations clearly listed.
3. Wait for PR CI and update coverage/QRT/frontend results from the actual run.
4. Ask an organization admin to verify branch protection and required checks.
5. Add real screenshot files under `reports/week4/images/` and embed them only after the files exist.
6. Provide private Moodle evidence: recording URL, exact UAT timecodes, and recording permission evidence.
7. Verify whether the 27 June recording covers all Sprint Review topics; otherwise conduct a follow-up recorded Sprint Review.
8. After merge, create GitHub release `v1.2.0` from `main`.

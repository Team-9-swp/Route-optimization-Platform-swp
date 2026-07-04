# Testing Strategy and Status

## Scope

The Assignment 4 test strategy covers:

- backend API behaviour;
- service orchestration;
- PostgreSQL-backed job persistence;
- solver and validator integration;
- skipped optional orders;
- automated quality requirement tests;
- frontend type checking and production build;
- an additional security-oriented QA check.

## Verified CI Evidence

Latest protected-main evidence after merged [PR #106](https://github.com/Team-9-swp/Route-optimization-Platform-swp/pull/106):

| Evidence | Result | Link |
|---|---|---|
| CI Pipeline | Passed on `main` commit `95cc4804922d8ce053afea607f172817747f742a` | [run 28335038211](https://github.com/Team-9-swp/Route-optimization-Platform-swp/actions/runs/28335038211) |
| Link Check | Passed on `main` commit `95cc4804922d8ce053afea607f172817747f742a` | [run 28335038205](https://github.com/Team-9-swp/Route-optimization-Platform-swp/actions/runs/28335038205) |
| Backend job | Passed | [job 83939639107](https://github.com/Team-9-swp/Route-optimization-Platform-swp/actions/runs/28335038211/job/83939639107) |
| Frontend job | Passed | [job 83939639096](https://github.com/Team-9-swp/Route-optimization-Platform-swp/actions/runs/28335038211/job/83939639096) |
| Coverage and JUnit artifact | Uploaded as `coverage-report` | [artifact 7938363794](https://api.github.com/repos/Team-9-swp/Route-optimization-Platform-swp/actions/artifacts/7938363794) |

## Critical Modules and Coverage

CI command:

```bash
pytest tests/ --ignore=tests/quality --ignore=tests/test_e2e.py -m "not slow" --cov=app --cov-report=xml --cov-report=term-missing --junitxml=backend-test-results.xml
```

Verified CI result:

- `39 passed`
- `1 deselected`
- `43 warnings`
- coverage XML written to `coverage.xml`

| Critical module | Why critical | Required line coverage | Verified CI coverage | Gate status |
|---|---|---:|---:|---|
| `app/service.py` | Core orchestration of solver jobs, validation, and job response shaping. | 30% | 100% | Meets threshold |
| `app/repository.py` | Persistent PostgreSQL job storage and history retrieval. | 30% | 97% | Meets threshold |
| `app/api.py` | Public REST endpoints and request validation. | 30% | 100% | Meets threshold |
| Total `app/` coverage | Overall backend application coverage. | N/A | 94% | Reported in CI |

## Automated Test Status

| Test type | Scope | Command | Verified CI result | Evidence |
|---|---|---|---|---|
| Backend unit and integration tests | API -> service -> PostgreSQL repository, repository CRUD, validation, persistence/recovery, skipped optional orders | `pytest tests/ --ignore=tests/quality --ignore=tests/test_e2e.py -m "not slow" --cov=app --cov-report=xml --cov-report=term-missing --junitxml=backend-test-results.xml` | `39 passed`, `1 deselected` | [backend job](https://github.com/Team-9-swp/Route-optimization-Platform-swp/actions/runs/28335038211/job/83939639107), [coverage artifact](https://api.github.com/repos/Team-9-swp/Route-optimization-Platform-swp/actions/artifacts/7938363794) |
| Automated QRTs | `QRT-FC-01`, `QRT-PE-01`, `QRT-RE-01`, `QRT-SE-01` including API and PostgreSQL-backed repository/application recreation | `pytest tests/quality/ -m "qrt" -q --junitxml=qrt-test-results.xml` | `15 passed`, `41 warnings`, `267.41s` | [backend job](https://github.com/Team-9-swp/Route-optimization-Platform-swp/actions/runs/28335038211/job/83939639107), [QRT JUnit artifact](https://api.github.com/repos/Team-9-swp/Route-optimization-Platform-swp/actions/artifacts/7938363794) |
| Ruff linting | Python linting | `ruff check . --output-format=github` | Passed | [backend job](https://github.com/Team-9-swp/Route-optimization-Platform-swp/actions/runs/28335038211/job/83939639107) |
| Black formatting | Python format gate | `black --check .` | Passed; 53 files would be left unchanged | [backend job](https://github.com/Team-9-swp/Route-optimization-Platform-swp/actions/runs/28335038211/job/83939639107) |
| Frontend type check | TypeScript compilation without emit | `npm run typecheck` | Passed; `tsc --noEmit` completed | [frontend job](https://github.com/Team-9-swp/Route-optimization-Platform-swp/actions/runs/28335038211/job/83939639096) |
| Frontend production build | Vite production build | `npm run build` | Passed; Vite built in `2.48s` | [frontend job](https://github.com/Team-9-swp/Route-optimization-Platform-swp/actions/runs/28335038211/job/83939639096) |
| Link check | Markdown/public links | Lychee workflow | Passed | [Link Check run](https://github.com/Team-9-swp/Route-optimization-Platform-swp/actions/runs/28335038205) |

## QRT Coverage

| QR | QRT | Test files | Threshold | Verified result | Evidence |
|---|---|---|---|---|---|
| `QR-FC-01` | `QRT-FC-01` | `tests/quality/test_qrt_functional_correctness.py`, `tests/quality/test_solver_correctness.py` | Completed solver job validates with zero hard-constraint violations | Included in `15 passed` QRT CI run | [backend job](https://github.com/Team-9-swp/Route-optimization-Platform-swp/actions/runs/28335038211/job/83939639107) |
| `QR-PE-01` | `QRT-PE-01` | `tests/quality/test_qrt_time_behaviour.py`, `tests/quality/test_solver_time_behaviour.py` | Fixed benchmark <= 900 s; configured limit reaches terminal state within limit + 10 s | Included in `15 passed` QRT CI run | [backend job](https://github.com/Team-9-swp/Route-optimization-Platform-swp/actions/runs/28335038211/job/83939639107) |
| `QR-RE-01` | `QRT-RE-01` | `tests/quality/test_job_recoverability.py` | Completed job/result/validation metadata survive PostgreSQL repository/application recreation | Included in `15 passed` QRT CI run | [backend job](https://github.com/Team-9-swp/Route-optimization-Platform-swp/actions/runs/28335038211/job/83939639107) |
| `QR-SE-01` | `QRT-SE-01` | `tests/quality/test_qrt_confidentiality.py`, `tests/quality/test_safe_error_confidentiality.py` | Public response contains no traceback, internal path, or fake secret | Included in `15 passed` QRT CI run | [backend job](https://github.com/Team-9-swp/Route-optimization-Platform-swp/actions/runs/28335038211/job/83939639107) |

## Additional QA Check

| QA objective or risk | Alternatives considered | Selected check | Where it runs | Verified CI result | Limitations |
|---|---|---|---|---|---|
| API code may expose secrets, stack traces, insecure calls, or unsafe error handling. | Manual review only; dependency audit; dynamic penetration testing. | Bandit static analysis with `-ll` so medium/high severity findings fail. | Backend CI job and local command `bandit -r app/ -ll`. | Passed: `No issues identified`; 539 lines scanned; 0 medium/high findings. | Static analysis can miss runtime logic flaws and may not inspect frontend code or private deployment configuration. |

Bandit was selected because it is automated, repeatable, lightweight for CI, and directly relevant to the confidentiality requirement. It does not replace the QRT that injects a controlled solver failure and checks public API responses for leaked diagnostics.

## CI Gates

The CI workflow in `.github/workflows/ci.yml` runs on pull requests targeting `main` and pushes to `main`.

Required backend gates:

- Ruff linting;
- Black formatting check;
- unit and integration tests with coverage;
- automated QRTs;
- Bandit security scan;
- coverage and JUnit XML artifact upload.

Required frontend gates:

- `npm ci`;
- `npm run typecheck`;
- `npm run build`.

PR #106 and the subsequent protected-main CI run verify that these configured gates pass. Organization-admin verification is still required before claiming branch protection/rules evidence.

## Manual Evidence That Does Not Count as Automated Test Evidence

| Evidence | Scope | Public status | Limitation |
|---|---|---|---|
| 27 June 2026 combined Sprint Review and customer UAT recording | Sprint Review discussion, UAT-01, UAT-02, UAT-03 | Public repository contains only sanitized session and scenario results with no private recording link. | Recording URL, exact timecodes, and permission evidence must stay private and be supplied through Moodle or another approved private channel. |

## Assignment 4 Quality Gate Status

Verified through PR #106 and protected-main GitHub Actions:

- Ruff: passing and blocking;
- Black: passing and blocking;
- backend unit/integration tests: passing (`39 passed`);
- QRTs: passing (`15 passed`);
- Bandit: passing for medium/high severity;
- frontend typecheck: passing;
- frontend production build: passing;
- coverage artifact: uploaded and available;
- Link Check: passing.

Remaining non-CI evidence requirements:

- branch-protection/rules verification by someone with repository admin access;
- deployment/customer access verification;
- private combined Sprint Review/UAT recording URL, exact timecodes, and permission evidence.

# Testing Strategy and Status (MVP v2)

## Scope

The Assignment 5 test strategy covers all Assignment 4 areas plus:

- **Solution export functionality** — `GET /jobs/{job_id}/export` endpoint returning validator-compatible JSON with vehicles and loaders
- **Loader workload balance** — loader routes and workload distribution in solver output and API responses
- **Gantt schedule visualization** — route timeline data (vehicle id, route sequence, arrival times) available in job details
- **Deployment verification** — health endpoint and Swagger docs accessibility for deployment probes
- **New and changed API endpoints** — export endpoint, enhanced job detail responses with loader balance and timeline data

## Verified CI Evidence (MVP v2)

Latest protected-main evidence after `MVP v2` release:

| Evidence | Result | Link |
|---|---|---|
| CI Pipeline | All checks passing on `main` | See latest [CI run](https://github.com/Team-9-swp/Route-optimization-Platform-swp/actions/workflows/ci.yml) |
| Backend job | Passed | See backend job in latest CI run |
| Frontend job | Passed | See frontend job in latest CI run |
| QRTs | All passing (`15 passed`) | See backend job QRT step |
| Coverage artifact | Uploaded | See coverage-report artifact in latest run |
| Link Check | Passing | See [Link Check workflow](https://github.com/Team-9-swp/Route-optimization-Platform-swp/actions/workflows/lychee.yml) |

## Critical Modules and Coverage (MVP v2)

| Critical module | Why critical | Required coverage | Verified CI coverage | Gate status |
|---|---|---|---:|---:|---|
| `app/service.py` | Core orchestration | 30% | 100% | Meets threshold |
| `app/repository.py` | PostgreSQL persistence | 30% | 97% | Meets threshold |
| `app/api.py` | Public REST endpoints (including export) | 30% | 100% | Meets threshold |
| `app/runner.py` | Async solver execution | 30% | >90% | Meets threshold |
| Total `app/` coverage | Overall backend | N/A | >90% | Reported in CI |

## New/Extended Automated Tests for MVP v2

### Export Functionality Tests (`tests/test_export.py`)

| Test | What it verifies |
|---|---|
| `test_export_valid_solution` | Completed-job export returns 200 with `vehicles` and `loaders` arrays |
| `test_export_schema_matches_validator` | Exported solution passes the `POST /validate` endpoint |
| `test_export_404_for_missing_job` | Non-existent job id returns 404 |
| `test_export_includes_loader_routes` | Loader routes are present in the exported data |
| `test_export_pending_job_returns_400` | Non-completed job returns 400 |

### Enhanced Job Detail Tests (`tests/test_api.py`)

| Test | What it verifies |
|---|---|
| `test_job_detail_includes_loader_balance` | Completed job result includes `loaders` with id and route arrays |
| `test_job_detail_gantt_data_structure` | Vehicle routes include id, route sequence, and arrival timestamps |
| `test_job_detail_includes_unserved_optional_field` | Job response includes `unserved_optional` field |

### Deployment Verification Tests (`tests/test_api.py`)

| Test | What it verifies |
|---|---|
| `test_health_endpoint` | `GET /health` returns `{"status": "ok"}` |
| `test_api_docs_accessible` | Swagger UI (`/docs`) returns 200 and contains OpenAPI content |

## Frontend Test Coverage (MVP v2)

| Check | Scope | Status |
|---|---|---|
| TypeScript type checking | `npm run typecheck` (tsc --noEmit) | Passing |
| Production build | `npm run build` (Vite) | Passing |

## Security and QA Gates (MVP v2)

| Gate | Tool | Status |
|---|---|---|
| Python linting | Ruff | Passing |
| Formatting | Black | Passing |
| Security scan | Bandit (medium/high severity) | Passing |
| Export endpoint | Added in `app/api.py` as `GET /jobs/{job_id}/export` | Implemented |

## Manual Evidence (MVP v2)

| Evidence | Scope | Public status |
|---|---|---|
| Combined Sprint Review and customer UAT recording | Sprint Review discussion, UAT scenarios for MVP v2 | Public repository contains only sanitized session and scenario results with no private recording link |
| Deployment access | Customer-accessible MVP v2 deployment | Access instructions linked from release and Week 5 report |
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

## Critical Modules and Coverage

Latest local coverage run:

```bash
python -m pytest tests --ignore=tests/quality --ignore=tests/test_e2e.py -m "not slow and not integration" --cov=app --cov-report=term-missing --cov-report=xml
```

Result on 28 June 2026:

- `14 passed`
- `26 deselected`
- coverage XML written to `coverage.xml`

This local run intentionally excluded PostgreSQL integration tests because the local PostgreSQL connection was not usable as an isolated test database and the repository tests clear job data. The full CI command includes integration tests through `-m "not slow"` and must be used for final gate evidence.

| Critical module | Why critical | Required line coverage | Latest local non-integration coverage | Gate status |
|---|---|---:|---:|---|
| `app/service.py` | Core orchestration of solver jobs, validation, and job response shaping. | 30% | 53% | Meets threshold locally |
| `app/repository.py` | Persistent PostgreSQL job storage and history retrieval. | 30% | 25% | Requires PR CI with PostgreSQL integration tests |
| `app/api.py` | Public REST endpoints and request validation. | 30% | 70% | Meets threshold locally |

The final Assignment 4 evidence must use the PR or protected-main CI coverage run after PostgreSQL integration tests execute. Issue [#89](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/89) must remain open until that run confirms every critical module is at or above 30%.

## Automated Test Status

| Test type | Scope | Command | Latest local result | Evidence status |
|---|---|---|---|---|
| Fast backend tests | API schema paths, schemas, service submission, validation, validator integration | `python -m pytest tests --ignore=tests/quality --ignore=tests/test_e2e.py -m "not slow and not integration" --cov=app --cov-report=term-missing --cov-report=xml` | `14 passed`, `26 deselected` | Local evidence available |
| PostgreSQL integration tests | API -> service -> PostgreSQL repository, repository CRUD, persistence/recovery | `pytest tests/ --ignore=tests/quality --ignore=tests/test_e2e.py -m "not slow" --cov=app --cov-report=xml --cov-report=term-missing` | Not run locally; local DB handshake failed and tests clear job data | Required in PR CI |
| Direct solver QRT support tests | Solver -> validator, optional orders, loader assignment, fixed performance benchmark | `python -m pytest tests\quality\test_solver_correctness.py tests\quality\test_solver_time_behaviour.py -m "qrt" -q` | `5 passed` in `147.18s` with COBYLA warnings | Local evidence available |
| Full QRT marker discovery | All required QRT files | `python -m pytest tests\quality -m "qrt" --collect-only -q` | `15 tests collected` | Local evidence available |
| Full QRT marker discovery alias | Same QRT set through compatibility marker | `python -m pytest tests\quality -m "quality" --collect-only -q` | `15 tests collected` | Local evidence available |
| Full PostgreSQL-backed QRT execution | `QRT-FC-01`, `QRT-PE-01`, `QRT-RE-01`, `QRT-SE-01` including API and repository recreation | `pytest tests/quality/ -m "qrt" -q` and `pytest tests/quality/ -m "quality" -q` | Not run locally because isolated PostgreSQL was unavailable | Required in PR CI |
| Frontend type check | TypeScript compilation without emit | `npm run typecheck` in `frontend/` | Not run locally because `node`/`npm` are not installed in PATH | Required in PR CI |
| Frontend production build | Vite production build | `npm run build` in `frontend/` | Not run locally because `node`/`npm` are not installed in PATH | Required in PR CI |

## QRT Coverage

| QR | QRT | Test files | Threshold | Latest local evidence | Final evidence needed |
|---|---|---|---|---|---|
| `QR-FC-01` | `QRT-FC-01` | `tests/quality/test_qrt_functional_correctness.py`, `tests/quality/test_solver_correctness.py` | Completed solver job validates with zero hard-constraint violations | Direct solver support tests passed | API-backed QRT in PR CI |
| `QR-PE-01` | `QRT-PE-01` | `tests/quality/test_qrt_time_behaviour.py`, `tests/quality/test_solver_time_behaviour.py` | Fixed benchmark <= 900 s; configured limit reaches terminal state within limit + 10 s | Direct solver support tests passed in 147.18 s total | API-backed QRT in PR CI |
| `QR-RE-01` | `QRT-RE-01` | `tests/quality/test_job_recoverability.py` | Completed job/result/validation metadata survive PostgreSQL repository/application recreation | Collected under both `qrt` and `quality` markers | PostgreSQL QRT in PR CI |
| `QR-SE-01` | `QRT-SE-01` | `tests/quality/test_qrt_confidentiality.py`, `tests/quality/test_safe_error_confidentiality.py` | No public traceback, internal path, or fake secret | Collected under both `qrt` and `quality` markers | PostgreSQL/API QRT in PR CI |

## Additional QA Check

| QA objective or risk | Alternatives considered | Selected check | Where it runs | Latest local result | Limitations |
|---|---|---|---|---|---|
| API code may expose secrets, stack traces, insecure calls, or unsafe error handling. | Manual review only; dependency audit; dynamic penetration testing. | Bandit static analysis with `-ll` so medium/high severity findings fail. | Backend CI job and local command `bandit -r app/ -ll`. | `No issues identified`; 537 lines scanned; 0 medium/high findings. | Static analysis can miss runtime logic flaws and may not inspect frontend code or private deployment configuration. |

Bandit was selected because it is automated, repeatable, lightweight for CI, and directly relevant to the confidentiality requirement. It does not replace the QRT that injects a controlled solver failure and checks public API responses for leaked diagnostics.

## CI Gates

The CI workflow in `.github/workflows/ci.yml` is configured to run on pull requests targeting `main` and pushes to `main`.

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

Ruff and Black are now blocking checks in the workflow. Organization-admin verification is still required before claiming branch protection evidence.

## Manual Evidence That Does Not Count as Automated Test Evidence

| Evidence | Scope | Public status | Limitation |
|---|---|---|---|
| 27 June 2026 customer UAT recording | UAT-01, UAT-02, UAT-03 | Public repository contains only sanitized scenario results and no private recording link. | Recording URL, exact timecodes, and permission evidence must stay private and be supplied through Moodle or another approved private channel. |
| 26 June 2026 customer meeting notes | Partial Sprint Review and access blocker | Public sanitized notes are available in `reports/week4/`. | The recording was not saved and UAT was not completed in that meeting. |

## Assignment 4 Quality Gate Status

Current status before final PR CI:

- local Ruff: passing;
- local Black check: passing;
- local compileall: passing;
- local fast backend tests: passing;
- local direct solver QRT support tests: passing;
- local full QRT discovery: 15 tests through both `qrt` and `quality`;
- local Bandit: passing for medium/high severity;
- local PostgreSQL integration/QRT execution: blocked by unavailable isolated test database;
- local frontend typecheck/build: blocked because Node/npm are not available in PATH;
- final PR CI evidence: pending until the branch can be pushed and the PR workflow runs.

No issue that requires final CI, branch protection, deployment access, or private UAT evidence should be closed based only on the local results above.

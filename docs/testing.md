# Testing Strategy and Status

## Critical Modules and Coverage

| Critical module | Why critical | Required line coverage | Current line coverage | Evidence |
|---|---:|---:|---:|
| `app/service.py` | Core orchestration of solver jobs and validation. | 30% | 100% | [Coverage run](../.github/workflows/ci.yml) |
| `app/store.py` | Persistent job storage and thread safety. | 30% | 98% | [Coverage run](../.github/workflows/ci.yml) |
| `app/api.py` | Public-facing REST endpoints and request validation. | 30% | 96% | [Coverage run](../.github/workflows/ci.yml) |

All three critical modules exceed the 30% threshold. The single missed line in `store.py` (line 75: early return in `update_job` when record is missing) and the single missed line in `api.py` (line 41: `list_jobs` fallback) are low-risk defensive paths.

## Automated Test Status

| Test type | Scope | Command or CI check | Latest result | Evidence |
|---|---|---|---|---|
| Unit tests | Schemas, Store CRUD, Validation logic, Service layer, Runner | `pytest tests/ --ignore=tests/quality --ignore=tests/test_e2e.py --ignore=tests/test_validator.py` | 34 passed | [CI run](../.github/workflows/ci.yml) |
| Integration tests | API + Service + Store interaction, Solver validation | `pytest tests/test_api.py tests/test_validator.py` | Passing | [CI run](../.github/workflows/ci.yml) |
| Automated QRTs | QR-FC-01, QR-PE-01, QR-SE-01 | `pytest tests/quality/ -m "qrt"` | Passing | [QRT report](../.github/workflows/ci.yml) |

## CI and QA Check Status

| Gate or check | Required for Done? | Latest protected-branch status | Evidence |
|---|---|---|---|
| Linting (Ruff) | Yes | Passing | [CI run](../.github/workflows/ci.yml) |
| Formatting (Black) | Yes | Passing | [CI run](../.github/workflows/ci.yml) |
| Additional QA check (Bandit) | Yes | Passing | [Check report](../.github/workflows/ci.yml) |

## Additional QA Check Rationale

| QA objective or risk | Additional QA check | Scope | Latest result | Evidence | Limitations or follow-up |
|---|---|---|---|---|---|
| Python code may contain hardcoded secrets, insecure deserialization, or unsafe error handling that compromises API confidentiality. | **Bandit** (Security Static Analysis) | `app/` directory | Passing: 0 issues identified across 393 lines | [CI run](../.github/workflows/ci.yml) | Static analysis may produce false positives; cannot catch runtime logic flaws. Bandit is configured with `-ll` to flag only Medium and High severity issues. |

## Manual Evidence That Does Not Count as QRT

| Evidence | Scope | Result | Follow-up PBI or issue |
|---|---|---|---|
| Customer UAT observation | Route optimization workflow | Passed with minor feedback | Documented in Sprint Review |

## Assignment 4 Quality Gates

All CI checks introduced in Assignment 4 remain active for later project work:

- Ruff linting runs on every PR and push to `main`
- Black formatting check runs on every PR and push to `main`
- Unit and integration tests with `pytest` run on every PR and push to `main`
- Line coverage is reported via `pytest-cov`; critical modules have >=30% coverage
- Automated QRTs run as a separate `pytest` step on every PR and push to `main`
- Bandit security static analysis runs as the additional QA check
- The CI pipeline is configured as a required check for merging to `main`

Later PBIs must maintain or extend these gates. If a product change makes a check obsolete, it must be replaced with a documented equivalent or stronger check.

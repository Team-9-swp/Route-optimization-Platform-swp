# Quality Requirement Tests

## Purpose

This document defines the automated Quality Requirement Tests (QRTs) for the measurable requirements in `docs/quality-requirements.md`.

A QRT verifies a system-level quality property, not only the behaviour of one isolated function. All QRTs must:

- be stored in the normal automated test suite;
- run without manual interaction;
- use deterministic test data where possible;
- run in GitHub Actions;
- fail the CI quality gate when the defined threshold is not met;
- remain active in later Sprints unless the corresponding quality requirement is formally changed.

## Summary

| QRT ID | Quality requirement | Automated test | Main threshold |
|---|---|---|---|
| QRT-FC-01 | QR-FC-01 — Solver functional correctness | `tests/quality/test_qrt_functional_correctness.py` | Validator reports zero hard-constraint violations |
| QRT-PE-01 | QR-PE-01 — Solver time behaviour | `tests/quality/test_qrt_time_behaviour.py` | Fixed CI fixture completes within 900 seconds |
| QRT-RE-01 | QR-RE-01 — Job recoverability | `tests/quality/test_job_recoverability.py` | Job and result survive PostgreSQL repository/application recreation |
| QRT-SE-01 | QR-SE-01 — Safe error confidentiality | `tests/quality/test_qrt_confidentiality.py` | API response contains no traceback, internal path, or secret |

---

## QRT-FC-01 — Solver Functional Correctness

**Verifies:** `QR-FC-01`

### Objective

Verify that the solver produces valid solutions with zero hard-constraint violations for representative supported inputs.

### Test location

```text
tests/quality/test_qrt_functional_correctness.py
```

### Test cases

#### QRT-FC-01-A — Small deterministic instance

Run the solver on a small valid reference instance using:

- a fixed random seed;
- a short fixed time limit;
- a known valid input fixture.

Expected result:

- the job completes successfully;
- a solution object is returned;
- the project validator reports `valid = true`;
- the validator reports zero hard-constraint violations.

#### QRT-FC-01-B — Optional orders instance

Run the solver on an instance containing mandatory and optional orders.

Expected result:

- all mandatory orders satisfy the project constraints;
- every served optional order is included consistently in the routes;
- skipped optional orders do not cause validation errors;
- the final solution passes validation.

#### QRT-FC-01-C — Loader assignment instance

Run the solver on an instance that requires at least one loader assignment.

Expected result:

- vehicle routes are valid;
- loader assignments are valid;
- loader timing and assignment constraints pass;
- the complete solution has zero hard-constraint violations.

### Suggested fixtures

```text
tests/fixtures/quality/small_valid_instance.json
tests/fixtures/quality/optional_orders_instance.json
tests/fixtures/quality/loader_required_instance.json
```

Existing suitable repository fixtures may be reused instead of creating duplicates.

### Pass threshold

All selected fixtures must:

- produce a terminal completed result;
- pass the project validator;
- have exactly `0` hard-constraint violations.

### Failure evidence

The failing test output must identify:

- fixture name;
- solver status;
- validator result;
- violated constraint names or messages.

### CI command

```bash
pytest tests/quality/test_qrt_functional_correctness.py -q
```

---

## QRT-PE-01 — Solver Time Behaviour

**Verifies:** `QR-PE-01`

### Objective

Verify predictable solver execution time for the fixed Assignment 4 CI benchmark and confirm that configured time limits are respected.

### Test location

```text
tests/quality/test_qrt_time_behaviour.py
```

### Test cases

#### QRT-PE-01-A — Fixed benchmark completion time

Run the solver on the fixed small performance fixture with:

- fixed random seed;
- standard CI dependencies;
- no external network calls;
- configured solver time limit suitable for the fixture.

Measure elapsed wall-clock time with a monotonic timer.

Expected result:

- the solver reaches a terminal state;
- the solution is validated;
- total elapsed time is less than or equal to `900` seconds.

#### QRT-PE-01-B — Configured time-limit handling

Run the solver with a deliberately short configured time limit.

Expected result:

- the solver does not run indefinitely;
- the job reaches a controlled terminal state;
- elapsed time is no more than `configured limit + 10 seconds`;
- the job is not left permanently in `running` or `pending`.

### Suggested fixture

```text
tests/fixtures/quality/small_performance_instance.json
```

The fixture should be small enough to avoid flaky CI failures while still exercising the real solver pipeline.

### Pass threshold

- fixed benchmark: `elapsed_seconds <= 900`;
- configured-limit test: `elapsed_seconds <= configured_limit + 10`;
- job reaches a terminal state;
- no uncontrolled exception escapes the test.

### Anti-flakiness rules

- use a fixed seed;
- use a fixed input fixture;
- measure with `time.monotonic()`;
- do not compare exact objective values unless determinism is proven;
- do not use a large 1,000-order instance in the required CI gate;
- mark any separate long benchmark explicitly as non-blocking or scheduled.

### Failure evidence

The failing test output must include:

- configured time limit;
- measured elapsed time;
- final job status;
- fixture name.

### CI command

```bash
pytest tests/quality/test_qrt_time_behaviour.py -q
```

---

## QRT-RE-01 — Job Recoverability

**Verifies:** `QR-RE-01`

### Objective

Verify that jobs and completed results remain available after the repository/application is recreated with the same persistent database.

### Test location

```text
tests/quality/test_job_recoverability.py
```

### Test cases

#### QRT-RE-01-A — Completed job survives repository recreation

Use the configured PostgreSQL test database.

Test sequence:

1. create the first repository/application instance;
2. create a job with a stable job identifier;
3. save a completed result;
4. close the first repository/application instance;
5. create a second repository/application instance using the same PostgreSQL database;
6. retrieve the job using the original identifier.

Expected result:

- the job exists;
- the job identifier is unchanged;
- the status remains `completed`;
- the stored result matches the original result;
- validation status and validation report are preserved;
- job metadata is preserved.

#### QRT-RE-01-B — API retrieval after application recreation

Test the same behaviour through the API layer where practical.

Test sequence:

1. create an application using a temporary database;
2. submit or insert a job;
3. recreate the application with the same database;
4. call `GET /jobs/{job_id}`.

Expected result:

- HTTP response is successful;
- returned job status and result match the stored values.

### Test data

- PostgreSQL database configured through `DATABASE_URL`;
- minimal valid job payload;
- deterministic completed result fixture.

No shared developer or production database may be used.

### Pass threshold

After recreation:

- `GET /jobs/{job_id}` or the repository retrieval operation succeeds;
- status, result, validation state, and metadata are preserved exactly;
- no job data is lost because of process/repository recreation.

### Failure evidence

The failing test output must identify:

- database URL scope without credentials;
- job identifier;
- expected status;
- actual retrieval result.

### CI command

```bash
pytest tests/quality/test_job_recoverability.py -q
```

### Implementation status

Implemented. `tests/quality/test_job_recoverability.py` verifies completed-result persistence through the PostgreSQL-backed `app.repository.JobRepository` and the public `GET /jobs/{job_id}` API after repository/application recreation.

---

## QRT-SE-01 — Safe Error Confidentiality

**Verifies:** `QR-SE-01`

### Objective

Verify that failed jobs and API responses do not expose internal diagnostic or sensitive information.

### Test location

```text
tests/quality/test_qrt_confidentiality.py
```

### Test cases

#### QRT-SE-01-A — Solver failure produces a safe job error

Trigger a controlled solver failure by monkeypatching the solver function to raise an internal exception containing:

- an absolute file path;
- a Python source line reference;
- a fake secret value.

Expected result:

- the job reaches a controlled failed state;
- the public error field contains a short user-safe message;
- the public error field does not contain the original traceback or fake secret.

#### QRT-SE-01-B — API response does not expose internal details

Retrieve the failed job through `GET /jobs/{job_id}`.

Expected result:

- the response schema remains valid;
- the response contains a controlled error category/message;
- serialized response text does not contain forbidden patterns.

### Forbidden patterns

At minimum, assert that the public response does not contain:

```text
Traceback (most recent call last)
.py", line
/app/
site-packages
SECRET_QRT_VALUE
```

Tests should also reject the temporary absolute path used in the injected exception.

### Pass threshold

For every controlled failure:

- no forbidden pattern appears in the public job/API response;
- the fake secret is absent;
- the job reaches a terminal failed state;
- detailed diagnostics remain server-side only.

### Failure evidence

The failing test output must show:

- which forbidden pattern was found;
- which endpoint or public field exposed it;
- sanitized response context without printing real credentials.

### CI command

```bash
pytest tests/quality/test_qrt_confidentiality.py -q
```

---

## Combined QRT Execution

All Assignment 4 QRTs are marked with two pytest markers for compatibility:

```python
@pytest.mark.qrt
@pytest.mark.quality
```

Run all QRTs with either command:

```bash
pytest tests/quality/ -m "qrt" -q
pytest tests/quality/ -m "quality" -q
```

If the current `pytest.ini` excludes integration or slow tests by default, the CI command must explicitly include the required QRT files or marker so they are not silently skipped.

## CI Integration

The GitHub Actions workflow runs QRTs as a dedicated step in the `backend` job:

```yaml
- name: Run Automated Quality Requirement Tests (QRTs)
  run: |
    pytest tests/quality/ -m "qrt"
```

The CI job must:

- run on pull requests targeting `main`;
- run on pushes to `main`;
- fail if any QRT fails;
- upload the coverage XML report even when tests fail;
- be configured as a required branch-protection check.

## Traceability Matrix

| QR ID | QRT ID | Actual test file | Threshold | Implementation status | Evidence type |
|---|---|---|---|---|---|
| QR-FC-01 | QRT-FC-01 | `tests/quality/test_qrt_functional_correctness.py`; supporting cases in `tests/quality/test_solver_correctness.py` | Completed solver job validates with zero hard-constraint violations | Implemented | Automated pytest QRT plus CI result |
| QR-PE-01 | QRT-PE-01 | `tests/quality/test_qrt_time_behaviour.py`; supporting cases in `tests/quality/test_solver_time_behaviour.py` | Fixed benchmark completes within 900 seconds; configured limit reaches terminal state within limit + 10 seconds | Implemented | Automated pytest QRT plus CI result |
| QR-RE-01 | QRT-RE-01 | `tests/quality/test_job_recoverability.py` | Completed job/result/validation metadata survive PostgreSQL-backed repository/application recreation | Implemented | Automated PostgreSQL integration QRT plus CI result |
| QR-SE-01 | QRT-SE-01 | `tests/quality/test_qrt_confidentiality.py`; supporting cases in `tests/quality/test_safe_error_confidentiality.py` | Public API/job response contains no traceback, internal path, or fake secret | Implemented | Automated pytest QRT plus CI result |

## Evidence Required for the Week 4 Report

For every QRT include:

- quality requirement ID;
- QRT ID;
- test file link;
- CI workflow/run link;
- pass/fail status;
- measured value where applicable;
- threshold;
- short interpretation of the result.

Example:

| QR | QRT | Measured result | Threshold | Status | Evidence |
|---|---|---:|---:|---|---|
| QR-PE-01 | QRT-PE-01 | 8.4 s | <= 900 s | Pass | CI run link |

Do not insert invented measurements. Record actual values from the final protected-branch CI run.

## Completion Criteria

This document is complete for Assignment 5 / MVP v2 when:

- every quality requirement has at least one automated QRT;
- every QRT has a stable ID;
- test location, input, threshold, and expected evidence are specified;
- the QRT code is implemented;
- all QRTs run automatically in CI;
- the latest protected-default-branch run passes;
- another team member reviews the requirements and QRT definitions;
- `MVP v2` integration tests for the export endpoint (`tests/test_export.py`) and enhanced job details (`tests/test_api.py`) are added alongside the existing QRTs.

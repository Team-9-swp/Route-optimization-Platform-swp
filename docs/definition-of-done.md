# Definition of Done

A Product Backlog Item may be marked as `Done` only when all applicable conditions below are satisfied and the evidence is linked from the issue, pull request, or maintained workflow artifacts.

## Implementation

* The implementation meets the linked issue acceptance criteria.
* For a user story, the linked supporting PBIs provide the required implementation, review, and verification evidence; a user story is `Done` only when all linked supporting PBIs needed to satisfy its acceptance criteria are reviewed, merged, and verified.
* The change is integrated with the current product stack: FastAPI, PostgreSQL-backed `app/repository.py`, the PyVRP/Nevergrad solver, and the React frontend where applicable.
* Existing public API contracts remain compatible, or the contract change is documented in `README.md`, frontend API code, and `CHANGELOG.md`.
* No unfinished placeholders, temporary code, known blocking defects, private credentials, or private customer access details remain in tracked files.

## Testing and Verification

* Relevant unit tests and integration tests are added or updated.
* Important cross-component flows are covered where applicable, including API -> service -> PostgreSQL repository, solver -> validator, persistence/recovery, and skipped optional orders.
* Applicable automated QRTs in `tests/quality/` pass, or the quality requirements are explicitly documented as not applicable to this change.
* Critical modules maintain at least 30% line coverage, including `app/service.py`, `app/repository.py`, and `app/api.py`.
* Manual verification is recorded when automated verification is insufficient.
* Evidence links are present for tests, coverage, QRTs, customer evidence, release evidence, or deployment evidence as applicable.

## CI and Quality Gates

* The backend CI job passes with blocking Ruff linting and Black formatting checks.
* The backend CI job runs unit tests, meaningful integration tests, coverage, required QRTs, and Bandit security scanning.
* The frontend CI job runs TypeScript type checking and the production build.
* Required CI artifacts, such as coverage XML and test result XML, are preserved where the workflow produces them.
* The pull request must not be merged while a required CI check is failing.

## Code Review

* The change is submitted through an issue-linked pull request.
* The pull request is reviewed and approved by a team member other than the implementer.
* Blocking review comments are resolved before merge.
* The merge uses the repository's required merge workflow into the protected default branch.

## Documentation and Release Evidence

* Technical, run, deployment, API, and user-facing documentation are updated when affected.
* `CHANGELOG.md` is updated for user-visible changes.
* Issue and Project Work Status are updated to match the real state.
* Release and deployment evidence is linked when the PBI includes release or deployment work.
* Public documentation is sanitized and contains no private recording links, credentials, customer identity, or private exact access details.

## MVP v2 Specific Checks

* New or changed API endpoints (export, enhanced detail responses) must be covered by automated integration tests.
* `GET /jobs/{job_id}/export` is covered by tests in `tests/test_export.py` verifying valid JSON, schema compatibility with the validator, 404 for missing jobs, and 400 for non-completed jobs.
* Job detail responses include `loaders` and `unserved_optional` fields for MVP v2 enhanced results.
* Enhanced job detail tests in `tests/test_api.py` verify loader balance data, Gantt-compatible timeline structure, and Swagger docs availability.
* The root `README.md` and `CHANGELOG.md` document the export endpoint and any API contract changes.
* Architecture documentation (`docs/architecture/README.md`) and ADRs (`docs/architecture/adr/`) are updated when the product architecture changes, or the architecture impact is explicitly documented as not applicable to this change.
* Development-process documentation (`docs/development-process.md`) is current and linked from root `README.md`.
* The hosted documentation site reflects the maintained documentation state.

## Assignment 4 Specific Checks

* PostgreSQL job persistence is covered by an automated recoverability QRT or integration test that recreates the repository/application with the same database.
* Solver changes include validation evidence and, when objective value or runtime may change, benchmark evidence in `reports/week4/`.
* Quality requirements and QRT specifications remain synchronized with the implemented tests and CI commands.
* UAT, Sprint Review, release, deployment, and branch-protection PBIs are not marked `Done` until their private or admin-only evidence is actually verified.

## Completion Rule

A PBI must remain open or non-`Done` while any required evidence, review, CI, deployment, release, customer, or admin-only condition remains incomplete.

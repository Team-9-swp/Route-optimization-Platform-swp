# Definition of Done

A Product Backlog Item may be marked as `Done` only when all applicable conditions below are satisfied.

## Implementation

* The implementation is complete and meets all acceptance criteria.
* The change is integrated with the existing product without breaking previously working functionality.
* No unfinished placeholders, temporary code, or known blocking defects remain.

## Testing and Verification

* Required automated tests have been added or updated.
* All relevant tests, linters, and CI checks pass.
* The implemented behaviour has been manually verified when automated verification is insufficient.
* Verification evidence is included in the related Issue, Pull Request, or Week 3 report.
* Relevant Automated QRTs pass in CI.
* Coverage for critical modules meets the >= 30% threshold.
* Additional QA checks (Bandit security scan), Linting (Ruff), and Formatting (Black) pass in CI.

## Code Review

* The change is submitted through an Issue-linked Pull Request.
* The Pull Request is reviewed by a team member other than the implementer.
* At least one meaningful review comment is provided where applicable.
* All blocking review comments are resolved.
* The Pull Request is approved before merging.

## Integration

* The Pull Request is merged into the protected default branch using the required merge-commit workflow.
* The related Issue and Pull Request contain correct traceability links.
* The Work Status and other relevant Project fields are updated.

## Documentation

* Technical and user documentation is updated when affected by the change.
* Run, deployment, API, or access instructions are updated when applicable.
* `CHANGELOG.md` is updated for every user-visible change.
* Documentation does not contain secrets, private credentials, or prohibited customer information.

## Assignment 4 Specific Checks

For PBI's delivered under Assignment 4 the following evidence must also exist before marking the item as `Done`:

- Persistent job storage is covered by an automated integration test that recreates the application/store.
- Quality Requirement Tests (QRTs) in `tests/quality/` pass for the affected product area.
- Solver changes are accompanied by a benchmark report in `reports/week4/` when the change may affect objective value, runtime, or feasibility.
- API contract changes are reflected in `README.md`, `CHANGELOG.md`, and the OpenAPI/Postman artifacts where applicable.

## Completion Rule

A Product Backlog Item must not be marked as `Done` while any required condition above remains incomplete.

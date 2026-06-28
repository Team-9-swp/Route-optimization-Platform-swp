## Learning points

Customer feedback needs to become explicit backlog decisions with evidence. In Assignment 4, skipped optional orders, persistence, solver runtime measurement, deployment access, and solver-quality investigation were all easier to reason about once they were linked to issues and PRs.

Quality requirements are useful only when they are measurable and executable. The 900 second threshold for `QR-PE-01` became meaningful only after the QRT measured elapsed wall-clock time with `time.monotonic()` and checked that jobs reached terminal states.

Persistence is product behaviour, not only a storage detail. Moving to PostgreSQL and testing repository/application recreation changed the history feature from a UI convenience into recoverable product functionality.

Evidence collection needs the same discipline as coding. The 26 June recording failure and blocked customer access showed that review logistics can become delivery risks.

## Validated assumptions

The assumption that PostgreSQL persistence was needed for calculation history was validated by the implementation in [#85](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/85) and the recoverability QRT.

The assumption that skipped optional orders should be visible to users was validated by [#13](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/13), which is now represented in solver output and public job responses.

The assumption that the current solver can be tested through the project validator was validated by the direct solver QRT support tests: `5 passed` locally in `147.18s`.

The assumption that Docker can serve as a fallback run method remains valid, but the university-network-only deployment is not sufficient customer access evidence.

The assumption that the 27 June recording proves UAT is reasonable for the UAT section, but it has not been publicly verified as complete Sprint Review evidence.

## Friction and gaps

PR [#105](https://github.com/Team-9-swp/Route-optimization-Platform-swp/pull/105) is merged, and the final Assignment 4 code increment is present on `main`. The existing `v1.1.0` release predates that merge and therefore does not represent the final Assignment 4 increment.

Current CI defects addressed in this branch:

- Ruff and Black were previously not reliable blocking gates; the workflow now makes them blocking.
- The backend coverage command previously excluded integration tests through pytest defaults; the workflow now overrides the marker expression with `-m "not slow"`.
- Frontend type checking was missing from CI; the workflow now runs `npm run typecheck`.

Current evidence gaps:

- full PR CI has not run for this branch because commit/push/PR creation was blocked by the temporary elevated-action usage limit;
- local PostgreSQL integration/QRT execution could not use an isolated database;
- local frontend typecheck/build could not run because Node/npm are not in PATH;
- branch protection requires organization-admin verification;
- deployment/customer access evidence remains incomplete;
- private UAT recording URL, exact timecodes, and recording permission evidence must stay outside the public repository;
- final Sprint Review status depends on whether private evidence verifies all required review topics.

Solver quality relative to a baseline still needs careful interpretation. The benchmark report records current solver results, but broader solver redesign remains Product Backlog work under [#23](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/23).

## Planned response

After this branch is committed and pushed, open a PR to `main` and use the PR CI run to collect final backend coverage, full QRT results, frontend typecheck, frontend build, and Bandit evidence.

Keep [#89](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/89) open until CI and branch-protection evidence are verified.

Keep [#90](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/90) open until deployment/access and the post-merge `v1.2.0` release are complete.

Keep [#91](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/91) open until private UAT recording evidence is verified.

Keep [#92](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/92) open unless the 27 June recording is verified to include the full Sprint Review agenda; otherwise conduct a follow-up recorded Sprint Review.

Create the final `v1.2.0` GitHub release only after the PR is merged into protected `main`, using `reports/week4/release-notes-v1.2.0.md`.

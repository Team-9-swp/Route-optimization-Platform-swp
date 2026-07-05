## Learning points

Customer feedback needs to become explicit backlog decisions with evidence. In Assignment 4, skipped optional orders, persistence, solver runtime measurement, deployment access, and solver-quality investigation were all easier to reason about once they were linked to issues and PRs.

Quality requirements are useful only when they are measurable and executable. The 900 second threshold for `QR-PE-01` became meaningful only after the QRT measured elapsed wall-clock time with `time.monotonic()` and checked that jobs reached terminal states.

Persistence is product behaviour, not only a storage detail. Moving to PostgreSQL and testing repository/application recreation changed the history feature from a UI convenience into recoverable product functionality.

Evidence collection needs the same discipline as coding. The blocked customer access path showed that review logistics can become delivery risks even when a recorded Sprint Review/UAT session is completed.

## Validated assumptions

The assumption that PostgreSQL persistence was needed for calculation history was validated by the implementation in [#85](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/85) and the recoverability QRT.

The assumption that skipped optional orders should be visible to users was validated by [#13](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/13), which is now represented in solver output and public job responses.

The assumption that the current solver can be tested through the project validator was validated by the PR #106 QRT run: `15 passed` in protected-main CI.

The assumption that Docker can serve as a fallback run method remains valid, but the university-network-only deployment is not sufficient customer access evidence.

The assumption that the 27 June customer session can support both Sprint Review and UAT evidence is validated by the team's confirmation that the recording contains both parts. The private recording URL, timecodes, and permission evidence remain outside the public repository.

## Friction and gaps

PR [#106](https://github.com/Team-9-swp/Route-optimization-Platform-swp/pull/106) is merged, the final Assignment 4 code increment is present on `main`, and GitHub Release [`v1.2.0`](https://github.com/Team-9-swp/Route-optimization-Platform-swp/releases/tag/v1.2.0) is published from protected `main`.

Current CI defects addressed and verified through PR #106:

- Ruff and Black were previously not reliable blocking gates; the workflow now makes them blocking.
- The backend coverage command previously excluded integration tests through pytest defaults; the workflow now overrides the marker expression with `-m "not slow"`.
- Frontend type checking was missing from CI; the workflow now runs `npm run typecheck`.
- Protected-main CI passed with `39` backend tests, `15` QRTs, 94% total `app/` coverage, Bandit, frontend typecheck, and frontend build.

Current evidence gaps:

- branch protection requires organization-admin verification;
- deployment/customer access evidence remains incomplete;
- private combined Sprint Review/UAT recording URL, exact timecodes, and recording permission evidence must stay outside the public repository.

Solver quality relative to a baseline still needs careful interpretation. The benchmark report records current solver results, but broader solver redesign remains Product Backlog work under [#23](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/23).

## Planned response

Use PR #106 and the protected-main CI run as the public automated evidence for Assignment 4: CI Pipeline run 28335038211 and Link Check run 28335038205.

Keep [#89](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/89) open until branch-protection evidence is verified.

Keep [#90](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/90) open until deployment/access evidence is complete.

Keep [#91](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/91) aligned with private Moodle-only UAT recording evidence.

Keep [#92](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/92) aligned with the completed combined Sprint Review/UAT session and Moodle-only recording evidence.

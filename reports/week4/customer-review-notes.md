# Customer Sprint Review and UAT Notes

## 27 June 2026 Combined Sprint Review and Customer UAT

**Participants:** Customer representative and project team members

**Publication status:** These notes contain no personal names, credentials, private links, exact private access details, or confidential business information.

A recorded customer session took place on 27 June 2026 and included both the Sprint Review and customer UAT. During the session, the team reviewed the Sprint Goal and delivered increment, demonstrated the product, discussed customer feedback and remaining risks, and executed UAT-01, UAT-02, and UAT-03.

The private recording URL, exact timecodes, recording permission evidence, customer identity, credentials, and private access details are supplied only through Moodle and are intentionally excluded from the public repository.

### Sprint Goal Reviewed

The planned Sprint Goal was to improve reliability and verifiability of the Route Optimization Platform by addressing selected customer feedback, preserving submitted jobs across restarts, improving solver robustness, defining measurable quality requirements, and adding automated quality gates.

### Delivered Increment Discussed

The discussion covered:

- the current route optimization platform;
- Docker-based run method;
- university VM deployment and customer access limitations;
- current solver behaviour;
- skipped optional order reporting;
- PostgreSQL-backed job history;
- quality requirements and automated verification;
- public demo, presentation, release, and remaining risks.

### Deployment and Customer Access

The university VM deployment is documented as reachable only from the Innopolis University network. Customer access from outside that network is not publicly verified.

Docker was discussed as a runnable fallback. The team agreed that either external access to the hosted application or another explicitly agreed remote access method still needs to be verified.

### UAT Result

Sanitized UAT result:

- UAT-01: submit a delivery instance and receive an optimized solution - passed according to sanitized UAT notes.
- UAT-02: validate a custom solution through the validator - passed according to sanitized UAT notes.
- UAT-03: retrieve previously submitted solutions from history - passed according to sanitized UAT notes.

Private evidence supplied outside the public repository:

- recording URL;
- exact UAT/Sprint Review timecodes;
- recording permission evidence.

## Addressed Customer Feedback

The team tracked customer feedback through:

- [#13 - Skipped optional orders report](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/13)
- [#23 - Solver refactoring and performance](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/23)
- [#85 - Persist jobs and results across restarts](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/85)
- [#87 - Define quality requirements and QRT specifications](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/87)
- [#88 - Add automated tests, coverage, and QA checks](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/88)
- [#90 - Update VM deployment and create the Sprint release](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/90)
- [#97 - Compare solver with baseline and analyze greedy-stage impact](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/97)

## Quality Requirements and Automated Evidence

The Assignment 4 quality model covers:

- solver functional correctness;
- solver time behaviour with a 900 second fixed benchmark threshold;
- recoverability of stored jobs;
- confidentiality of public error responses.

Verified protected-main evidence after merged [PR #106](https://github.com/Team-9-swp/Route-optimization-Platform-swp/pull/106):

- CI Pipeline [run 28335038211](https://github.com/Team-9-swp/Route-optimization-Platform-swp/actions/runs/28335038211) passed on `main` commit `95cc4804922d8ce053afea607f172817747f742a`;
- Link Check [run 28335038205](https://github.com/Team-9-swp/Route-optimization-Platform-swp/actions/runs/28335038205) passed;
- backend unit/integration tests: `39 passed`, `1 deselected`;
- QRTs: `15 passed`;
- coverage: `app/service.py` 100%, `app/repository.py` 97%, `app/api.py` 100%, total `app/` 94%;
- Ruff and Black passed as blocking backend checks;
- Bandit passed with no medium/high severity findings across 539 lines;
- frontend `npm run typecheck` and `npm run build` passed.

## Customer Feedback

The customer requested or recommended:

1. Compare the current solver with the baseline using the same selected scenarios, inputs, runtime limits, and metrics.
2. Investigate whether the greedy stage causes weaker objective values.
3. Consider a more joint optimization approach for vehicle routes, loader assignments, and optional-order decisions.
4. Provide accessible product access outside the university network or agree on another remote access method.

## Decisions

- Deployment accessibility remains an important blocker for customer access evidence.
- Docker remains the documented fallback run method.
- GitHub Release [`v1.2.0`](https://github.com/Team-9-swp/Route-optimization-Platform-swp/releases/tag/v1.2.0) is published from protected `main`.
- Baseline comparison and greedy-stage analysis are tracked in [#97](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/97) and the public benchmark report.
- Broader joint optimization remains Product Backlog work under [#23](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/23).
- [#91](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/91) and [#92](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/92) track private Moodle-only recording evidence and public reporting consistency.

## Remaining Gaps and Risks

- The university VM deployment is not publicly verified as accessible outside the Innopolis University network.
- Branch protection / required-check evidence requires organization admin verification.
- Private recording URL, exact timecodes, permission evidence, customer identity, credentials, and private access details are not committed publicly.
- Solver quality relative to a baseline remains a broader product risk unless benchmark comparison evidence is reviewed.

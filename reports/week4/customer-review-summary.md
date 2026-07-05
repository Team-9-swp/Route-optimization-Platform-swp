# Customer Review Summary

## Summary

A recorded customer session took place on 27 June 2026 and included both the Sprint Review and customer UAT.

The team reviewed the Sprint Goal and delivered increment, demonstrated the product, discussed customer feedback and remaining risks, and executed UAT-01, UAT-02, and UAT-03.

The three active UAT scenarios are recorded as passed in the maintained UAT documentation.

The private recording URL, customer identity, and private access information are intentionally excluded from the public repository and are supplied only through Moodle.

## Sprint Goal

The Sprint Goal was to deliver a more reliable and verifiable Route Optimization Platform by addressing selected customer feedback, preserving submitted jobs across restarts, improving solver robustness, and enforcing automated quality gates through tests and CI.

The product code increment is present on `main`, PR #106 plus protected-main GitHub Actions provide public CI evidence, and GitHub Release `v1.2.0` is published. Remaining public evidence work is limited to branch-protection verification and deployment/access verification; private recording evidence stays outside the repository.

## Increment and Product Access

The product is runnable with Docker Compose and uses PostgreSQL for persistent job history.

The university VM deployment is documented as limited to the Innopolis University network. Customer access from outside that network is not verified in public evidence. Issue [#90](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/90) remains open until deployment/access and release criteria are actually satisfied.

## UAT Result

| Scenario | Public sanitized result | Evidence limitation |
|---|---|---|
| UAT-01 - Submit a delivery instance and receive an optimized solution | Passed according to 27 June combined Sprint Review/UAT notes | Private recording URL, timecodes, and permission evidence are Moodle-only |
| UAT-02 - Validate a custom solution through the validator | Passed according to 27 June combined Sprint Review/UAT notes | Private recording URL, timecodes, and permission evidence are Moodle-only |
| UAT-03 - Retrieve previously submitted solutions from history | Passed according to 27 June combined Sprint Review/UAT notes | Private recording URL, timecodes, and permission evidence are Moodle-only |

Issue [#91](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/91) tracks Moodle-only UAT recording evidence that is intentionally not committed publicly.

## Quality Evidence Status

Implemented quality areas:

- `QR-FC-01`: solver functional correctness;
- `QR-PE-01`: solver time behaviour with a 900 second threshold;
- `QR-RE-01`: PostgreSQL recoverability;
- `QR-SE-01`: safe error confidentiality.

Verified protected-main CI evidence after merged [PR #106](https://github.com/Team-9-swp/Route-optimization-Platform-swp/pull/106):

- CI Pipeline [run 28335038211](https://github.com/Team-9-swp/Route-optimization-Platform-swp/actions/runs/28335038211) passed on `main` commit `95cc4804922d8ce053afea607f172817747f742a`.
- Link Check [run 28335038205](https://github.com/Team-9-swp/Route-optimization-Platform-swp/actions/runs/28335038205) passed.
- Backend unit/integration tests passed: `39 passed`, `1 deselected`.
- QRTs passed: `15 passed`.
- Coverage: `app/service.py` 100%, `app/repository.py` 97%, `app/api.py` 100%, total `app/` 94%.
- Ruff, Black, Bandit, frontend typecheck, and frontend production build passed.

Final evidence still needed:

- branch-protection / required-check verification by a repository or organization admin;
- deployment/customer access verification;
- private recording URL, exact timecodes, and recording permission evidence through Moodle or another approved private channel.

## Main Customer Feedback

| Feedback | Response |
|---|---|
| Show skipped optional orders. | Implemented and linked to [#13](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/13). |
| Preserve calculation history. | Implemented with PostgreSQL persistence and linked to [#85](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/85). |
| Measure solver execution time. | Covered by `QR-PE-01`, `QRT-PE-01`, and benchmark documentation. |
| Compare solver quality with a baseline and investigate greedy-stage impact. | Tracked through [#97](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/97) and `reports/week4/solver-benchmark.md`; broader solver redesign remains [#23](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/23). |
| Make the product accessible outside the university network or agree on another access method. | Still tracked by [#90](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/90). |

## Open Decisions and Action Points

| Action | Issue | Current status |
|---|---|---|
| Verify external or explicitly agreed customer access. | [#90](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/90) | Open |
| Keep private combined Sprint Review/UAT recording URL, exact timecodes, and permission evidence in Moodle only. | [#91](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/91), [#92](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/92) | Private evidence |
| Verify branch protection / required checks. | [#89](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/89) | Open |

## Remaining Risks

- The public repository does not verify customer access to the hosted deployment.
- The public repository does not include private recording links or timecodes.

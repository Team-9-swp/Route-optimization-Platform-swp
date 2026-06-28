# Customer Review Summary

## Summary

Assignment 4 has two separate customer-evidence events:

- **26 June 2026:** partial Sprint Review / customer meeting. The recording was not saved because of a technical failure, and UAT was not completed because the customer could not access the hosted product outside the Innopolis University network.
- **27 June 2026:** separate recorded customer UAT session. Sanitized notes record UAT-01, UAT-02, and UAT-03 as passed. The public repository does not contain the recording link, exact timecodes, customer identity, credentials, or private access details.

The 27 June recording must not be treated as the final Sprint Review unless private notes or timecodes verify that it also covered every required Sprint Review topic.

## Sprint Goal

The Sprint Goal was to deliver a more reliable and verifiable Route Optimization Platform by addressing selected customer feedback, preserving submitted jobs across restarts, improving solver robustness, and enforcing automated quality gates through tests and CI.

The product code increment is present on `main`, and PR #106 plus protected-main GitHub Actions provide public CI evidence. Final Assignment 4 evidence still depends on branch-protection verification, deployment/access verification, private evidence, screenshots, and post-merge release creation.

## Increment and Product Access

The product is runnable with Docker Compose and uses PostgreSQL for persistent job history.

The university VM deployment is documented as limited to the Innopolis University network. Customer access from outside that network is not verified in public evidence. Issue [#90](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/90) remains open until deployment/access and release criteria are actually satisfied.

## UAT Result

| Scenario | Public sanitized result | Evidence limitation |
|---|---|---|
| UAT-01 - Submit a delivery instance and receive an optimized solution | Passed according to 27 June UAT notes | Private recording URL, timecodes, and permission evidence required |
| UAT-02 - Validate a custom solution through the validator | Passed according to 27 June UAT notes | Private recording URL, timecodes, and permission evidence required |
| UAT-03 - Retrieve previously submitted solutions from history | Passed according to 27 June UAT notes | Private recording URL, timecodes, and permission evidence required |

Issue [#91](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/91) should remain open until the private UAT evidence is verified.

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
- private UAT recording URL, exact timecodes, and recording permission evidence through Moodle or another approved private channel;
- final Sprint Review evidence;
- screenshots under `reports/week4/images/`;
- final `v1.2.0` release after this documentation evidence PR is merged.

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
| Verify external or explicitly agreed customer access and create the final release after merge. | [#90](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/90) | Open |
| Verify private UAT recording URL, exact timecodes, and permission evidence. | [#91](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/91) | Open |
| Verify or conduct final Sprint Review recording covering all required topics. | [#92](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/92) | Open |
| Verify branch protection / required checks. | [#89](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/89) | Open |
| Create post-merge `v1.2.0` release from the final protected-`main` commit. | [#90](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/90) | Pending post-merge |

## Remaining Risks

- The public repository does not verify customer access to the hosted deployment.
- The public repository does not include private recording links or timecodes.
- The final Sprint Review is not verified as complete by public notes.
- The final release cannot be created until this documentation evidence PR is merged into `main`.

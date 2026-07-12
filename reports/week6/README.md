# Week 6 Report — Trial

## Project Overview

**Project:** Route Optimization Platform  
**Team:** Team 9  
**Week:** 6 (2026-07-06 to 2026-07-12)  
**Focus:** Customer trial — reconfirm all UAT scenarios after Sprint 5 follow-up fixes; prepare for Week 7 transition confirmation.

## Week 6 Changes Since Sprint 5

| Area | Commit | Description |
|---|---|---|
| Solver determinism | `d3181fe` | Seed `np.random`, use local `Random` for `LoaderSA` to ensure reproducible same-seed results |
| SA time budget | `da1bb98` | Fix simulated annealing time budget for short time limits (was forcing a minimum of 10s) |
| Auto-validation race | `6570970` | Move auto-validation before `COMPLETED` status update to fix a race condition in QRT test |
| Unserved optional in output | `5149b37` | Include `unserved_optional` in solver output result dict |
| Internal key stripping | `72c14d6` | Strip internal keys (`_cost`, `_evaluator`) before storing result in DB |

## UAT Trial Results

All 5 active UAT scenarios were reconfirmed with the customer during the Week 6 trial session (2026-07-10).

| ID | Title | Result |
|---|---|---|
| UAT-01 | Submit a delivery instance and receive an optimised solution | Passed |
| UAT-02 | Validate a custom solution through the validator | Passed |
| UAT-03 | Retrieve previously submitted solutions from history | Passed |
| UAT-04 | View route visualization for each vehicle and loader | Passed |
| UAT-05 | Reproducible solver results with fixed seed | Passed |

**Summary:** 5/5 passed, 0 failed, 0 blocked. All acceptance criteria remain satisfied.

## Customer Feedback Points

1. **All 5 scenarios accepted.** The customer confirmed that all acceptance criteria remain satisfied and the product meets the expected behavior for trial use.
2. **Solver determinism verified.** The customer noted that same-seed reproducibility now works correctly (previously inconsistent in Sprint 5 review), confirming the fix from commits `d3181fe` and `da1bb98`.
3. **Product access via screen sharing.** The customer acknowledged that external deployment access is still pending but screen sharing remains an acceptable interim method for the trial.

## Items Still Needing Improvement

1. **External customer access.** Deployment access outside the university network is still unresolved and tracked in [#90](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/90). The customer confirmed this is acceptable for the Week 6 trial but expects a resolution for Week 7 transition.
2. **Route map responsiveness on large instances.** Previously noted SVG rendering lag on large instances remains deferred; acceptable for trial use.

## Resulting PBIs and Issues

| ID | Title | Priority | Notes |
|---|---|---|---|
| PBI-W6-01 | Resolve external customer deployment access for Week 7 transition | High | Customer confirmed this is the critical path for transition confirmation. |

## Recording and Publication

**Session format:** Combined UAT trial session with customer  
**Session language:** Russian  
**Private evidence:** Recording link, exact timecodes, and permission evidence are submitted through Moodle only.  
**Public evidence:** This sanitized English report.

Private recording links, exact timecodes, customer identity, credentials, and private access details are intentionally excluded from this public report.

## UAT Documentation

Updated UAT scenarios with Week 6 execution records:

- [User Acceptance Tests](../../docs/user-acceptance-tests.md)

## Next Steps

- Resolve external customer deployment access ([#90](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/90)) for Week 7 transition.
- Conduct Week 7 transition confirmation session with customer.
- Prepare Week 7 transition report.

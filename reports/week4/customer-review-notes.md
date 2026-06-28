# Customer Review Notes

## 26 June 2026 Partial Sprint Review

**Participants:** Customer representative and project team members

**Recording status:** The meeting took place, but the recording was not saved because of a technical recording failure. These sanitized notes were reconstructed from team notes.

**Publication status:** These notes contain no personal names, credentials, private links, exact private access details, or confidential business information.

### Sprint Goal Reviewed

The planned Sprint Goal was to improve reliability and verifiability of the Route Optimization Platform by addressing selected customer feedback, preserving submitted jobs across restarts, improving solver robustness, defining measurable quality requirements, and adding automated quality gates.

The complete Sprint increment was not accepted as finished during this meeting.

### Delivered Increment Discussed

The discussion covered:

- the current route optimization platform;
- Docker-based run method;
- university VM deployment;
- current solver behaviour;
- planned quality requirements and automated verification.

Unfinished Assignment 4 features were not recorded as completed demonstrations.

### Deployment and Customer Access

The customer could not open the hosted website because the university VM deployment was reachable only from the Innopolis University network while the customer was outside Innopolis.

Docker was discussed as a temporary fallback. The team agreed to investigate either external access to the hosted application or another explicitly agreed remote access method.

### UAT Result for 26 June

Customer-executed UAT was not completed during this meeting.

Therefore:

- no UAT scenario should be marked passed based on the 26 June meeting;
- the increment was not accepted by the customer through UAT on 26 June;
- a separate recorded UAT session was required.

## 27 June 2026 Customer UAT

A separate recorded customer UAT session exists from 27 June 2026. Public repository files include only sanitized results and do not include the recording URL, exact timecodes, recording permission evidence, customer identity, credentials, or private access details.

Sanitized UAT result:

- UAT-01: submit a delivery instance and receive an optimized solution - passed according to sanitized UAT notes.
- UAT-02: validate a custom solution through the validator - passed according to sanitized UAT notes.
- UAT-03: retrieve previously submitted solutions from history - passed according to sanitized UAT notes.

Private evidence still required for Moodle or another approved private channel:

- recording URL;
- exact UAT timecodes;
- recording permission evidence.

The available public notes do not verify that the 27 June recording also covered all required Sprint Review topics. It must not be used as final Sprint Review evidence unless private notes or timecodes confirm the complete Sprint Review agenda.

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

- Deployment accessibility remains an important blocker for customer access and final release evidence.
- Docker remains the documented fallback run method.
- Baseline comparison and greedy-stage analysis are tracked in [#97](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/97) and the public benchmark report.
- Broader joint optimization remains Product Backlog work under [#23](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/23).
- [#91](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/91) should remain open until private UAT recording evidence is verified.
- [#92](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/92) should remain open until a final Sprint Review recording or verified timecodes cover all required topics.

## Remaining Gaps and Risks

- The university VM deployment is not publicly verified as accessible outside the Innopolis University network.
- Final GitHub release `v1.2.0` must be created from the final protected-`main` commit after this documentation evidence PR is merged.
- Branch protection / required-check evidence requires organization admin verification.
- Solver quality relative to a baseline remains a broader product risk unless benchmark comparison evidence is reviewed.

## Required Follow-up Sprint Review Evidence

If the 27 June recording is used for final Sprint Review evidence, private notes or timecodes must verify all of the following:

1. recording permission before recording starts;
2. planned Sprint Goal;
3. delivered Sprint increment;
4. addressed customer feedback;
5. customer execution of UAT scenarios;
6. UAT results;
7. quality requirements;
8. automated QRT results;
9. latest protected-main CI evidence;
10. quality gates that continue into later work;
11. remaining gaps and risks;
12. resulting Product Backlog changes.

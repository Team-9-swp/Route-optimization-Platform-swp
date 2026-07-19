# Sprint Retrospective — Week 7 (Sprint 5)

**Project:** Route Optimization Platform

**Sprint:** Sprint 5 — Week 7 Final Transition and MVP v3

**Sprint dates:** 2026-07-13 — 2026-07-19

**Milestone:** [Sprint 5 — Week 7 Final Transition and MVP v3](https://github.com/Team-9-swp/Route-optimization-Platform-swp/milestone/9)

**Canonical selected size:** `73 Story Points`, documented in [#183](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/183)

## What went well

- The final user-facing workflow improved materially: actual execution duration, two-decimal Objective presentation, interactive route/schedule views, and JSON upload were merged through [PR #205](https://github.com/Team-9-swp/Route-optimization-Platform-swp/pull/205) and [PR #207](https://github.com/Team-9-swp/Route-optimization-Platform-swp/pull/207).
- Solver follow-up work was merged through [PR #200](https://github.com/Team-9-swp/Route-optimization-Platform-swp/pull/200), and the linked maintenance issues [#184](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/184) and [#204](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/204) were closed.
- The team kept readiness separate from customer-side operation. The final handover record states `Ready for independent use` without claiming an unverified customer deployment.
- The customer confirmed that the customer-facing documentation, transition model, final corrections, and reached handover scope are sufficient and accepted.
- The public evidence set uses sanitized documents and a separately verified public demo link; private recording/access information remains outside the repository.

## What did not go well

- Sprint planning needed correction from the earlier 58 SP figure to the canonical **73 Story Points**, and overlapping wrapper/concrete issues made the total harder to audit.
- The improved visualization was not ready for customer execution during the recorded Sprint Review. Later merge and build evidence is team verification, not customer UAT.
- Customer-side deployment and independent result reproduction were not executed, so a stronger transition level cannot be supported.
- Several issue bodies were closed with stale `To Do` or `In Progress` fields, creating inconsistent evidence that required final cleanup.
- [#185](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/185) was closed with checked criteria, but final repository inspection did not locate a dedicated same-seed-twice regression test by name. Issue closure and inspectable code evidence should have been reconciled before completion.
- Final release, screenshot, and Moodle packaging work did not fit into this documentation PR and remains explicitly open in [#190](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/190) and [#194](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/194).

## What changed based on the Week 6 retrospective

The [Week 6 retrospective](../week6/retrospective.md) identified determinism protection, the return-to-depot cost edge case, visualization validation, and meeting/access preparation.

1. **Determinism verification:** [#185](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/185) is closed, but the expected dedicated regression test is not readily identifiable in the repository. The result is an evidence-quality gap, not a basis for a stronger claim.
2. **Return-to-depot maintenance:** solver changes were merged in [PR #200](https://github.com/Team-9-swp/Route-optimization-Platform-swp/pull/200), and [#204](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/204) is closed with its acceptance criteria checked.
3. **Visualization:** the implementation was expanded and merged in [PR #205](https://github.com/Team-9-swp/Route-optimization-Platform-swp/pull/205). The observed result is team-verified functionality, while customer-executed finished-product UAT remains absent.
4. **Review evidence:** a sanitized [summary](sprint-review-summary.md) and [transcript](sprint-review-transcript.md) were prepared. Exact timecodes and the private recording remain Moodle-only.

## Observations and results

- Small presentation improvements mattered alongside algorithm work: duration and Objective formatting directly improve interpretability without changing stored result values.
- Closing issues is not sufficient traceability when the issue body, code, test name, and PR links disagree. Final audits must check all four.
- The customer can accept documentation and the reached transition scope while still intending to reproduce the product later. Acceptance, readiness, and operation are different evidence categories.
- A final course increment can be prepared before its SemVer packaging exists. Release status must follow the actual tag/release, not the planned version name.

## Lessons from final transition and handover

- State the support boundary, access model, operational limitations, and evidence classification in the handover itself; do not rely on meeting context.
- Keep administrative confirmation separate from technical follow-up. Customer acceptance is closed, while customer-side execution remains an optional follow-up and technical limitations remain visible.
- Public artifacts should link sanitized evidence and clearly point private recording, identity, and exact-time evidence to the private submission channel.

## Lessons from final product delivery

- Merge current `main` before finalizing evidence so reports describe the actual product, not an obsolete branch snapshot.
- Treat release packaging as its own gated activity. A prepared MVP v3 product state does not imply that a final tag or GitHub Release exists.
- Plan evidence work early enough to capture screenshots, stable permalinks, and customer execution while the relevant environment is available.

## Post-course maintenance recommendations

1. Add or clearly identify a fast automated regression that runs the solver twice with the same fixture/seed and compares objective, vehicle routes, loader routes, and unserved optional orders; link the exact test from [#185](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/185).
2. Maintain the Docker Compose quick start, troubleshooting steps, dependency updates, and security patches; record any reproducible post-course defects as sanitized GitHub issues without promising indefinite operational support.

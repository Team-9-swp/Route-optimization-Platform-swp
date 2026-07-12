# Sprint Retrospective — Week 6 (Sprint 4)

**Project:** Route Optimization Platform
**Team:** Team-9-swp
**Date:** 2026-07-12
**Sprint:** Sprint 4 — Determinism & Baseline

## What went well

*   **Determinism fix was straightforward.** The team quickly identified that Nevergrad's internal random seed generation was the root cause of non-deterministic results. Passing our own seed (seed 42) resolved the issue cleanly, demonstrating good understanding of the solver internals.
*   **Baseline achieved.** Beating the baseline on test case 4 by ~0.5% was a concrete, measurable success that the customer acknowledged and validated during the Sprint Review.
*   **Customer transition discussion went smoothly.** The meeting with the customer resulted in a clear deployment plan — customer will self-deploy from the `master` branch using a single container with full UI. No ambiguity remained on the delivery format.
*   **Effective communication.** The team clearly explained the algorithm's architecture (Nevergrad → PyVRP → greedy loader assignment → simulated annealing) to the customer, building trust in the technical approach.

## What did not go well

*   **Driver return-to-depot edge case was discovered late.** The cost-calculation issue (routes split by zeros counted as separate drivers) was identified during the Sprint Review meeting rather than during development or testing. Earlier detection would have allowed time for a fix in this sprint.
*   **Gantt chart not yet visible.** Although the Gantt chart was confirmed as in-scope for Sprint 4, it was not demonstrated during the review. Progress was not discussed in detail, suggesting it may be behind schedule.
*   **Calculation time on dashboard ambiguity.** The customer asked about this feature and was told it was "already there by status" but it was unclear whether it was fully implemented or just planned. This created a minor communication gap.
*   **Meeting platform dependency.** The customer noted potential network limitations for the next meeting, requiring a switch to Zoom. This was not anticipated and may affect future meeting reliability.

## What the team changed or attempted to change based on the previous Sprint Retrospective, and what results they observed

From the Sprint 5 (Week 5) retrospective, the team identified these action items and observed these results:

1. **Improve deployment strategy.** The previous retrospective called for researching a more permanent externally accessible deployment solution. Result: The team focused on self-deployment by the customer instead of external hosting, which the customer accepted as the preferred handover model.
2. **Optimize test suite.** The previous retrospective called for test performance optimization. Result: No significant changes were made in Sprint 4 — the focus shifted to algorithm determinism and baseline comparison.
3. **Improve frontend UX.** The previous retrospective called for improving error message display. Result: Not addressed in Sprint 4 — deferred to Sprint 5.
4. **Refine the Definition of Done.** The previous retrospective called for updating the PR template with a DoD checklist. Result: The team continued using the existing workflow without formal changes.

## Action points

1. **Add determinism verification to CI.** Run the solver twice with the same seed and assert identical results. This prevents regressions on the determinism fix. **Owner:** Team. **Target:** Sprint 5.
2. **Fix driver return-to-depot cost calculation.** Investigate and fix the routes-split-by-zeros edge case where return trips are counted as separate drivers. **Owner:** Algorithm team. **Target:** Sprint 5.
3. **Complete Gantt chart visualisation.** Ensure the Gantt chart is demonstrable by the end of Sprint 5. **Owner:** Frontend team. **Target:** Sprint 5.
4. **Verify Zoom access for Week 7 meeting.** Confirm Zoom works for all participants as a backup meeting platform before the next customer meeting. **Owner:** Team lead. **Target:** Before Week 7 meeting.

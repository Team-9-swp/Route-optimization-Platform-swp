# Sprint Retrospective — Week 7 (Sprint 5)

> **DRAFT — to be completed during the Week 7 Sprint Retrospective.**
> This artifact is prepared in advance with the Sprint 5 context that is
> already known. The inspection sections (`What went well`, `What did not go
> well`, and the final `Action points`) record the team's actual observations
> and must be filled **after** the Sprint Review, before this draft banner is
> removed.

**Project:** Route Optimization Platform
**Team:** Team-9-swp
**Sprint:** Sprint 5 — Week 7 Final Transition and MVP v3
**Sprint dates:** 2026-07-13 — 2026-07-19
**Milestone:** [Sprint 5 — Week 7 Final Transition and MVP v3](https://github.com/Team-9-swp/Route-optimization-Platform-swp/milestone/9)

## Sprint context

- **Sprint Goal (from roadmap):** Complete follow-up maintenance based on the
  Week 6 customer trial, resolve remaining product and transition blockers,
  verify independent customer access, update customer-facing documentation,
  confirm the final handover outcome, and deliver the final course version,
  **MVP v3**.
- **Selected scope:** 13 issues, 58 Story Points (canonical planning issue
  [#183](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/183)).
- **Intended release:** [`v1.5.0`](https://github.com/Team-9-swp/Route-optimization-Platform-swp/releases)
  (MVP v3), SemVer-higher than the Week 6 trial release `v1.4.0`, from protected
  `main`.

## What went well

<!-- Complete after the Sprint Review. -->

## What did not go well

<!-- Complete after the Sprint Review. -->

## What the team changed or attempted to change based on the previous Sprint Retrospective, and what results they observed

From the [Week 6 (Sprint 4) retrospective](../week6/retrospective.md), the team
carried these action items into Sprint 5. The planned resolution for each is
recorded below; the **observed result** must be confirmed when this section is
finalized.

1. **Add determinism verification to CI** (Week 6 action, owner: Team, target:
   Sprint 5). Run the solver twice with the same seed and assert identical
   results to protect the Week 6 determinism fix.
   - Planned work item:
     [#185 — automated solver determinism verification](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/185).
   - **Observed result:** _(to confirm)_.

2. **Fix driver return-to-depot cost calculation** (Week 6 action, owner:
   Algorithm team, target: Sprint 5). Investigate and fix the edge case where
   vehicle routes split by depot returns (zeros) are counted as separate
   drivers.
   - Planned work item:
     [#184 — Sprint 5 follow-up maintenance](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/184).
   - **Observed result:** _(to confirm)_.

3. **Validate the Gantt chart visualisation** (Week 6 action, owner: Frontend
   team, target: Sprint 5). The implementation was reported complete in Week 6;
   verify it during customer-side testing.
   - **Observed result:** _(to confirm)_.

4. **Verify Zoom access for the Week 7 meeting** (Week 6 action, owner: Team
   lead, target: before the Week 7 meeting). Confirm Zoom works for all
   participants as a backup meeting platform.
   - **Observed result:** _(to confirm)_.

## Action points

<!-- This is the final Sprint of the course, so action points are framed as
     post-course follow-ups rather than a next-Sprint backlog. Add one or two
     concrete follow-up actions after the retrospective. -->

_To be added after the Week 7 Sprint Retrospective._

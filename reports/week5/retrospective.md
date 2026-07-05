# Sprint Retrospective - Week 5

**Date:** 2026-07-05
**Sprint:** Sprint 5 — MVP v2

## What went well

- The validator-compatible solution export feature (`feat(api): export
  validator-compatible solution JSON`, issue #126) was merged to `main`,
  closing the compatibility gap between UI-exported solutions and the
  project validator.
- The `feat/assignment5-auto-deploy` branch was merged into `main`,
  delivering automatic deployment triggered by protected-`main` CI checks
  (issue #130).
- During auto-deploy work, the team found and fixed a real deployment
  reliability issue: database schema reconciliation was not idempotent,
  causing `DuplicateTable` errors on repeated deploys. Making this step
  idempotent removed a concrete class of deployment failures.
- Older customer feedback items (#13, #14, #85, #87, #88) remained closed
  and stable as maintained product behavior through Sprint 5, rather than
  regressing.
- Solver-quality investigation (#127) continued using a reproducible,
  fixed-seed baseline instead of reopening the historical, now-closed
  discussion in #23 and #97.
- The column-generation research spike (#128) was scoped and treated
  explicitly as research, not a committed feature, keeping it from blocking
  other Sprint 5 work.

## What did not go well

- The known product bug (#129) still required reproduction details before
  implementation could start, so it was not confirmed fixed by the time of
  this report.
- The idempotency bug in the deployment schema reconciliation step was only
  discovered while building the auto-deploy pipeline, not caught earlier —
  suggesting deployment failure modes were under-tested before this Sprint.
- Gantt schedule visualization (#125) and workload-balance metric (#124)
  were planned for Sprint 5 but did not reach implementation. Both remain
  open and will be reprioritized for the next Sprint.

## Changes compared with the previous Sprint

- Deployment moved from a manually published release process toward
  automatic deployment from protected `main`, hardened by the idempotency
  fix found during this Sprint's implementation.
- Product export capability moved from "UI-only" to validator-compatible,
  closing a concrete interoperability gap (#126).
- Solver-quality discussion moved from closed, standalone historical issues
  (#23, #97) to a single actively tracked, reproducible investigation (#127).

## Note on workload distribution

Architecture documentation, ADRs, the known-bug fix, and automatic
deployment configuration were kept with the team member who already has the
deepest context on the solver and deployment setup, rather than
redistributed to even out Story Points. The idempotency bug found during
auto-deploy work is a concrete example of the kind of deployment-specific
knowledge that made this ownership choice valuable.

## Concrete process changes for next Sprint

1. **Add a deployment dry-run/idempotency check to CI** before merging
   deployment-related changes, so schema-reconciliation issues like the
   `DuplicateTable` case are caught before they reach a real deploy.
2. **Require reproduction steps as part of the Definition of Done for bug
   PBIs** before implementation starts, applied consistently (as already
   done for #129), so bug fixes are not blocked mid-sprint by missing
   repro details.

## Follow-up

This retrospective should be reviewed against the actual Sprint
Retrospective discussion with the team before being treated as final,
particularly the "What did not go well" section.

# Roadmap

The Route Optimization Platform was developed in Sprint increments. Earlier Sprints delivered **MVP v1** (`v1.0.0`) and **MVP v2** ([`v1.3.0`](https://github.com/Team-9-swp/Route-optimization-Platform-swp/releases/tag/v1.3.0)) as a Docker Compose stack with a FastAPI backend, PostgreSQL persistence, a PyVRP/Nevergrad solver, hard-constraint validation, and a React web UI.

Assignment 6 used two formal Sprint containers: Sprint 4 produced the Week 6 trial release and Sprint 5 prepared the final course product state, **MVP v3**. The issue tracker and milestones remain the source of truth for backlog state.

## Sprint 4 — Week 6 Trial Release and Transition Readiness

- **Milestone:** [Sprint 4 — Week 6 Trial Release and Transition Readiness](https://github.com/Team-9-swp/Route-optimization-Platform-swp/milestone/8)
- **Dates:** 2026-07-06 — 2026-07-12
- **Published trial release:** [`v1.4.0`](https://github.com/Team-9-swp/Route-optimization-Platform-swp/releases/tag/v1.4.0)
- **Outcome:** manual solver time-limit control, Gantt schedule visualization, customer-facing documentation, UAT/Sprint Review evidence, and the Week 6 public report were delivered. The [Week 6 report](../reports/week6/README.md) preserves the detailed evidence.

## Sprint 5 — Week 7 Final Delivery (MVP v3)

- **Product Backlog / Project:** [Route Optimizer Backlog](https://github.com/orgs/Team-9-swp/projects/1)
- **Milestone:** [Sprint 5 — Week 7 Final Transition and MVP v3](https://github.com/Team-9-swp/Route-optimization-Platform-swp/milestone/9)
- **Dates:** 2026-07-13 — 2026-07-19
- **Sprint Goal:** Complete Week 6 follow-up maintenance, improve the final user-facing workflow, document the actual transition state, and prepare a verified final course increment for **MVP v3**.
- **Canonical selected size:** **73 Story Points**, as recorded in [#183](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/183). Duplicate #182 and overlapping coordination wrapper #184 are not double-counted.

### Completed or prepared work

- [#201 — actual execution duration](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/201), [#202 — two-decimal Objective presentation](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/202), and [#203 — interactive vehicle/loader route plan and schedule](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/203) were merged in [PR #205](https://github.com/Team-9-swp/Route-optimization-Platform-swp/pull/205).
- [#206 — restored JSON file upload](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/206) was merged in [PR #207](https://github.com/Team-9-swp/Route-optimization-Platform-swp/pull/207).
- Sprint 5 solver maintenance was merged in [PR #200](https://github.com/Team-9-swp/Route-optimization-Platform-swp/pull/200); the linked maintenance items [#184](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/184), [#185](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/185), and [#204](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/204) are closed. The repository does not contain a dedicated same-seed-twice regression test identifiable by name, so this roadmap does not claim more test evidence than the closed issue records and merged code provide.
- The current Sprint Review, UAT, handover, and planning evidence was merged in [PR #208](https://github.com/Team-9-swp/Route-optimization-Platform-swp/pull/208) and is finalized by the [Week 7 report](../reports/week7/README.md).
- The customer accepted the documentation set, transition model, final corrections, and reached handover scope. Customer-side deployment or independent result reproduction is not claimed.

## Final course outcome

The prepared final product state corresponds to **MVP v3**: it includes the interactive route and schedule views, actual solver execution duration, readable Objective presentation, restored JSON upload, updated solver maintenance, and final customer-facing handover evidence.

- **Handover level:** `Ready for independent use`
- **Customer-confirmation status:** `Accepted`
- **Latest published release:** `v1.4.0`
- **Final MVP v3 SemVer packaging/release:** Pending — tracked in [#190](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/190)

No speculative post-course version is planned here. Remaining work is limited to actual open evidence/release tasks and documented operational limitations, not a fabricated future release.

# Roadmap

The Route Optimization Platform is developed in Sprint increments. Earlier Sprints delivered **MVP v1** (`v1.0.0`) and **MVP v2** ([`v1.3.0`](https://github.com/Team-9-swp/Route-optimization-Platform-swp/releases/tag/v1.3.0)) — a Docker Compose stack with a FastAPI backend, PostgreSQL persistence, a PyVRP/Nevergrad solver, hard-constraint validation, and a React web UI.

Assignment 6 adds two formal Sprint containers: **Sprint 4** (Week 6) prepares a stable trial / handover candidate, and **Sprint 5** (Week 7) uses the customer's trial feedback to deliver the final course version, **MVP v3**. The selected Sprint Backlog items live in the issue tracker, assigned to the Sprint milestones; this roadmap links them rather than duplicating their content.

## Sprint 4 — Week 6 Trial Release and Transition Readiness

- **Milestone:** [Sprint 4 — Week 6 Trial Release and Transition Readiness](https://github.com/Team-9-swp/Route-optimization-Platform-swp/milestone/8)
- **Dates:** 2026-07-06 — 2026-07-12
- **Sprint Goal:** Deliver a stable Week 6 trial / handover-candidate release that the customer and TA can access, review the customer-facing documentation, execute UAT, discuss transition readiness, and identify follow-up work for Week 7.
- **Focus:** Produce a customer-accessible trial increment together with handover documentation, UAT / Sprint Review / transition-readiness evidence, and a clear Week 7 follow-up scope.

**Selected Sprint Backlog (linked PBIs):**

- Planning & release: #154 (refine backlog and plan Sprint 4/5), #155 (deliver Week 6 trial release).
- Product: #163 (Gantt chart visualization on the frontend), #171 (manual solver time limit on the New Job page), #166 (route optimization algorithm improvement for the trial).
- Customer-facing documentation: #161 (polish README, CONTRIBUTING, AGENTS), #162 (maintain `docs/customer-handover.md`).
- Customer trial, UAT & review: #164 (Week 6 customer trial and transition-readiness discussion), #157 (update and execute Week 6 UAT scenarios), #165 (Week 6 Sprint Review summary/transcript).
- Sprint events & reporting: #158 (Week 6 retrospective), #159 (Week 6 reflection and LLM report), #160 (Week 6 presentation slides and rehearsal video), #156 (Week 6 public report and Moodle evidence).

**Completed / deferred outcome:** The Gantt chart and manual time-limit controls, customer-facing documentation, UAT / Sprint Review / transition-readiness evidence, and the Week 6 public report were completed and published with the Week 6 trial / handover-candidate release [`v1.4.0`](https://github.com/Team-9-swp/Route-optimization-Platform-swp/releases/tag/v1.4.0). Customer-side deployment and the driver return-to-depot cost edge case remain Sprint 5 work; private evidence remains Moodle-only.

## Sprint 5 — Week 7 Final Delivery (MVP v3)

- **Milestone:** [Sprint 5 — Week 7 Final Transition and MVP v3](https://github.com/Team-9-swp/Route-optimization-Platform-swp/milestone/9)
- **Dates:** 2026-07-13 — 2026-07-19
- **Sprint Goal:** Complete follow-up maintenance based on the Week 6 customer trial, resolve remaining product and transition blockers, verify independent customer access, update customer-facing documentation, confirm the final handover outcome, and deliver the final course version, **MVP v3**.
- **Selected scope:** 13 issues, **58 Story Points**. Duplicate planning issue #182 is excluded; [#183](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/183) is canonical.

**Selected Sprint 5 issues:**

- **Planning and maintenance:** [#183 — refine and plan Sprint 5](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/183), [#184 — follow-up maintenance, including the driver return-to-depot cost edge case](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/184), [#185 — automated solver determinism verification](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/185).
- **Documentation and transition:** [#186 — final customer-facing documentation review](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/186), [#187 — verify final product transition and independent customer access](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/187).
- **UAT and Sprint Review:** [#188 — Week 7 UAT](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/188), [#189 — Week 7 Sprint Review](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/189).
- **MVP v3 release and demo:** [#190 — final MVP v3 release](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/190), [#191 — public sanitized MVP v3 demo](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/191).
- **Retrospective, reflection, reporting, and Demo Day:** [#192 — Week 7 retrospective](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/192), [#193 — reflection and LLM report](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/193), [#194 — Week 7 public report and Moodle evidence](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/194), [#195 — final Demo Day presentation](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/195).

All selected Sprint 5 issues remain open with Work Status `To Do`. Completion and release evidence will be recorded only after the corresponding Week 7 work is performed.

## Final course outcome

By the end of Week 7, the product should reach **MVP v3**: a runnable and accessible Route Optimization Platform with updated customer-facing documentation, current handover documentation, verified access instructions, final UAT / Sprint Review evidence, a public sanitized demo video, and a final SemVer release from the protected default branch.

No speculative post-course version planning is included. Remaining work, if any, will be documented as limitations, blockers, or follow-up items in `docs/customer-handover.md` and the Week 7 report.

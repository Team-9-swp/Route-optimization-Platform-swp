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

**Completed / deferred outcome:** The Gantt chart and manual time-limit controls, customer-facing documentation, UAT / Sprint Review / transition-readiness evidence, and the Week 6 public report were completed. Customer-side deployment, the driver return-to-depot cost edge case, and release creation are deferred to Sprint 5; private evidence remains Moodle-only.

## Sprint 5 — Week 7 Final Delivery (MVP v3)

Sprint 5 will be planned in detail after the Week 6 customer trial. Its Sprint milestone will be created from the confirmed Week 7 scope; the areas below are the expected follow-up, to be refined from customer feedback, UAT results, and transition-readiness blockers.

- **Sprint Goal (draft):** Complete follow-up maintenance, final transition, and delivery of the final course version, **MVP v3**.
- **Dates:** 2026-07-13 — 2026-07-19.

**Expected Week 7 follow-up areas:**

- Resolve Week 6 customer feedback and remaining transition blockers.
- Complete remaining algorithm improvements and product fixes, including the validator / fuel calculation / driver return-to-depot cost edge case.
- Finalize product access and the transition status; update `docs/customer-handover.md`.
- Publish the final **MVP v3** SemVer release (higher precedence than the Week 6 trial release) from protected `main`.
- Record the public sanitized MVP v3 demo video.
- Prepare the Week 7 public report and Moodle evidence.

## Final course outcome

By the end of Week 7, the product should reach **MVP v3**: a runnable and accessible Route Optimization Platform with updated customer-facing documentation, current handover documentation, verified access instructions, final UAT / Sprint Review evidence, a public sanitized demo video, and a final SemVer release from the protected default branch.

No speculative post-course version planning is included. Remaining work, if any, will be documented as limitations, blockers, or follow-up items in `docs/customer-handover.md` and the Week 7 report.

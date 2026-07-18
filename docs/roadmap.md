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
- **Sprint Goal:** Complete Week 6 follow-up maintenance, improve the final user-facing workflow, document the actual transition state, and prepare a verified final course increment for **MVP v3**.
- **Canonical selected size:** **73 Story Points**. The calculation counts #183 and #185–#195 as the course-task scope (53 SP), excludes duplicate #182 and treats #184 as a non-additive coordination wrapper, then adds the concrete product PBIs #201 (3 SP), #202 (1 SP), #203 (8 SP), #204 (5 SP), and #206 (3 SP), for another 20 SP. This preserves #204 as the canonical concrete maintenance PBI without counting the overlapping #184 wrapper twice.

**Live metadata state (audited 2026-07-19):** #182–#195, #201, #202, #203, #204, and #206 are assigned to milestone 9 and are present in the `Route Optimizer Backlog` Project. Status, assignee, Story Points, MVP Version, MoSCoW, milestone, and issue type are populated where supported. The Project's system `Reviewers` field is not editable for issue items; reviewer evidence remains in issue bodies and merged PR reviews. The existing `Sprint 5 Backlog` view still has the stale `Sprint 5 — MVP v2` filter because GitHub's available ProjectV2 API exposes no view-update mutation; the view therefore requires the documented manual filter change.

### Completed product PBIs

- [#201 — actual execution duration on Job Detail](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/201) (3 SP), merged in [PR #205](https://github.com/Team-9-swp/Route-optimization-Platform-swp/pull/205).
- [#202 — two-decimal Objective presentation on Job Detail and its validation result](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/202) (1 SP), merged in [PR #205](https://github.com/Team-9-swp/Route-optimization-Platform-swp/pull/205).
- [#203 — interactive vehicle/loader route plan and schedule](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/203) (8 SP), merged in [PR #205](https://github.com/Team-9-swp/Route-optimization-Platform-swp/pull/205).
- [#206 — restored JSON file upload](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/206) (3 SP), merged in [PR #207](https://github.com/Team-9-swp/Route-optimization-Platform-swp/pull/207).

### In progress or blocked

- **Planning:** [#183](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/183) is the canonical planning task. The roadmap, milestone, Project items, and supported fields are updated; only the unsupported API update of the stale `Sprint 5 Backlog` view filter remains.
- **Maintenance and verification:** coordination wrapper [#184](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/184), verification task [#185](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/185), and canonical concrete cost-fix PBI [#204](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/204) remain open. #184 is tracked but is not added to the Story Point total separately from #204.
- **Documentation, transition, and UAT:** [#186](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/186), [#187](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/187), and [#188](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/188) remain open because customer-side deployment/reproduction, the final visualization review, and complete documentation acceptance are not verified.
- **Sprint Review:** [#189](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/189) has a sanitized public transcript and summary. Recording and sanitized-transcript publication permission are confirmed; private recording details and Moodle-only activity timecodes still require private submission evidence.
- **Final delivery work:** [#190](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/190), [#191](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/191), [#192](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/192), [#193](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/193), [#194](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/194), and [#195](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/195) remain selected work. No reliable evidence identifies #194's actual implementer, so its ownership remains unassigned pending manual team confirmation; its report scope was not performed here.

The closed duplicate [#182](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/182) remains in milestone history but is excluded from canonical scope and totals.

## Final course outcome

The implemented MVP v3 candidate adds the interactive vehicle/loader route plan and schedule, actual execution duration, readable Objective presentation, and restored JSON upload while preserving the API, database, and saved jobs. The current handover level is **Ready for independent use** and the customer-confirmation status is **Accepted with follow-up items**.

Final MVP v3 release, customer-side reproduction evidence, finished-visualization review, public demo, and remaining course artifacts are still required before the final course outcome can be described as complete.

No speculative post-course version planning is included. Remaining work, if any, will be documented as limitations, blockers, or follow-up items in `docs/customer-handover.md` and the Week 7 report.

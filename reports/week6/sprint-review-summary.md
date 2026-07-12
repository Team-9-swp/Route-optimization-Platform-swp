# Sprint 4 Review Summary

**Project:** Route Optimization Platform
**Team:** Team 9
**Sprint:** Sprint 4 — Determinism & Baseline
**Session format:** Sprint Review with customer
**Session language:** Russian
**Public evidence type:** Sanitised English summary
**Private evidence:** Recording link, exact timecodes, and permission evidence are submitted through Moodle only.

Private recording links, exact timecodes, customer identity, credentials, and private access details are intentionally excluded from this public report.

## Recording and Publication Permission

At the beginning of the session, the team asked the customer representative for permission to record the meeting and publish a sanitised transcript/summary in the repository. Permission was granted during the recorded session.

## Sprint Review Agenda

1. Confirm recording and publication permission.
2. Review Sprint 4 goal and work completed.
3. Review algorithm determinism fix and UAT results.
4. Discuss transition-readiness and customer deployment.
5. Discuss baseline comparison results and algorithm changes.
6. Confirm product delivery format and next steps.
7. Discuss remaining Sprint 4 items (Gantt chart, calculation time).

## Sprint Goal Reviewed

The team reviewed the Sprint 4 goal: ensure algorithm determinism, beat baseline on test case 4, and prepare stable trial release for customer handover.

## Demonstrated / Discussed Increment

| Area | Related issue | Review result |
|---|---|---|
| Algorithm determinism | #155 | Determinism fixed. Customer confirmed the fix. |
| Baseline comparison — test case 4 | #156 | Team beat baseline by ~0.5% on test case 4 with seed 42. |
| Driver return-to-depot | #157 | Implemented; noted a minor cost-calculation edge case (routes split by zeros counted as separate drivers). Validator shows correct numbers. |
| Manual time limit | #158 | Implemented and released. |
| Gantt chart visualisation | #159 | In progress for this sprint. |
| Calculation time on dashboard | #160 | Feature present in UI; status confirmed. |
| Transition-readiness discussion | #161 | Discussed deployment, repository access, and customer self-deployment plan. |
| Customer deployment plan | #162 | Customer to deploy independently from `master` branch. |

## Customer Feedback and Decisions

| Feedback / observation | Decision | Follow-up |
|---|---|---|
| Algorithm is now deterministic. | Accepted. | No further action required. |
| Baseline beaten on test case 4 by ~0.5%. | Accepted. | Customer will verify independently from sources. |
| Driver return-to-depot creates a minor cost-calculation edge case (routes split by zeros). | Noted. | Fix planned for next sprint. |
| Customer wants full UI deployment, not just algorithm. | Accepted. | Deploy via single container with interface. |
| Customer to deploy independently from `master` branch. | Accepted. | Customer will deploy in Week 7. |
| Customer will run algorithm from sources and through the interface. | Accepted. | Customer will verify consistency. |
| Gantt chart visualisation to be completed in this sprint. | Accepted. | Continue work. |
| Calculation time on dashboard — feature present. | Confirmed. | No further action required. |
| Customer may have limited network access next week; use Zoom instead of Tele. | Accepted. | Use Zoom for Week 7 meeting. |

## Accepted Outcomes

- The customer confirmed algorithm determinism is fixed.
- The customer accepted the baseline comparison result (~0.5% improvement on test case 4).
- The customer confirmed the transition-readiness discussion and self-deployment plan.
- The customer confirmed full UI deployment is the expected delivery format.
- The customer confirmed Gantt chart is in scope for this sprint.

## Requested Changes

- Complete Gantt chart visualisation for vehicles and loaders.
- Continue preparation for customer handover.
- Address driver return-to-depot cost-calculation edge case in next sprint.

## Deferred Work

- Driver return-to-depot cost-calculation fix (routes split by zeros) — deferred to Sprint 5.
- Additional solver improvements — deferred to Sprint 5.
- Permanent external customer access — ongoing deployment item.

## Backlog Updates

| Follow-up item | Status |
|---|---|
| Algorithm determinism | Completed — #155 |
| Baseline comparison test case 4 | Completed — #156 |
| Driver return-to-depot | Completed — #157 (minor edge case deferred) |
| Manual time limit | Completed — #158 |
| Gantt chart visualisation | In progress — #159 |
| Calculation time on dashboard | Confirmed present — #160 |
| Transition readiness | Completed — #161 |
| Customer deployment plan | Completed — #162 |
| Customer self-deployment | Planned — Week 7 |

## Review Conclusion

The Sprint 4 Review was conducted with the customer. The team demonstrated algorithm determinism, confirmed baseline improvement on test case 4, discussed transition-readiness and deployment plan, and confirmed the Gantt chart is in scope for this sprint. The customer will deploy independently from the `master` branch in Week 7 and verify algorithm results from sources.

# Sprint 5 Review Summary

**Project:** Route Optimization Platform  
**Team:** Team 9  
**Sprint:** Sprint 5 — MVP v2  
**Session format:** Combined Sprint Review and UAT session  
**Session language:** Russian  
**Public evidence type:** Sanitized English summary  
**Private evidence:** Recording link, exact timecodes, and permission evidence are submitted through Moodle only.

Private recording links, exact timecodes, customer identity, credentials, and private access details are intentionally excluded from this public report.

## Recording and Publication Permission

At the beginning of the session, the team asked the customer representative for permission to record the meeting and publish a sanitized transcript/summary in the repository. Permission was granted during the recorded session.

## Sprint Review Agenda

1. Confirm recording and publication permission.
2. Explain the Sprint 5 plan and MVP v2 scope.
3. Review product and technical work planned for the Sprint.
4. Discuss algorithm progress and remaining solver risks.
5. Discuss visualization, Gantt schedule, deployment, and validation feedback.
6. Execute customer-facing UAT scenarios during the same session.
7. Record customer feedback and backlog follow-up decisions.

## Sprint Goal Reviewed

The team reviewed the Sprint 5 goal: improve MVP v2 usability and maintainability by working on workload balance, Gantt-style visualization, site bug fixes, solver improvements, column-generation research, automatic deployment, release evidence, and updated project documentation.

## Demonstrated / Discussed Increment

| Area | Related issue | Review result |
|---|---:|---|
| Loader workload balance | #124 | Discussed as an important direction; customer wants to avoid clearly underused loaders. |
| Gantt schedule visualization | #125 | Customer confirmed that a Gantt-style view would be useful, especially for vehicles and loaders. |
| Solver and greedy-stage analysis | #127 | Reviewed. PyVRP + Nevergrad direction was discussed as promising, but one benchmark scenario still needs work. |
| Column-generation research | #128 | Discussed as useful research, but likely too complex for quick implementation in the current Sprint. |
| Product access / deployment | #115, #130 | Customer access was discussed; at the time of the meeting, screen sharing was still the practical access method. |
| Validator behavior | #126 / validator-related flow | Customer confirmed that immediate validation feedback is useful. |
| UAT scenarios | #116 | Executed during the same combined Sprint Review/UAT session. |

## Customer Feedback and Decisions

| Feedback / observation | Decision | Follow-up |
|---|---|---|
| Route visualization becomes overloaded when many routes are shown at once. | Accepted as valid feedback. | Add default filtering, for example show only top-3 longest vehicle routes and/or loader routes by default. |
| Gantt visualization would be useful for vehicles and loaders. | Accepted. | Continue Gantt work; consider selective display for large results. |
| Algorithm work should remain the main focus because the target is to beat the baseline. | Accepted. | Continue solver experiments and benchmark comparison. |
| PyVRP + Nevergrad is a reasonable direction and similar tool combinations are used in optimization competitions. | Accepted as promising direction. | Continue investigation and document measured results. |
| For different problem structures, switching between solver strategies is acceptable and should not be treated as a hack. | Accepted. | Consider solver selection based on problem size/structure instead of scenario ID. |
| Column generation is likely hard to implement quickly and may have many hidden algorithmic issues. | Deferred / research only. | Keep as research spike; consider assignment/covering formulations first. |
| The dashboard should show calculation duration because benchmark runs are limited by time. | Accepted. | Add job finish time or duration column to dashboard/job details. |
| Objective values are too fractional in the dashboard. | Accepted. | Add rounding for displayed objective values. |
| Same seed runs produced inconsistent results during the session. | Not accepted as final behavior. | Investigate solver determinism, concurrent job interference, and time-limit effects. |
| Loader route representation is potentially incorrect: loaders should start from the first assigned order and return to that area/order, not necessarily to the depot. | Accepted as issue/clarification. | Fix route display/semantics for loaders and verify against task requirements. |
| Product access for the customer is still not fully solved. | Open risk. | Continue deployment/access work; use screen sharing until stable access is available. |

## UAT Summary from the Combined Session

The Sprint Review included customer-facing UAT execution. The customer representative observed and interacted with selected workflows while the team recorded actual results.

| Scenario | Public result | Notes |
|---|---|---|
| Create a new optimized route with different seed values | Partially passed / needs follow-up | Different seed values produced different results, but repeated runs with the same seed did not behave consistently enough during the session. The team will investigate solver determinism, concurrency, and time-limit effects. |
| Inspect vehicle and loader route information | Partially passed / needs follow-up | Vehicle route information was visible, but the customer identified a likely issue in how loader starts/returns are represented. |
| Review validation feedback | Passed | Customer confirmed that immediate validator output is useful. |

## Accepted Outcomes

- The customer confirmed that the main Sprint direction should remain algorithm improvement and visualization.
- The customer confirmed that Gantt-style schedules are useful for understanding vehicle and loader activity.
- The customer accepted PyVRP + Nevergrad as a reasonable solver direction.
- The customer accepted solver-strategy switching by problem structure/size as a valid approach.
- The customer confirmed that validator feedback being visible immediately is useful.

## Requested Changes

- Reduce clutter in route visualization through default filtering.
- Add objective value rounding in the dashboard.
- Add calculation duration / finish time to the dashboard or job details.
- Investigate inconsistent results for repeated same-seed runs.
- Fix or clarify loader route representation according to the task requirements.
- Continue work on reliable product access for the customer.

## Deferred Work

- Full column-generation implementation is deferred because it is complex and risky for the current Sprint.
- More advanced route compaction / multi-route vehicle handling remains a solver follow-up.
- Permanent external customer access remains an open deployment/access item if the current access method is not sufficient.

## Backlog Updates

| Follow-up item | Status |
|---|---|
| Route visualization default filter for large results | Add or link to backlog |
| Gantt schedule visualization | Continue under #125 |
| Solver benchmark and greedy-stage investigation | Continue under #127 |
| Column-generation research | Continue under #128 |
| Same-seed reproducibility investigation | Add or link to backlog |
| Dashboard calculation duration | Add or link to backlog |
| Objective value rounding | Add or link to backlog |
| Loader route semantics/display fix | Add or link to backlog |
| Customer-accessible deployment | Continue under #115 / #130 |

## Review Conclusion

The Sprint 5 Review was conducted as a combined Sprint Review and UAT session. The customer reviewed the Sprint direction, discussed MVP v2 product behavior, executed/observed UAT workflows, and provided feedback. Several outcomes were accepted, while seed reproducibility, loader route representation, dashboard improvements, visualization filtering, and access/deployment remain follow-up work.

# Week 6 Report — Transition-Readiness Meeting & Sprint Review

## Project Overview

**Project:** Route Optimization Platform
**Team:** Team 9
**Short description:** A logistics optimization platform for generating, validating, and reviewing vehicle and loader routes for the BIA CVRPTW problem variant.

## Assignment 6 Evidence Index

| Requirement area | Public evidence |
|---|---|
| Product Backlog board/view | [Product Backlog](https://github.com/orgs/Team-9-swp/projects/1/views/1) |
| Sprint Backlog board/view | [Team GitHub Project](https://github.com/orgs/Team-9-swp/projects/1) |
| Sprint 4 milestone | [Sprint 4 — Week 6 Trial Release and Transition Readiness](https://github.com/Team-9-swp/Route-optimization-Platform-swp/milestone/8) |
| Sprint 4 planning | [Roadmap](../../docs/roadmap.md) |
| Project entry points | [README](../../README.md), [CONTRIBUTING](../../CONTRIBUTING.md), [AGENTS](../../AGENTS.md) |
| Hosted documentation | [Documentation site](https://team-9-swp.github.io/Route-optimization-Platform-swp/) |
| Customer feedback response | [Customer Feedback Response](#customer-feedback-response) |
| Development process | [Development process](../../docs/development-process.md) |
| Architecture views | [Architecture documentation](../../docs/architecture/README.md) |
| ADRs | [ADR index](../../docs/architecture/adr/README.md) |
| Testing / QA / DoD | [Testing strategy](../../docs/testing.md), [Definition of Done](../../docs/definition-of-done.md) |
| Quality requirements | [Quality requirements](../../docs/quality-requirements.md) |
| Quality requirement tests | [Quality requirement tests](../../docs/quality-requirement-tests.md) |
| UAT | [User Acceptance Tests](../../docs/user-acceptance-tests.md) |
| Sprint Review summary | [Sprint 4 Review Summary](sprint-review-summary.md) |
| Sprint Review transcript | [Sanitised Sprint Review Transcript](sprint-review-transcript.md) |
| Retrospective | [Retrospective](retrospective.md) |
| Reflection | [Reflection](reflection.md) |
| LLM usage | [LLM usage report](llm-report.md) |
| Customer handover | [Customer Handover](../../docs/customer-handover.md) |
| Changelog | [CHANGELOG.md](../../CHANGELOG.md) |

## Sprint Goal, Dates, and Scope

**Sprint:** Sprint 4 — Week 6 Trial Release and Transition Readiness
**Sprint dates:** 2026-07-06 — 2026-07-12
**Total Sprint size:** ~52 Story Points

**Sprint Goal:** Deliver a stable Week 6 trial / handover candidate that the customer and TA can access, review the customer-facing documentation, execute UAT, discuss transition readiness, and identify follow-up work for Week 7.

**Scope summary:** Sprint 4 focused on algorithm determinism fix, baseline comparison, driver return-to-depot, Gantt chart visualisation, manual time limit, transition-readiness meeting with the customer, and customer deployment planning.

## Delivered Sprint 4 Changes

- Algorithm determinism fixed (seed 42 passed to Nevergrad).
- Baseline beaten on test case 4 (~0.5% improvement).
- Driver return-to-depot implemented.
- Manual time limit feature implemented.
- Gantt chart visualisation completed ([#163](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/163)).
- Transition-readiness meeting conducted with customer.
- Customer deployment plan confirmed (self-deploy from protected `main` in Week 7; not completed yet).
- Customer handover documentation updated.

## Product Access and Run Instructions

Public product repository:

- [Route Optimization Platform repository](https://github.com/Team-9-swp/Route-optimization-Platform-swp)

Current public run/access instructions:

- [Root README run instructions](../../README.md)
- [Deployment documentation](../../docs/deployment.md)
- [Customer handover documentation](../../docs/customer-handover.md)

Private access details, exact deployment access instructions, credentials, recording links, and exact timecodes are submitted through Moodle only.

## Customer Feedback Response

Public sources reviewed:

- [Week 6 Sprint Review transcript](sprint-review-transcript.md)
- [Week 6 Sprint Review summary](sprint-review-summary.md)
- [User acceptance tests](../../docs/user-acceptance-tests.md)
- [Roadmap](../../docs/roadmap.md)

Private recording links, customer identity, credentials, exact timecodes, and private access details are intentionally excluded from this public report.

| Feedback point | Resulting PBI or issue | Status | Response |
|---|---|---|---|
| Algorithm is now deterministic and baseline performance improved. | [#166](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/166) | Done | Fixed-seed behavior and the test-case improvement were reviewed; independent customer verification remains planned. |
| Driver return-to-depot creates a minor cost-calculation edge case. | Follow-up action tracked in Week 7 planning | Deferred | Validator / fuel calculation for routes split by zeros requires follow-up in Sprint 5. |
| Customer wants full UI deployment, not just algorithm. | [#162](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/162) | Done | Deploy via single container with interface. |
| Customer to deploy independently from protected `main`. | [#162](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/162) | Planned — Week 7 | Customer-side deployment has not happened yet. |
| Gantt chart visualisation. | [#163](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/163) | Done | PBI and implementation are complete. |
| Manual solver time limit. | [#171](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/171) | Done | Control is available on the New Job page. |
| Customer may have limited network access next week; use Zoom. | — | Accepted | Use Zoom for Week 7 meeting. |

## Customer-Facing Documentation Review

During the Week 6 transition-readiness meeting, the customer provided implicit feedback on the customer-facing documentation set through the discussion. An explicit documentation walkthrough was not conducted during this meeting; it is planned for Week 7.

| Documentation area | Customer signal from transcript | Assessment |
|---|---|---|
| Repository transparency | Customer: *"I hope everything is transparent. And I'll be able to do everything independently, without additional consultations, and deploy it."* | Positive — customer trusts the repository is transparent enough for independent work. |
| Deployment model | Customer: *"I'll deploy it and try then during next week"* and *"spin everything up through a single container without any shamanism"* | Positive — customer understands the single-container deployment model. |
| Delivery format | Customer: *"With a wrapper, of course"* (full UI, not algorithm-only) | Positive — customer confirmed full UI delivery expectation. |
| Branch/release guidance | Customer requested a stable source pointer for independent use. | Partially addressed — protected `main` is the source branch; the Week 6 / final release is pending until final fixes are ready. |
| Deployment instructions | Customer asked: *"how does that happen?"* regarding service transfer | Gap — deployment instructions in `docs/customer-handover.md` and `docs/deployment.md` could be clearer for first-time deployers. |
| Acceptance criteria | Customer: *"after deployment, will it be enough just to say the words I say? Or do I need to record something again?"* | Partially addressed — team confirmed verbal acceptance is sufficient, but formal acceptance criteria could be documented more clearly. |

**Planned action:** Conduct an explicit customer-facing documentation review during the Week 7 meeting, asking the customer to walk through `README.md`, `docs/customer-handover.md`, and `docs/deployment.md` specifically.

## Transition-Readiness Summary

The Week 6 meeting confirmed the following transition-readiness status:

**What is ready:**
- Algorithm is deterministic and beats the baseline on test case 4.
- Full UI deployment model confirmed (single container with interface).
- Customer plans to self-deploy from protected `main` in Week 7.
- Customer has repository access and understands the deployment process.

**What must happen in Week 7:**
1. Customer to deploy independently from protected `main` and verify the deployment works.
2. Customer to run the algorithm from sources and verify against baseline results.
3. Customer to run the algorithm through the web interface and verify consistency with source-level runs.
4. Validate the completed Gantt chart during customer-side testing.
5. Fix the validator / fuel calculation / driver return-to-depot cost edge case (routes split by zeros).
6. Conduct explicit customer-facing documentation review.
7. Use Zoom for the Week 7 meeting due to customer network limitations.

**Handover level:** `Ready for independent use` — customer has not yet deployed or operated the product on their side; self-deployment is planned for Week 7.

## Feedback Not Addressed in Sprint 4

| Feedback / item | Reason |
|---|---|
| Driver return-to-depot cost-calculation fix | Deferred to Sprint 5 — minor edge case identified during Sprint Review. |
| Additional solver improvements | Deferred to Sprint 5 — planned for next iteration. |
| Permanent external product access | Private access details are submitted through Moodle only. |

## Architecture Summary

The Sprint 4 architecture remains consistent with MVP v2: React frontend, FastAPI backend, PostgreSQL persistence, PyVRP/Nevergrad solver, hard-constraint validator, Docker Compose packaging, and GitHub Actions workflows.

Key Sprint 4 changes: determinism fix (seed 42 passed to Nevergrad), driver return-to-depot in solver output, manual time-limit control, and completed Gantt chart visualisation.

## Architecture and Quality Traceability

Quality requirements are linked to architecture decisions through:

- solver functional correctness and deterministic behaviour (QR-FC-01);
- time behaviour and benchmark-aware solver execution (QR-TB-01);
- recoverability through PostgreSQL-backed persistence (QR-RE-01);
- safe error handling and public-response confidentiality (QR-SE-01);
- deployment reliability through protected-main CI/CD and release evidence.

Relevant architecture and decision records:

- [Architecture documentation](../../docs/architecture/README.md)
- [ADR index](../../docs/architecture/adr/README.md)
- [Quality requirements](../../docs/quality-requirements.md)
- [Quality requirement tests](../../docs/quality-requirement-tests.md)

## Testing and CI Status

Public testing and quality evidence:

- [Testing strategy](../../docs/testing.md)
- [Definition of Done](../../docs/definition-of-done.md)
- [Quality requirements](../../docs/quality-requirements.md)
- [Quality requirement tests](../../docs/quality-requirement-tests.md)
- [CI pipeline](https://github.com/Team-9-swp/Route-optimization-Platform-swp/actions/workflows/ci.yml)
- [Latest protected-main CI runs](https://github.com/Team-9-swp/Route-optimization-Platform-swp/actions?query=branch%3Amain)

## Sprint Review

- [Sprint 4 Review Summary](sprint-review-summary.md)
- [Sanitised Sprint Review Transcript](sprint-review-transcript.md)

The Sprint Review was conducted as a transition-readiness meeting with the customer. The public repository contains sanitised English evidence only. Private recording links, exact timecodes, recording permission evidence, customer identity, credentials, and private access details are submitted through Moodle only.

## Deferred and Follow-up Work

| Item | Issue | Sprint 4 decision |
|---|---|---|
| Validator / fuel calculation / driver return-to-depot cost edge case | Follow-up action tracked in Week 7 planning | Deferred to Sprint 5. |
| Additional solver improvements | — | Deferred to Sprint 5. |
| Permanent external product access | — | Private access details submitted through Moodle only. |

## Current Product Status

Sprint 4 work described by this report is complete except for explicitly deferred items. The algorithm is deterministic and beats the baseline on test case 4, and the Gantt visualisation and manual time-limit control are complete. Customer-side deployment is planned from protected `main` in Week 7. The Week 6 / final release is pending and will be created only after the remaining final fixes are ready.

## Next Steps

- Customer to deploy independently from protected `main` in Week 7.
- Customer to run the algorithm from sources and verify against baseline.
- Customer to run the algorithm through the web interface and verify consistency.
- Validate the completed Gantt chart during Week 7 customer-side testing.
- Address driver return-to-depot cost-calculation edge case in Sprint 5.
- Use Zoom for Week 7 meeting due to customer network limitations.

## Contribution Traceability

| Team member | Assignment 6 responsibility | Issues / evidence | Technical / process contribution |
|---|---|---|---|
| Elvina | Parts 1, 2, 9, Week 6 report | Sprint Review evidence, Week 6 reporting | Sprint planning, customer feedback traceability, Sprint Review evidence |
| Adelia | Parts 7, 10, 11, 12, 13, 14 | Retrospective, reflection, LLM report | Release support, retrospective, reflection, LLM report |
| Matvey | Part 6 | Testing, QA, Definition of Done | Testing, QA, quality evidence |
| Aidar | Part 8 | UAT scenarios, transition-readiness meeting | UAT scenarios, customer-facing validation, transition planning |
| Valera | Parts 3, 4, 5 | Algorithm determinism, solver improvements | Algorithm fixes, solver optimisation, technical deep-dive |

## Screenshots

Screenshots are submitted through Moodle or will be added before final submission. No private evidence or placeholder image links are included in this public report.

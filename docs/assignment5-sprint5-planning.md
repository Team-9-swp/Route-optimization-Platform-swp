# Assignment 5 Sprint 5 Planning Artifacts

This file contains the prepared GitHub metadata used for Assignment 5 Part 1. Verify live GitHub milestone, issue, and Project state before using it as submission evidence.

## Milestone

Title: `Sprint 5 — MVP v2`

Due date: `2026-07-05`

Description:

```md
## Sprint

Assignment 5 — Sprint 5

## Sprint dates

- Start: 2026-06-29
- Finish: 2026-07-05

## Sprint Goal

Deliver MVP v2 with improved solution usability and maintainability by fixing validator-compatible JSON export, improving loader workload distribution, adding Gantt schedule visualization, investigating stronger optimization approaches, documenting the architecture and development process, and automating deployment from the protected main branch.

## Planned outcome

A customer-accessible MVP v2 increment with selected product improvements, updated architecture and development-process documentation, extended testing and CI evidence, hosted documentation, UAT evidence, Sprint Review evidence, and a SemVer release from the protected default branch.
```

## Selected PBIs

| Title | Implementer | Reviewer | SP | Priority |
|---|---|---|---:|---|
| A5-01: Refine Product Backlog and plan Sprint 5 | `belelvser` | `Adelevere` | 3 | Must Have |
| A5-02: Trace and respond to MVP v1 customer feedback | `belelvser` | `Adelevere` | 2 | Must Have |
| A5-03: Document development process and configuration management | `whateverwillbewillbe` | `FuFill` | 3 | Must Have |
| A5-04: Document static, dynamic, and deployment architecture views | `whateverwillbewillbe` | `Aydar-art` | 5 | Must Have |
| A5-05: Create and link Architecture Decision Records | `whateverwillbewillbe` | `FuFill` | 3 | Must Have |
| A5-06: Extend testing, QA, and Definition of Done for MVP v2 | `FuFill` | `whateverwillbewillbe` | 5 | Must Have |
| A5-07: Deploy and release MVP v2 | `FuFill` | `whateverwillbewillbe` | 5 | Must Have |
| A5-08: Update and execute MVP v2 UAT scenarios | `Aydar-art` | `FuFill` | 3 | Must Have |
| A5-09: Conduct Sprint 5 Review | `Aydar-art` | `belelvser` | 3 | Must Have |
| A5-10: Conduct Sprint Retrospective | `Adelevere` | `belelvser` | 2 | Must Have |
| A5-11: Publish hosted documentation | `Adelevere` | `whateverwillbewillbe` | 3 | Must Have |
| A5-12: Write Week 5 reflection | `Adelevere` | `belelvser` | 2 | Must Have |
| A5-13: Record public MVP v2 demo video | `Adelevere` | `FuFill` | 2 | Must Have |
| A5-14: Prepare Assignment 5 LLM usage report | `Adelevere` | `belelvser` | 1 | Must Have |
| A5-15: Prepare Week 5 public report and Moodle report | `belelvser` | `Adelevere` | 3 | Must Have |
| Improve loader workload balance | `Aydar-art` | `FuFill` | 5 | Must Have |
| Add Gantt schedule visualization | `FuFill` | `Aydar-art` | 5 | Must Have |
| Export validator-compatible solution JSON | `whateverwillbewillbe` | `FuFill` | 3 | Must Have |
| Re-evaluate solver pipeline and greedy-stage impact | `FuFill` | `Aydar-art` | 8 | Should Have |
| Investigate column generation for route optimization | `Aydar-art` | `FuFill` | 5 | Could Have |
| Fix the known product bug | `whateverwillbewillbe` | `Aydar-art` | 3 | Must Have |
| Configure automatic deployment from protected main | `whateverwillbewillbe` | `FuFill` | 5 | Must Have |

Total: 22 PBIs, 79 Story Points.

## Issue Bodies

### A5-01: Refine Product Backlog and plan Sprint 5

```md
## Type

Assignment 5 PBI

## Expected outcome

The Product Backlog is refined, Sprint 5 is planned for MVP v2, and selected PBIs are traceable through GitHub Issues, the Sprint 5 milestone, the GitHub Project, and `docs/roadmap.md`.

## Acceptance criteria

- [ ] Sprint 5 milestone contains dates, Sprint Goal, and selected PBIs.
- [ ] Every selected PBI has outcome, acceptance criteria, Story Points, implementer, different reviewer, priority, MVP version, and Work Status.
- [ ] Sprint 5 Backlog view contains all milestone issues.
- [ ] `docs/roadmap.md` describes Sprint 5, MVP v2, and expected next work.

## Story Points

3

## Priority

Must Have

## MVP version

MVP v2

## Implementer

@belelvser

## Reviewer

@Adelevere

## Work Status

To Do

## Sprint

Sprint 5 — MVP v2
```

### A5-02: Trace and respond to MVP v1 customer feedback

```md
## Type

Assignment 5 PBI

## Expected outcome

Customer feedback from MVP v1 and Assignment 4 is reviewed, linked to Sprint 5 scope or deferred with rationale, and reflected in the Week 5 report.

## Acceptance criteria

- [ ] Available MVP v1 and Assignment 4 feedback is reviewed before Sprint 5 implementation decisions are finalized.
- [ ] Feedback selected for MVP v2 is linked to Sprint 5 PBIs.
- [ ] Deferred feedback has a documented reason and follow-up backlog link where useful.
- [ ] Week 5 public or Moodle evidence contains a feedback response table without exposing private data.

## Story Points

2

## Priority

Must Have

## MVP version

MVP v2

## Implementer

@belelvser

## Reviewer

@Adelevere

## Work Status

To Do

## Sprint

Sprint 5 — MVP v2
```

### A5-03: Document development process and configuration management

```md
## Type

Assignment 5 PBI

## Expected outcome

The repository documents the maintained development workflow and configuration-management rules used for MVP v2.

## Acceptance criteria

- [ ] Development-process documentation describes branch, issue, review, CI, and release workflow.
- [ ] Configuration-management documentation covers environment variables, Docker configuration, dependencies, migrations, and secret handling.
- [ ] Required evidence and traceability locations are documented.
- [ ] Documentation avoids private credentials and private customer information.

## Story Points

3

## Priority

Must Have

## MVP version

MVP v2

## Implementer

@whateverwillbewillbe

## Reviewer

@FuFill

## Work Status

To Do

## Sprint

Sprint 5 — MVP v2
```

### A5-04: Document static, dynamic, and deployment architecture views

```md
## Type

Assignment 5 PBI

## Expected outcome

The architecture documentation explains MVP v2 through static, dynamic, and deployment views that match the implemented system.

## Acceptance criteria

- [ ] Static view describes main backend, frontend, database, solver, validator, and deployment components.
- [ ] Dynamic view covers the solve/export/validate workflow and the deployment workflow.
- [ ] Deployment view shows Docker-based services, protected-main CI, deployment target, and external access boundaries.
- [ ] Architecture views are linked from the documentation index and reviewed by a different team member.

## Story Points

5

## Priority

Must Have

## MVP version

MVP v2

## Implementer

@whateverwillbewillbe

## Reviewer

@Aydar-art

## Work Status

To Do

## Sprint

Sprint 5 — MVP v2
```

### A5-05: Create and link Architecture Decision Records

```md
## Type

Assignment 5 PBI

## Expected outcome

At least three Architecture Decision Records document important MVP v2 technical decisions and are linked to the architecture documentation.

## Acceptance criteria

- [ ] At least three ADRs are added under a maintained ADR location.
- [ ] Each ADR has context, decision, consequences, and status.
- [ ] ADRs cover meaningful MVP v2 architecture, deployment, solver, or documentation decisions.
- [ ] Architecture documentation links to the ADRs.

## Story Points

3

## Priority

Must Have

## MVP version

MVP v2

## Implementer

@whateverwillbewillbe

## Reviewer

@FuFill

## Work Status

To Do

## Sprint

Sprint 5 — MVP v2
```

### A5-06: Extend testing, QA, and Definition of Done for MVP v2

```md
## Type

Assignment 5 PBI

## Expected outcome

Testing, QA documentation, and Definition of Done are updated so MVP v2 changes have clear quality expectations and evidence.

## Acceptance criteria

- [ ] MVP v2 test strategy identifies required unit, integration, frontend, UAT, and regression coverage.
- [ ] Definition of Done includes validation, review, documentation, CI, and release expectations for Sprint 5.
- [ ] New product PBIs identify required automated or UAT coverage.
- [ ] CI and QA evidence locations are documented without inventing test results.

## Story Points

5

## Priority

Must Have

## MVP version

MVP v2

## Implementer

@FuFill

## Reviewer

@whateverwillbewillbe

## Work Status

To Do

## Sprint

Sprint 5 — MVP v2
```

### A5-07: Deploy and release MVP v2

```md
## Type

Assignment 5 PBI

## Expected outcome

MVP v2 is deployed from protected `main`, verified, documented, and published as a SemVer release.

## Acceptance criteria

- [ ] Deployment uses a protected `main` commit after required CI checks pass.
- [ ] Customer-accessible deployment or agreed access method is documented.
- [ ] Release notes link the Sprint 5 milestone, relevant evidence, and changelog entry.
- [ ] No private credentials, private access details, or private recording links are published.

## Story Points

5

## Priority

Must Have

## MVP version

MVP v2

## Implementer

@FuFill

## Reviewer

@whateverwillbewillbe

## Work Status

To Do

## Sprint

Sprint 5 — MVP v2
```

### A5-08: Update and execute MVP v2 UAT scenarios

```md
## Type

Assignment 5 PBI

## Expected outcome

MVP v2 UAT scenarios are updated, executed with customer-relevant workflows, and linked to sanitized evidence.

## Acceptance criteria

- [ ] UAT scenarios cover selected MVP v2 product changes.
- [ ] Expected results and actual results are recorded.
- [ ] Defects or follow-up feedback are linked to backlog items.
- [ ] Public evidence is sanitized and private evidence is kept only in approved private submission locations.

## Story Points

3

## Priority

Must Have

## MVP version

MVP v2

## Implementer

@Aydar-art

## Reviewer

@FuFill

## Work Status

To Do

## Sprint

Sprint 5 — MVP v2
```

### A5-09: Conduct Sprint 5 Review

```md
## Type

Assignment 5 PBI

## Expected outcome

Sprint 5 Review is conducted with MVP v2 evidence, customer feedback, and backlog follow-up decisions.

## Acceptance criteria

- [ ] Sprint Review agenda and demonstrated scope are documented.
- [ ] Customer or stakeholder feedback is recorded with sanitized public notes.
- [ ] Accepted, rejected, and deferred outcomes are linked to Sprint 5 PBIs or future backlog items.
- [ ] Review evidence is linked from the Week 5 report.

## Story Points

3

## Priority

Must Have

## MVP version

MVP v2

## Implementer

@Aydar-art

## Reviewer

@belelvser

## Work Status

To Do

## Sprint

Sprint 5 — MVP v2
```

### A5-10: Conduct Sprint Retrospective

```md
## Type

Assignment 5 PBI

## Expected outcome

The team conducts a Sprint Retrospective and records actionable improvement items for future work.

## Acceptance criteria

- [ ] Retrospective notes summarize what went well, what was difficult, and what to improve.
- [ ] Action items have owners or follow-up locations.
- [ ] Private or sensitive discussion is not published.
- [ ] Retrospective summary is linked from Week 5 evidence.

## Story Points

2

## Priority

Must Have

## MVP version

MVP v2

## Implementer

@Adelevere

## Reviewer

@belelvser

## Work Status

To Do

## Sprint

Sprint 5 — MVP v2
```

### A5-11: Publish hosted documentation

```md
## Type

Assignment 5 PBI

## Expected outcome

Project documentation is hosted and publicly accessible without exposing private data.

## Acceptance criteria

- [ ] Documentation site builds from repository documentation sources.
- [ ] Hosted documentation link is public and verified.
- [ ] Architecture, development-process, testing, ADR, deployment, and user-facing evidence pages are reachable.
- [ ] Hosting instructions or workflow are documented.

## Story Points

3

## Priority

Must Have

## MVP version

MVP v2

## Implementer

@Adelevere

## Reviewer

@whateverwillbewillbe

## Work Status

To Do

## Sprint

Sprint 5 — MVP v2
```

### A5-12: Write Week 5 reflection

```md
## Type

Assignment 5 PBI

## Expected outcome

Week 5 reflection documents team learning, contribution, process observations, and responsible use of tools.

## Acceptance criteria

- [ ] Reflection covers Sprint 5 planning, implementation, quality, deployment, and teamwork.
- [ ] Individual or team contributions are described accurately.
- [ ] Reflection does not claim unverified work as complete.
- [ ] Reflection is linked from Week 5 public or Moodle report as appropriate.

## Story Points

2

## Priority

Must Have

## MVP version

MVP v2

## Implementer

@Adelevere

## Reviewer

@belelvser

## Work Status

To Do

## Sprint

Sprint 5 — MVP v2
```

### A5-13: Record public MVP v2 demo video

```md
## Type

Assignment 5 PBI

## Expected outcome

A public sanitized demo video shows the MVP v2 increment and is linked from Week 5 evidence.

## Acceptance criteria

- [ ] Demo covers selected MVP v2 features and workflow.
- [ ] Recording contains no private credentials, customer private data, or private access links.
- [ ] Public video link is verified before submission.
- [ ] Demo is linked from the Week 5 public report and release evidence where appropriate.

## Story Points

2

## Priority

Must Have

## MVP version

MVP v2

## Implementer

@Adelevere

## Reviewer

@FuFill

## Work Status

To Do

## Sprint

Sprint 5 — MVP v2
```

### A5-14: Prepare Assignment 5 LLM usage report

```md
## Type

Assignment 5 PBI

## Expected outcome

Assignment 5 LLM usage is documented transparently with prompts, outputs, human decisions, and limitations.

## Acceptance criteria

- [ ] LLM usage report identifies where LLM tools were used.
- [ ] Important prompts, generated outputs, and human validation steps are summarized.
- [ ] The report distinguishes completed work from suggestions or drafts.
- [ ] No private credentials, tokens, or private customer data are included.

## Story Points

1

## Priority

Must Have

## MVP version

MVP v2

## Implementer

@Adelevere

## Reviewer

@belelvser

## Work Status

To Do

## Sprint

Sprint 5 — MVP v2
```

### A5-15: Prepare Week 5 public report and Moodle report

```md
## Type

Assignment 5 PBI

## Expected outcome

Week 5 public and Moodle reports index all required evidence, final links, and contribution traceability for Assignment 5.

## Acceptance criteria

- [ ] `reports/week5/README.md` indexes all applicable public evidence.
- [ ] Required screenshots are stored under `reports/week5/images/`.
- [ ] Contribution traceability is documented.
- [ ] Moodle report contains final commit-hash permalinks and private evidence links.
- [ ] Public and private links are verified before submission.

## Story Points

3

## Priority

Must Have

## MVP version

MVP v2

## Implementer

@belelvser

## Reviewer

@Adelevere

## Work Status

To Do

## Sprint

Sprint 5 — MVP v2
```

### Improve loader workload balance

```md
## Type

Assignment 5 PBI

## Expected outcome

Loader assignments avoid clearly underused workers, including solutions where an assigned loader performs approximately one hour of work while comparable loaders are substantially more loaded.

## Acceptance criteria

- [ ] A workload-balance metric is explicitly defined.
- [ ] Current behavior is reproduced on a committed sanitized test scenario.
- [ ] Solver logic includes an appropriate constraint, penalty, or assignment improvement.
- [ ] Result remains valid according to the project validator.
- [ ] Before/after workload distribution is documented.
- [ ] Automated regression tests are added.

## Story Points

5

## Priority

Must Have

## MVP version

MVP v2

## Implementer

@Aydar-art

## Reviewer

@FuFill

## Work Status

To Do

## Sprint

Sprint 5 — MVP v2
```

### Add Gantt schedule visualization

```md
## Type

Assignment 5 PBI

## Expected outcome

Users can inspect vehicle, driver, loader, and job timing through a Gantt-style visualization.

## Acceptance criteria

- [ ] Backend or result schema exposes required start/end timing data.
- [ ] Frontend renders scheduled activities on a timeline.
- [ ] Resources and activity types are distinguishable.
- [ ] Empty, failed, and large-result states are handled.
- [ ] Frontend typecheck and production build pass.
- [ ] The feature is covered by a new UAT scenario.

## Story Points

5

## Priority

Must Have

## MVP version

MVP v2

## Implementer

@FuFill

## Reviewer

@Aydar-art

## Work Status

To Do

## Sprint

Sprint 5 — MVP v2
```

### Export validator-compatible solution JSON

```md
## Type

Assignment 5 PBI

## Expected outcome

A solution JSON downloaded from the web interface can be passed directly to the project validator without manual editing.

## Acceptance criteria

- [ ] The current incompatibility is reproduced and documented.
- [ ] Exported field names, types, nesting, and identifiers match validator expectations.
- [ ] UI-only fields do not break validation.
- [ ] A solve/export/validate integration test is added.
- [ ] A downloaded solution validates successfully on a sanitized scenario.

## Story Points

3

## Priority

Must Have

## MVP version

MVP v2

## Implementer

@whateverwillbewillbe

## Reviewer

@FuFill

## Work Status

To Do

## Sprint

Sprint 5 — MVP v2
```

### Re-evaluate solver pipeline and greedy-stage impact

```md
## Type

Assignment 5 PBI

## Expected outcome

The team measures how the greedy stage affects solution quality and determines whether a more joint optimization approach should replace or modify the current pipeline.

## Historical context

Closed issues #23 and #97 are related historical context only. They must not be reopened, reused, or modified for Assignment 5.

## Acceptance criteria

- [ ] Current solver stages and fixed decisions are documented.
- [ ] A reproducible baseline with fixed scenarios and seeds is created.
- [ ] Current greedy behavior is compared with at least one modified alternative.
- [ ] Objective value, validity, runtime, skipped orders, and loader balance are compared.
- [ ] Findings and recommended next action are documented.
- [ ] Any production change has automated regression coverage.

## Story Points

8

## Priority

Should Have

## MVP version

MVP v2

## Implementer

@FuFill

## Reviewer

@Aydar-art

## Work Status

To Do

## Sprint

Sprint 5 — MVP v2
```

### Investigate column generation for route optimization

```md
## Type

Assignment 5 PBI

## Expected outcome

The team determines whether column generation is appropriate for the current CVRPTW variant. This is a research spike, not a guaranteed production implementation.

## Acceptance criteria

- [ ] Master problem and pricing problem are described for the project domain.
- [ ] Integration boundaries with the current solver are identified.
- [ ] A small prototype or executable experiment is produced where feasible.
- [ ] Results are compared on small sanitized scenarios.
- [ ] Limitations and implementation cost are documented.
- [ ] An ADR records the decision as Accepted, Proposed, Rejected, or Deferred.

## Story Points

5

## Priority

Could Have

## MVP version

MVP v2

## Implementer

@Aydar-art

## Reviewer

@FuFill

## Work Status

To Do

## Sprint

Sprint 5 — MVP v2
```

### Fix the known product bug

```md
## Type

Assignment 5 PBI

## Expected outcome

The known product bug is identified with reproduction details, fixed, and protected by regression testing.

## Acceptance criteria

- [ ] Reproduction steps and sanitized input are documented before implementation starts.
- [ ] Expected behavior and actual behavior are described.
- [ ] A failing regression test is added before or with the fix.
- [ ] The root cause is fixed.
- [ ] Relevant CI checks pass.

## Story Points

3 (provisional until the bug is reproduced)

## Priority

Must Have

## MVP version

MVP v2

## Implementer

@whateverwillbewillbe

## Reviewer

@Aydar-art

## Work Status

To Do

## Sprint

Sprint 5 — MVP v2
```

### Configure automatic deployment from protected main

```md
## Type

Assignment 5 PBI

## Expected outcome

A successful protected-`main` CI run automatically deploys the current product increment.

## Acceptance criteria

- [ ] Deployment runs only after required CI checks pass on `main`.
- [ ] Credentials and keys are stored in GitHub Secrets or another approved secret store.
- [ ] Deployment updates the Docker-based application and runs required migrations.
- [ ] A post-deployment health check verifies the API.
- [ ] Failed deployment is visible in GitHub Actions.
- [ ] Deployment and rollback or recovery instructions are documented.
- [ ] Deployment architecture documentation reflects the workflow.

## Story Points

5

## Priority

Must Have

## MVP version

MVP v2

## Implementer

@whateverwillbewillbe

## Reviewer

@FuFill

## Work Status

To Do

## Sprint

Sprint 5 — MVP v2
```

## Totals

Story Points by implementer:

- `belelvser`: 8
- `Adelevere`: 10
- `Aydar-art`: 16
- `FuFill`: 23
- `whateverwillbewillbe`: 22

Story Points by priority:

- Must Have: 66
- Should Have: 8
- Could Have: 5

## Project Setup Notes

- Product Backlog view: <https://github.com/orgs/Team-9-swp/projects/1/views/1>
- Existing Sprint Backlog view: <https://github.com/orgs/Team-9-swp/projects/1/views/3>
- Required new view: `Sprint 5 Backlog`
- Required filter: `milestone:"Sprint 5 — MVP v2"`
- Required visible fields: Title, Status, Priority or MoSCoW, Story Points, Assignee, MVP Version, Milestone.
- Existing Project fields include `Status`, `Story Points`, `MVP Version`, and `MoSCoW`; do not create duplicate equivalent fields.
- Existing Status option is named `To do` in GitHub Project, while issue bodies and labels use `To Do`.
- The currently available repository token does not include Project scopes, so Project field values and the Sprint 5 Backlog view must be completed by a user with GitHub Project edit access.

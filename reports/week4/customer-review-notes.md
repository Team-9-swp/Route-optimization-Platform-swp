# Customer Review Notes

**Meeting date:** 26 June 2026

**Participants:** Customer representative and project team members

**Recording status:** The meeting took place, but the recording was not saved because of a technical recording failure. These sanitized notes were reconstructed immediately after the meeting from team notes.

**Publication status:** These notes contain no personal names, credentials, private links, or confidential business information.

## Sprint Goal reviewed

The planned Sprint Goal was to improve the reliability and verifiability of the Route Optimization Platform by addressing selected customer feedback, improving persistence and solver robustness, defining measurable quality requirements, and adding automated quality gates.

The complete Sprint increment was not presented as finished during this meeting.

## Delivered increment discussed

The discussion covered:

- the current route optimization platform;
- the existing Docker-based run method;
- the university VM deployment;
- current solver behaviour;
- planned quality requirements and automated quality verification.

Unfinished Assignment 4 features were not recorded as completed demonstrations.

## Deployment and customer access

The customer could not open the hosted website because the university VM deployment was reachable only from the Innopolis University network, while the customer was outside Innopolis.

The project can be run locally using Docker. Docker was discussed as a temporary fallback.

The team agreed to investigate:

- external access to the hosted application; or
- another explicitly agreed remote access method.

Customer access must be verified before the follow-up UAT session.

## UAT results

Customer-executed UAT was not completed during this meeting because the customer could not access the hosted product.

Therefore:

- no UAT scenario should be marked Passed based on this meeting;
- the current increment was not accepted by the customer through UAT;
- a follow-up recorded session is required after customer access is available.

## Addressed customer feedback

The team discussed previous customer requests related to:

- route-result visibility;
- calculation history and persistence;
- solver execution time;
- solution quality relative to the baseline;
- customer access to the deployed application.

The corresponding backlog work is tracked through [#13](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/13), [#23](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/23), [#85](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/85), [#87](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/87), [#88](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/88), [#90](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/90), and [#97](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/97).

## Quality requirements and automated quality evidence

The team has prepared or is preparing quality requirements covering:

- solver functional correctness;
- solver time behaviour;
- recoverability of stored jobs;
- safe API error handling.

At the time of this meeting:

- final automated QRT implementations were not demonstrated;
- final protected-default-branch CI evidence was not demonstrated;
- no claim should be made that all quality gates passed.

The final quality evidence must be shown during the follow-up Sprint Review or linked from the completed Week 4 report.

## Customer feedback

The customer requested or recommended:

1. Compare the current solver with the baseline using the same selected scenarios, inputs, runtime limits, and metrics.
2. Investigate whether the greedy stage causes weaker objective values.
3. Consider a more joint optimization approach for vehicle routes, loader assignments, and optional-order decisions.
4. Provide accessible product access outside the university network or agree on another remote access method.

## Decisions

- Deployment accessibility is an immediate blocker for customer UAT.
- Docker remains a temporary fallback access method.
- Baseline comparison and greedy-stage analysis are tracked in [#97](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/97).
- Broader joint optimization remains part of solver investigation under [#23](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/23).
- UAT and final Sprint Review evidence must be completed in a follow-up recorded session.
- [#87](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/87) records quality requirement and QRT specifications; [#88](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/88) remains open until QRT implementation and CI evidence are complete.

## Remaining gaps and risks

- The customer cannot currently access the hosted product outside the university network.
- Customer-executed UAT is incomplete.
- Final Assignment 4 increment evidence is incomplete.
- Automated QRT and protected-branch CI evidence is incomplete.
- The current solver architecture may lose solution quality by optimizing major components mainly in sequence.
- [#97](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/97) still requires actual baseline measurements.

## Resulting Product Backlog updates

- [#90](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/90) was updated with external or agreed remote access, Docker fallback, and pre-UAT access verification criteria.
- [#23](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/23) contains the new joint-optimization and solver-quality feedback.
- [#97](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/97) tracks baseline comparison and greedy-stage analysis.
- [#91](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/91) remains open until customer-executed UAT is completed.
- [#92](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/92) remains open until the follow-up Sprint Review and all required review evidence are complete.

## Required follow-up Sprint Review

Conduct a short recorded follow-up session after the customer can access the product.

The follow-up must cover:

1. recording permission before recording starts;
2. planned Sprint Goal;
3. delivered Sprint increment;
4. addressed customer feedback;
5. customer execution of at least three UAT scenarios;
6. UAT results;
7. quality requirements;
8. automated QRT results;
9. latest protected-main CI evidence;
10. quality gates that must continue into later work;
11. remaining gaps and risks;
12. resulting Product Backlog changes.

Record exact Moodle-only timestamps for the UAT and Sprint Review sections.

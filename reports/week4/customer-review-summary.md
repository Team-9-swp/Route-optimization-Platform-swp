# Customer Review Summary

**Date:** 26 June 2026

**Participants:** Customer representative and project team members

**Evidence:** Sanitized written notes. The meeting recording was not saved because of a technical recording failure.

## Sprint Goal

The Sprint Goal is to improve the reliability and verifiability of the Route Optimization Platform through customer-feedback work, persistent storage, solver robustness, measurable quality requirements, automated tests, CI, and deployment improvements.

The complete Sprint Goal was not accepted as achieved during this meeting because the Sprint increment and final quality evidence were still incomplete.

## Increment and product access

The application is available through Docker and is deployed on a university VM.

The hosted deployment is currently limited to the Innopolis University network. Because the customer was outside Innopolis, the customer could not open the hosted application during the meeting.

The team agreed to provide external access or another agreed remote access method.

## UAT result

Customer-executed UAT was not completed.

No UAT scenario should be reported as Passed based on this meeting. A follow-up recorded UAT session is required.

## Quality evidence status

Quality requirements and QRT specifications have been prepared or are being prepared for:

- solver correctness;
- solver execution time;
- job recoverability;
- safe API error handling.

Final automated test implementation and protected-main CI evidence remain incomplete.

## Main customer feedback

1. Compare the current solver with the baseline under equivalent conditions.
2. Investigate whether the greedy stage causes weaker results.
3. Evaluate more joint optimization of vehicles, loaders, and optional orders.
4. Make the product accessible to the customer outside the university network.

## Decisions and action points

| Action | Issue | Status |
|---|---|---|
| Provide external or explicitly agreed customer access. | [#90](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/90) | In progress |
| Complete customer-executed UAT. | [#91](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/91) | Blocked by deployment access |
| Compare the current solver with the baseline. | [#97](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/97) | To Do |
| Investigate greedy-stage impact. | [#97](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/97) | To Do |
| Evaluate joint optimization. | [#23](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/23) | Product Backlog |
| Complete QRT implementation and CI evidence. | [#87](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/87), [#88](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/88) | Specification done; implementation/evidence in progress |
| Conduct the follow-up recorded Sprint Review. | [#92](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/92) | Required |

## Approvals and requested changes

The customer did not provide final product acceptance during this meeting.

Requested follow-up work includes deployment access and solver-quality investigation.

## Remaining risks

- customer access is blocked by the current network restriction;
- UAT is incomplete;
- final Sprint quality evidence is incomplete;
- solver quality may be affected by greedy or sequential optimization stages.

## Backlog impact

Issues [#23](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/23), [#90](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/90), and [#97](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/97) capture the main customer feedback. Issues [#91](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/91) and [#92](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/92) remain open until the customer can execute UAT and the final Sprint Review is recorded.

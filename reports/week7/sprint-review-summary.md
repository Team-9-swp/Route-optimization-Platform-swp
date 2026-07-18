# Sprint 5 Review Summary

- **Meeting date:** 2026-07-16
- **Participants:** customer representative and project team members
- **Public evidence type:** sanitized English summary
- **Handover level:** `Ready for independent use`
- **Customer-confirmation status:** `Accepted with follow-up items`

Private recording links, exact timecodes, customer identity, credentials, and private access details are intentionally excluded.

## Recording and publication permission

The customer granted permission before the meeting continued both to record the session and to publish a sanitized transcript in the public project repository. The canonical public evidence is the [sanitized English Sprint Review transcript](sprint-review-transcript.md); this permission does not authorize publication of the raw recording or raw automatic transcript.

## Sprint Goal and final-state changes reviewed

The meeting reviewed the Sprint 5 goal of completing Week 6 follow-up work, improving the final user-facing workflow, and preparing the product for independent internal/local use.

- The team confirmed that actual execution-duration display had been added.
- The team confirmed that Objective values had been rounded for readable presentation.
- The improved vehicle/loader visualization was still being finalized and was not shown in its finished state. The team offered a later build or screenshots for follow-up review.
- The restored JSON upload was merged later through PR #207 and was not treated as customer-reviewed evidence from this meeting.

## Deployment, reproduction, and intended use

The customer described the product as primarily an internal/local tool. A permanently exposed commercial internet service was not required. The main transition path is the source repository plus Docker Compose instructions, with the customer expected to run or reproduce the product in their own environment.

Reproducibility remained important: the customer wanted the product to run successfully and produce results comparable to the team's results. The meeting did not provide inspectable proof of customer-side deployment, operation, or a completed reproduction run.

## Final transition discussion

The customer asked how follow-up contact and support would work after delivery. The support duration and the point when regular team support ends were not clearly documented. The customer recommended explicitly documenting final transfer and the end of support.

The conservative classification is:

- **Handover level:** `Ready for independent use`
- **Customer-confirmation status:** `Accepted with follow-up items`

No claim is made that the customer independently used, deployed, or operated the final product.

## Customer feedback

The customer gave positive overall feedback about the collaboration and the project's technical and R&D value. The customer noted the uncertainty inherent in algorithmic work and recognized the team's exploration of optimization approaches.

## Follow-up actions

| Classification | Action | Tracking |
|---|---|---|
| Team-side | Provide the finished visualization for customer review. | [#188](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/188) |
| Team-side | Document the support window and the end of regular support. | [#186](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/186), [`docs/customer-handover.md`](../../docs/customer-handover.md) |
| Customer-side | Run/reproduce the product in the customer's environment and compare representative results. | [#187](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/187) |
| Team-side | Resolve or explicitly defer remaining algorithm/product work, including the driver return-to-depot Objective issue. | [#204](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/204) |
| External | Record environment or network constraints if they affect customer-side reproduction. | [#187](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/187) |

## Risks and limitations

- Finished-visualization customer UAT is not complete.
- Customer-side deployment, operation, and result reproduction are not verified.
- The exact support window needs to be communicated with final delivery.
- Open algorithm, release, demo, and course-evidence tasks remain outside this Sprint Review artifact.

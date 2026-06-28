# Sprint Retrospective — Week 4

## What went well

* The team created a clear Assignment 4 Sprint milestone and refined the selected backlog items.
* Customer feedback was traced to specific Product Backlog issues.
* Quality requirements and QRT specifications were documented with measurable thresholds.
* Documentation changes were made through issue-linked pull requests.
* Link checks were run before review.
* The team documented incomplete work honestly instead of marking unfinished UAT, CI, or quality evidence as completed.

## What did not go well

* The customer could not access the hosted application outside the Innopolis University network.
* The customer meeting recording was not saved because of a technical failure.
* Customer-executed UAT was not completed.
* Automated QRT implementations and final CI evidence were not ready for the customer meeting.
* Several documentation pull requests depended on earlier unmerged branches, which complicated review and merge order.
* Access to the GitHub Project was limited to one team member.

## Changes compared with the previous Sprint

* The team added explicit customer-feedback traceability instead of keeping feedback only in meeting notes.
* Quality requirements now use stable IDs, measurable thresholds, and ISO/IEC 25010 sub-characteristics.
* The team separated broad solver-refactoring work from smaller investigation PBIs.
* Deployment accessibility and pre-UAT access verification were added to the backlog.
* Documentation now distinguishes completed, in-progress, deferred, and blocked work.

## Process improvements for the next Sprint

### 1. Verify customer access before every review

**Owner:** deployment responsible
**Action:** Test the exact customer access path at least one day before UAT or Sprint Review. Keep Docker as a verified fallback.

### 2. Use a recording checklist

**Owner:** meeting facilitator
**Action:** Before the meeting, verify recording permissions, recording status, storage location, microphone input, and backup notes. Confirm that the recording file exists immediately after the meeting.

## Follow-up

This retrospective must be reviewed and updated after the final recorded Sprint Review and customer-executed UAT.

# Sprint Retrospective - Week 4

**Status:** Interim retrospective. The product increment and public documents have been updated, but final PR CI, branch-protection evidence, deployment/access verification, post-merge release creation, and final Sprint Review verification remain open.

## What went well

- The team converted customer feedback into traceable Product Backlog issues instead of leaving it only in meeting notes.
- PostgreSQL persistence replaced the active in-memory job store and made calculation history recoverable.
- Skipped optional orders are now visible in solver/API/frontend output.
- The current solver is benchmarked in a reproducible report.
- Quality requirements use stable IDs, ISO/IEC 25010 sub-characteristics, measurable thresholds, and automated QRT links.
- Ruff and Black are now configured as blocking CI checks instead of optional checks.
- UAT and Sprint Review evidence are documented with a clear separation between public sanitized summaries and private recording evidence.

## What did not go well

- The customer could not access the hosted product from outside the Innopolis University network during the 26 June meeting.
- The 26 June meeting recording was not saved because of a technical failure.
- UAT had to be moved to a separate recorded session on 27 June.
- Public notes do not verify that the 27 June recording covers every required Sprint Review topic.
- Final CI evidence could not be produced locally because isolated PostgreSQL and Node/npm were unavailable in this environment.
- GitHub branch protection evidence depends on organization-admin access.
- Commit, push, and PR creation were blocked in this Codex session by the temporary elevated-action usage limit.

## Changes compared with the previous Sprint

- The product now uses PostgreSQL-backed persistence rather than process-local storage.
- Quality gates are treated as continuing project assets, not one-time report material.
- QRTs now exercise solver correctness, performance, recoverability, and safe error handling.
- Documentation distinguishes Done, deferred, blocked, private-evidence, and post-merge states.
- Release preparation now separates draft release notes from actual release creation on protected `main`.

## Process improvements

### 1. Verify customer access before every review

**Owner:** deployment responsible

**Action:** Test the exact customer access path at least one day before UAT or Sprint Review. Keep Docker Compose as a verified fallback and record which access method the customer actually used.

### 2. Use a recording and evidence checklist

**Owner:** meeting facilitator

**Action:** Before the meeting, verify recording permission, recording status, audio input, storage location, and backup notes. Immediately after the meeting, confirm the recording file exists and record private Moodle-only timecodes.

## Follow-up

This retrospective can be marked final only after:

- PR CI passes with backend integration tests, QRTs, frontend typecheck, and frontend build;
- branch-protection evidence is verified by an organization admin or explicitly documented as unavailable;
- deployment/access and release evidence are complete;
- private UAT recording evidence is verified;
- final Sprint Review evidence is verified or a follow-up Sprint Review is conducted.

# Sprint Retrospective - Week 4

**Status:** Interim retrospective. The product increment, public CI evidence, screenshots, GitHub Release `v1.2.0`, and combined Sprint Review/UAT documentation have been updated. Branch-protection evidence, deployment/access verification, and private Moodle-only recording evidence remain open.

## What went well

- The team converted customer feedback into traceable Product Backlog issues instead of leaving it only in meeting notes.
- PostgreSQL persistence replaced the active in-memory job store and made calculation history recoverable.
- Skipped optional orders are now visible in solver/API/frontend output.
- The current solver is benchmarked in a reproducible report.
- Quality requirements use stable IDs, ISO/IEC 25010 sub-characteristics, measurable thresholds, and automated QRT links.
- Ruff and Black are now configured as blocking CI checks instead of optional checks.
- PR #106 merged, and protected-main CI verified backend tests, QRTs, Bandit, frontend typecheck, frontend build, coverage upload, and Link Check.
- The combined Sprint Review and customer UAT session was completed on 27 June 2026, with public sanitized summaries separated from private Moodle-only recording evidence.
- GitHub Release `v1.2.0` is published from protected `main`.

## What did not go well

- The customer could not access the hosted product from outside the Innopolis University network during the 26 June meeting.
- GitHub branch protection evidence depends on organization-admin access.
- Private recording URL, exact timecodes, and permission evidence cannot be published in the repository and must remain in Moodle.

## Changes compared with the previous Sprint

- The product now uses PostgreSQL-backed persistence rather than process-local storage.
- Quality gates are treated as continuing project assets, not one-time report material.
- QRTs now exercise solver correctness, performance, recoverability, and safe error handling.
- Documentation distinguishes Done, deferred, blocked, private-evidence, and post-merge states.
- Release documentation now points to the published `v1.2.0` release on protected `main`.

## Process improvements

### 1. Verify customer access before every review

**Owner:** deployment responsible

**Action:** Test the exact customer access path at least one day before UAT or Sprint Review. Keep Docker Compose as a verified fallback and record which access method the customer actually used.

### 2. Use a recording and evidence checklist

**Owner:** meeting facilitator

**Action:** Before the meeting, verify recording permission, recording status, audio input, storage location, and backup notes. Immediately after the meeting, confirm the recording file exists and record private Moodle-only timecodes.

## Follow-up

This retrospective can be marked final only after:

- branch-protection evidence is verified by an organization admin or explicitly documented as unavailable;
- deployment/access evidence is complete;
- private combined Sprint Review/UAT recording evidence remains available through Moodle.

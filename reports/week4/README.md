# Week 4 Report — Assignment 4

## Project

**Route Optimization Platform** — a logistics optimisation system that generates vehicle and loader routes for the BIA CVRPTW problem variant.
License: [MIT](../../LICENSE)

## Summary of scope since Assignment 3

The Assignment 4 Sprint (22 June – 3 July 2026) shifts focus from feature delivery to quality, reliability, and customer validation. Key outcomes:

- Defined 4 measurable quality requirements with distinct ISO/IEC 25010 sub-characteristics in [`docs/quality-requirements.md`](../../docs/quality-requirements.md)
- Automated quality requirement test specifications in [`docs/quality-requirement-tests.md`](../../docs/quality-requirement-tests.md)
- Created and executed 3 end-user-facing UAT scenarios in [`docs/user-acceptance-tests.md`](../../docs/user-acceptance-tests.md)
- Assignment 4 sprint plan and roadmap in [`docs/roadmap.md`](../../docs/roadmap.md)
- Released [`v1.1.0`](https://github.com/Team-9-swp/Route-optimization-Platform-swp/releases/tag/v1.1.0) for the Assignment 4 Sprint increment

## Solver benchmark and greedy-stage analysis

- [`solver-benchmark.md`](./solver-benchmark.md) — reproducible objective/runtime comparison across all `instances/i*.json` fixtures.
- [`solver-benchmark-greedy.md`](./solver-benchmark-greedy.md) — same benchmark with the Loader SA refinement skipped.
- [`greedy-stage-analysis.md`](./greedy-stage-analysis.md) — comparison of the full pipeline versus the greedy-only pipeline.

## UAT results summary

All 3 active UAT scenarios were executed by the customer during a recorded session and accepted. No scenarios failed or require product changes at this stage.

### Passed scenarios

| ID | Title | Result |
|---|---|---|
| UAT-01 | Submit a delivery instance and receive an optimised solution | Passed |
| UAT-02 | Validate a custom solution through the validator | Passed |
| UAT-03 | Retrieve previously submitted solutions from history | Passed |

### Failed or blocked scenarios

None.

### Most important customer feedback

- The customer confirmed that the core workflow (submit → solve → view results) works as expected.
- The route map and route tables were found clear and useful for understanding vehicle and loader assignments.
- The validation page was appreciated for testing custom solutions before deployment.
- No blocking issues or usability problems were identified during the session.

### Resulting PBIs or issues

No new PBIs or issues were created as a direct result of UAT. The customer accepted the current increment as-is. Any follow-up items will be triaged into the Product Backlog for the next sprint.

## Backlog and Sprint views

- **GitHub Project (board)**: https://github.com/orgs/Team-9-swp/projects/1
- **Sprint Backlog view**: https://github.com/orgs/Team-9-swp/projects/1/views/2
- **Sprint milestone**: https://github.com/Team-9-swp/Route-optimization-Platform-swp/milestone/5

## Release and changelog

- **SemVer release**: https://github.com/Team-9-swp/Route-optimization-Platform-swp/releases/tag/v1.1.0
- **CHANGELOG**: [CHANGELOG.md](../../CHANGELOG.md)

## Deployment

- **Docker Compose:** `docker compose -f docker-compose.yml -f docker-compose.prod.yml up --build -d`
- **Run instructions:** [README.md → Quick start](../../README.md#quick-start)
- **Remote access:** via ngrok (see [README.md → Deployment](../../README.md#deployment))

## Maintained quality assets

- [`docs/quality-requirements.md`](../../docs/quality-requirements.md)
- [`docs/quality-requirement-tests.md`](../../docs/quality-requirement-tests.md)
- [`docs/user-acceptance-tests.md`](../../docs/user-acceptance-tests.md)

## Process and templates

- [Definition of Done](../../docs/definition-of-done.md)
- [Roadmap](../../docs/roadmap.md)
- [Issue templates](../../.github/ISSUE_TEMPLATE)
- [Pull Request template](../../.github/pull_request_template.md)

## Reviewed PRs (Assignment 4)

- #95 — Assignment 4 sprint planning and roadmap update
- #96 — Quality requirements and quality requirement tests
- #97 — (placeholder for additional sprint PRs)

## Video demonstration

- **Public demo video:** *Coming soon — will be linked once recorded*

## Screenshots

See [`reports/week4/images/`](./images/). The following screenshots should be added before final submission:

- Sprint Backlog view (Assignment 4)
- SemVer release v1.1.0
- Quality requirements document
- UAT document with execution history

## Private UAT recording

The private customer UAT recording has been submitted via Moodle. The recording link is **not** committed to the public repository per team policy.

## Contribution traceability

| Name | GitHub username | Role | PRs | Reviews |
|---|---|---|---|---|
| TBD | TBD | TBD | TBD | TBD |

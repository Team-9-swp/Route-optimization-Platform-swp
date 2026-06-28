# Draft Release Notes - v1.2.0

These notes are prepared for the post-merge GitHub release. The final release must be created from the merge commit on `main`, not from this PR branch.

## Assignment 4 Sprint Mapping

- Sprint milestone: https://github.com/Team-9-swp/Route-optimization-Platform-swp/milestone/5
- Product Backlog view: https://github.com/orgs/Team-9-swp/projects/1/views/1
- Sprint Backlog view: https://github.com/orgs/Team-9-swp/projects/1/views/3
- Sprint dates: 22 June 2026 - 3 July 2026
- Selected scope: persistent job history, skipped optional orders, solver robustness, measurable quality requirements, QRTs, CI quality gates, testing evidence, UAT/reporting evidence, and release preparation.

## Product Changes

- Added PostgreSQL persistence for jobs, results, validation metadata, and history.
- Replaced active in-memory job storage with async `app/repository.py`.
- Added skipped optional orders to solver output, API responses, and frontend result views.
- Integrated the current PyVRP/Nevergrad solver pipeline with the async runner.
- Removed the obsolete `max_restarts` solve parameter.
- Added user-safe solver failure handling so public API responses do not expose stack traces, internal paths, or injected fake secrets.

## Quality and Test Changes

- Added automated QRTs for:
  - `QR-FC-01` / `QRT-FC-01`: solver output validates with zero hard-constraint violations.
  - `QR-PE-01` / `QRT-PE-01`: fixed benchmark completes within 900 seconds and configured time limits reach a terminal state.
  - `QR-RE-01` / `QRT-RE-01`: completed jobs survive PostgreSQL-backed repository/application recreation.
  - `QR-SE-01` / `QRT-SE-01`: controlled internal failures do not leak private diagnostics through the API.
- Made Ruff and Black blocking backend CI checks.
- Added frontend `npm run typecheck` before the production build.
- Added coverage XML and JUnit XML artifacts for backend test evidence.
- Kept Bandit as the additional QA security check for medium/high severity findings in `app/`.

## Run Instructions

```bash
docker compose up --build
```

Open:

- API docs: http://localhost:8000/docs
- Web app: http://localhost:3000

For local backend development:

```bash
docker compose up -d db
alembic upgrade head
python -m uvicorn app.main:app --reload
```

For frontend verification:

```bash
cd frontend
npm ci
npm run typecheck
npm run build
```

## Public Artifacts

- Week 4 report: `reports/week4/README.md`
- Public demo video: https://drive.google.com/file/d/15Dh_azNvTxptEjW1XX4S__jnOmg84rHg/view?usp=sharing
- Presentation: `reports/week4/presentation.pdf`
- Solver benchmark: `reports/week4/solver-benchmark.md`
- Changelog: `CHANGELOG.md`

## Known Evidence Limitations

- The GitHub release must be created only after this PR is merged to `main`.
- Branch protection / required-check settings require organization admin verification.
- Customer recording URL, exact UAT timecodes, and recording permission evidence must stay private and be supplied through Moodle or another approved private channel.
- The university VM deployment is publicly documented as network-limited until customer access is verified or another access method is explicitly agreed.

## Post-Merge Command

After the PR is merged and `main` is up to date:

```bash
gh release create v1.2.0 --target main --title "v1.2.0 - Assignment 4 Quality Gates and Persistent Jobs" --notes-file reports/week4/release-notes-v1.2.0.md
```

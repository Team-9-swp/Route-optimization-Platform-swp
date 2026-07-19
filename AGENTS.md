# AGENTS.md

This file is the predictable instruction file for coding agents working in this repository, following the open [agents.md](https://agents.md/) convention. It complements [`README.md`](./README.md) (project overview and access) and [`CONTRIBUTING.md`](./CONTRIBUTING.md) (human contributor guide). Keep human onboarding in those files; this file is for agent-relevant operating guidance.

## Repository at a glance

- **Product:** Route Optimization Platform for the BIA CVRPTW variant — FastAPI backend, PostgreSQL persistence, PyVRP/Nevergrad solver (`solver.py`), hard-constraint validator (`backup/validator.py`, exposed via `app/validation.py`), and a React + TypeScript + Vite frontend under `frontend/`.
- **Default branch:** `main` (protected, always deployable). Releases are SemVer `vX.Y.Z` tags from `main`; latest is `v1.5.0`.
- **Source of truth for process:** [`docs/development-process.md`](./docs/development-process.md).

## Key locations

| Area | Path |
|---|---|
| API app | `app/main.py`, `app/api.py`, `app/service.py`, `app/runner.py`, `app/schemas.py`, `app/repository.py`, `app/db.py` |
| Solver | `solver.py` (entry point `solve(raw_data, time_limit, seed)`) |
| Validator | `backup/validator.py` (`validate_solution(instance, solution)`), wrapped by `app/validation.py` |
| Frontend | `frontend/src/app/components/*.tsx`, `frontend/src/api/*.ts`, `frontend/src/types/index.ts` |
| Tests | `tests/` (unit/integration), `tests/quality/` (QRTs) |
| Deployment | `docker-compose.yml`, `docker-compose.prod.yml`, `docs/deployment.md` |
| Migrations | `alembic/versions/` |

## Setup and common commands

Backend:

```bash
python -m pip install -r requirements.txt
docker compose up -d db && alembic upgrade head     # PostgreSQL for integration tests
python -m uvicorn app.main:app --reload
```

Frontend:

```bash
cd frontend && npm install && npm run dev            # proxies /api -> http://localhost:8000
```

Verify (mirror CI):

```bash
# Backend
pytest tests/ --ignore=tests/quality --ignore=tests/test_e2e.py -m "not slow" --cov=app --cov-report=term-missing
pytest tests/quality/ -m "qrt" -q
ruff check . && black --check . && bandit -r app/ -ll
# Frontend
npm --prefix frontend run typecheck
npm --prefix frontend run build
```

The solver is heavy (PyVRP/Nevergrad). Prefer the small fixtures in `test_cases/` for quick validation runs; run full benchmarks only when needed (`python scripts/benchmark.py --time-limit 60`).

## Workflow and review expectations

- Trunk-based GitHub flow. Branch from `main` with `feat/...`, `fix/...`, or `docs/...` prefixes; land via pull request only.
- Every PR is **issue-linked** (`Closes #NNN`) and **reviewed by a different person** than the implementer. Do not self-merge unless explicitly authorized.
- Use Conventional Commits with a short body explaining the change.
- Inspect `git status` and `git diff` before committing; stage only intended files.
- CI (backend + frontend jobs) must pass before merge. See [CI pipeline](./docs/development-process.md#ci-pipeline) and [Definition of Done](./docs/definition-of-done.md).

## Safety and data cautions

- Never commit real credentials, customer data, private recordings, private access instructions, or limited-permission test credentials. Runtime configuration is supplied via environment variables and `docker-compose.prod.yml`, not committed secrets. See [Secret and sensitive information handling](./docs/development-process.md#secret-and-sensitive-information-handling).
- Public artifacts must be sanitized: use GitHub usernames/roles instead of real names; use only sanitized demo/test data in screenshots, API examples, and deployments.
- Do not run code from pull requests on the production VM (the self-hosted deploy runner only runs on `main`).
- Do not edit applied Alembic history; reverse a migration with a new revision.

## Notes for agents

- The solver does **not** mutate its input instance, so the stored `input_data` is safe to reuse for validation.
- The stored solver `result` strips `_cost`, `_evaluator`, and `objective_value`; `objective_value` lives in its own DB column and in the validation report.
- When changing solver output or validation, keep `tests/test_validator.py`, `tests/quality/`, and `docs/quality-requirement-tests.md` consistent.

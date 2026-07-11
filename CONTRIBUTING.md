# Contributing

Thanks for contributing to the Route Optimization Platform. This guide is the short, public entry point for human contributors. It complements the root [`README.md`](./README.md) (project overview and access) and the deeper [development process](./docs/development-process.md) (canonical workflow, CI, and configuration details).

## Ground rules

- Open an issue before starting non-trivial work so it can be traced and reviewed.
- Keep `main` green: every change lands through a pull request that passes CI.
- Do not commit real credentials, customer data, or private access details. See [Secret and sensitive information handling](./docs/development-process.md#secret-and-sensitive-information-handling).
- Follow the existing code style. Backend is formatted with Black and linted with Ruff; frontend is type-checked with `tsc`.

## Set up a local environment

Backend:

```bash
python -m pip install -r requirements.txt
docker compose up -d db          # PostgreSQL for persistence/integration tests
alembic upgrade head
python -m uvicorn app.main:app --reload
```

Frontend:

```bash
cd frontend
npm install
npm run dev                      # Vite dev server, proxies /api -> http://localhost:8000
```

## Verify your changes before pushing

Backend tests and quality gates (match what CI runs):

```bash
pytest tests/ --ignore=tests/quality --ignore=tests/test_e2e.py -m "not slow" --cov=app --cov-report=term-missing
pytest tests/quality/ -m "qrt" -q
ruff check . && black --check .
bandit -r app/ -ll
```

Frontend:

```bash
npm run typecheck
npm run build
```

Integration tests and quality requirement tests require PostgreSQL configured through `DATABASE_URL`.

## Branch and pull-request workflow

The team uses trunk-based GitHub flow (see [Git workflow](./docs/development-process.md#git-workflow) for the full model):

1. Create a short-lived branch from the latest `main`:
   - `feat/...` for features, `fix/...` for bug fixes, `docs/...` for documentation.
2. Make small, reviewable commits. Conventional commit messages are preferred.
3. Push and open a pull request against `main`.
4. Link the issue with `Closes #NNN` in the PR description.
5. Make sure the acceptance criteria checkboxes in the linked issue are satisfied.

## Review and merge requirements

- A pull request requires **review by a different team member** than the implementer.
- CI (backend lint/format/tests/QRT and frontend type-check/build) must pass.
- Acceptance criteria from the linked issue must be verified before merge.
- See [Definition of Done](./docs/definition-of-done.md) for the shared completion standard.
- Squash-and-merge or rebase-and-merge keeps `main` linear.

## Releases

Releases follow [Semantic Versioning](https://semver.org/) with a `v` prefix and are tagged from protected `main`. User-visible changes are recorded in [`CHANGELOG.md`](./CHANGELOG.md). See [Releases and changelog](./docs/development-process.md) for the full release workflow.

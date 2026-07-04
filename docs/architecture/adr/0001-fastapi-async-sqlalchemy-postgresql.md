# ADR-0001: Adopt FastAPI with async SQLAlchemy and PostgreSQL for persistent job storage

- **Status:** Accepted
- **Date:** 2026-07-04
- **Addresses quality requirement:** [QR-RE-01 — Job Recoverability](../../quality-requirements.md)

## Context

The product exposes a long-running route-optimization job lifecycle: a customer submits a CVRPTW instance, the solver runs, and the completed result must be retrievable later. The customer explicitly asked for calculation history.

The earlier MVP used an in-memory job store. Any backend or container restart lost every submitted job and result, so the product could not satisfy recoverability expectations and could not be reliably demonstrated after a redeploy. Concurrency is also important: the API must stay responsive while a solver job runs for up to several minutes, which argues for an asynchronous I/O model.

The system must also be runnable directly by the customer and by graders, so the storage component must be reproducible from the committed sources and documented in the deployment model.

## Decision

We adopt **FastAPI** as the backend framework with an **asynchronous SQLAlchemy** layer connected to **PostgreSQL** through the `asyncpg` driver, with **Alembic** managing schema migrations.

Concretely:

- The application is assembled in `app/main.py` as an async FastAPI app; the router lives in `app/api.py`.
- Persistence uses an async SQLAlchemy repository (`app/repository.py`) and a database engine/session managed in `app/db.py`.
- The connection string is delivered through the `DATABASE_URL` environment variable; the default local/CI value is `postgresql+asyncpg://optimizer:optimizer@db:5432/optimizer`.
- Schema changes ship as Alembic revisions under `alembic/versions/` and are applied with `alembic upgrade head` (in CI and on startup).
- A named Docker volume (`pgdata`) holds the PostgreSQL data directory so data survives container recreation.

## Consequences

- **Positive:** Submitted jobs and completed results remain available after backend or container restarts as long as the same persistent database (volume) is reused. This directly satisfies QR-RE-01.
- **Positive:** The async model keeps the API responsive while solver jobs run in the background.
- **Positive:** Migrations make schema evolution reviewable and reproducible alongside code changes.
- **Negative:** The stack now depends on a PostgreSQL service, adding operational responsibility (health checks, backups, migration ordering).
- **Negative:** Integration and QRT tests require a live PostgreSQL instance, which is reflected in the CI pipeline and `docs/testing.md`.

## Alternatives considered

- **SQLite:** simpler to operate but weaker under concurrent writes and less representative of a production-grade deployment; rejected because it undermined confidence in recoverability and concurrency evidence.
- **Keep in-memory storage:** rejected because it fundamentally cannot satisfy QR-RE-01 and broke customer demonstration after restarts.

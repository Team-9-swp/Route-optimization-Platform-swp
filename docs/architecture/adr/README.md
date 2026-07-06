# Architecture Decision Records

This directory holds the maintained Architecture Decision Records (ADRs) for the Route Optimization Platform.

An ADR captures *one* significant technical decision: the context that forced it, the decision made, and the consequences accepted. ADRs are versioned together with the product and updated through the normal issue-linked pull-request workflow.

## Index

| ID | Decision | Status | Addresses |
|---|---|---|---|
| [ADR-0001](0001-fastapi-async-sqlalchemy-postgresql.md) | Adopt FastAPI with async SQLAlchemy and PostgreSQL for persistent job storage | Accepted | QR-RE-01 |
| [ADR-0002](0002-pyvrp-nevergrad-bounded-runner.md) | Use a PyVRP + Nevergrad solver pipeline inside a bounded async job runner | Accepted | QR-FC-01, QR-PE-01 |
| [ADR-0003](0003-user-safe-error-handling.md) | Return user-safe error messages without internal details | Accepted | QR-SE-01 |
| [ADR-0004](0004-docker-compose-deployment.md) | Deploy as a Docker Compose stack of `db`, `api`, and `frontend` | Accepted | Deployment model |

## How ADRs are organized here

- File names use the form `NNNN-short-kebab-case-title.md`, zero-padded and numbered in creation order.
- Each ADR has stable sections: Status, Context, Decision, Consequences, and the Quality Requirement(s) it addresses.
- Status follows the usual ADR lifecycle: `Proposed`, `Accepted`, `Deprecated`, `Superseded`, or `Rejected`.
- When a decision is superseded, the old ADR is marked `Superseded by ADR-NNNN` rather than deleted.

## Relationship to the architecture documentation

The main architecture documentation is `docs/architecture/README.md` (maintained by A5-04, issue #112). It links the relevant ADRs from the static, dynamic, and deployment views and explains how the documented architecture and the recorded decisions fit together.

Each relevant quality requirement in [`docs/quality-requirements.md`](../../quality-requirements.md) links back to at least one ADR in its Traceability section.

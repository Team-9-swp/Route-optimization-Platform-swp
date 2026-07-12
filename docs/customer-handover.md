# Customer Handover

This is the maintained customer-facing handover document for the Route Optimization Platform. It describes the **actual current handover state** of the product, how to access and run it, what configuration it needs, and what support remains. It is written for the customer and the TA reviewer. Private credentials and customer-identifying details are never placed here; they are shared only through the private submission channel.

For the project overview and public entry point, see [`README.md`](../README.md). This document is kept current whenever access details, deployment steps, limitations, or transition status change.

---

## 1. Product overview

The Route Optimization Platform solves the **BIA CVRPTW** vehicle-and-loader routing problem variant. It produces:

- vehicle routes with a planned arrival schedule (time windows, capacity, shift limits);
- loader routes that meet the vehicle schedule;
- hard-constraint validation of any generated solution;
- skipped optional-order reporting when optional orders cannot be served;
- a web interface to submit instances, inspect results, validate, and download validator-compatible solution JSON.

The system has three services: a FastAPI backend (`api`), a PostgreSQL database (`db`) for persistent job history, and a React frontend (`frontend`) served by nginx.

## 2. Current handover status

| Item | State |
|---|---|
| Latest release | [`v1.3.0`](https://github.com/Team-9-swp/Route-optimization-Platform-swp/releases/tag/v1.3.0) (MVP v2) on protected `main` |
| Source repository | [Team-9-swp/Route-optimization-Platform-swp](https://github.com/Team-9-swp/Route-optimization-Platform-swp) |
| Repository ownership | Retained by the team (course project). Read access granted to the customer and TA. |
| Hosted trial deployment | University VM, reachable **only from the Innopolis campus network** |
| Customer-side deployment | **Planned** — customer to self-deploy from `master` branch in Week 7 |
| **Handover level reached** | **Ready for independent use** (customer deployment planned) |

**Handover level: `Ready for independent use`.** The product can be built and run independently from the public repository using the instructions below, and a hosted trial instance exists on the university VM. The customer has confirmed they will self-deploy from the `master` branch in Week 7 using a single container with full UI. That transition level depends on the customer successfully completing the self-deployment and verifying the results.

## 3. How the customer accesses and uses the product

Two access paths are available:

### Option A — Hosted trial (within the Innopolis network)

A running stack is deployed on the university VM. While on the campus network or VPN, the customer opens the frontend URL provided during the trial session. The web UI lets the customer:

1. Go to **New Job**, paste or upload an instance JSON, optionally set a name/seed, and run the solver.
2. Open the resulting job to inspect vehicle/loader routes, the route map, the validation report, and skipped optional orders.
3. Download the validator-compatible solution JSON.

For access from outside the campus network during a live session, an agreed short-lived tunnel (for example `ngrok http 3000`) may be used. The tunnel command is an access convenience, not deployment evidence.

### Option B — Run independently from source

```bash
git clone https://github.com/Team-9-swp/Route-optimization-Platform-swp.git
cd Route-optimization-Platform-swp
docker compose up --build
```

Then open the web interface at `http://localhost:3000` and the API docs (Swagger) at `http://localhost:8000/docs`.

## 4. Installation and deployment

Full deployment details are in [`docs/deployment.md`](deployment.md). Summary:

- **Local / customer self-run:** `docker compose up --build`. PostgreSQL is started automatically by the Compose stack; no external database is required.
- **Production overrides:** `docker-compose.prod.yml` sets the restart policy, production `CORS_ORIGINS`, and `LOG_LEVEL=warning`.
- **VM deployment (team-operated):** a self-hosted GitHub Actions runner on the VM builds and starts the stack from protected `main` after CI passes, reconciles the database schema, and runs a local health check. No GitHub Secrets are required for deployment.
- **Health check:** `GET /health` returns `200` when the API is ready.

Recovery and rollback procedures are documented in [`docs/deployment.md`](deployment.md#recovery-from-a-failed-deployment).

## 5. Configuration and secrets handling

The product is configured through environment variables and the Compose files; **no secrets are committed to the repository**.

| Variable | Purpose | Default (local) |
|---|---|---|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql+asyncpg://optimizer:optimizer@db:5432/optimizer` |
| `CORS_ORIGINS` | Allowed browser origins for the API | `http://localhost:3000,http://localhost:5173` |
| `LOG_LEVEL` | API log verbosity | `info` (production: `warning`) |
| `VITE_API_BASE_URL` | API base URL used by the frontend at build time | `http://localhost:8000` |

- The local Compose defaults (`optimizer:optimizer`) are for local/trial use only. Production overrides `DATABASE_URL`, `CORS_ORIGINS`, and other values through `docker-compose.prod.yml` and the VM environment.
- Any real production database password or tunnel credential is supplied out-of-band through the private submission channel and is **never** committed.
- See `.env.example` for the sanitized example configuration and [`docs/development-process.md`](development-process.md#secret-and-sensitive-information-handling) for the secrets policy.

## 6. Operational notes

- Jobs are persisted in PostgreSQL; restarting the stack preserves job history. The `pgdata` volume holds the database.
- The solver runs asynchronously. After submitting a job, poll `GET /jobs/{job_id}` (or watch the dashboard) until the status becomes `completed` or `failed`.
- A job can be auto-validated on completion (`auto_validate=true`) or validated separately via the **Validate** page / `POST /validate`.
- Solver runtime is bounded by `time_limit` (seconds); larger instances need more time for better solutions.

## 7. Verification steps the customer can follow

1. Open `http://<host>:3000` (or `http://localhost:3000` when self-running).
2. Submit the provided sample instance (for example `test_cases/t1.json`) from the New Job page.
3. Wait for the job to complete; open it and confirm the route map, vehicle/loader routes, and validation result render.
4. Download the solution JSON and confirm it matches the validator's expected schema (`vehicles`, `loaders`).
5. Optionally run `python backup/validator.py --dir test_cases --input_file t1 --result_file <downloaded>` to re-validate independently.

## 8. Troubleshooting and support

| Symptom | What to check |
|---|---|
| Frontend cannot reach the API | The browser origin must be in `CORS_ORIGINS`; the API must be up (`GET /health`). |
| Hosted trial unreachable | The VM is only reachable from the Innopolis network/VPN. Use the agreed tunnel during a live session, or run from source (Option B). |
| Job stuck in `pending`/`running` | The solver is still working; increase `time_limit` for large instances. Very large instances may return infeasible. |
| `failed` status | The solver could not find a feasible solution within the limit, or the instance is malformed. Check the instance JSON and retry with a higher `time_limit`. |
| Database errors on startup | Ensure PostgreSQL is healthy and `DATABASE_URL` is correct; run `alembic upgrade head`. |

Support during the course is provided by the team through the agreed channel. Issues can be filed in the [repository issue tracker](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues).

## 9. Known limitations and risks

- The hosted deployment is **campus-network-only**; external customer access requires the customer to be on the network/VPN or use an agreed temporary tunnel.
- The customer has **not yet** deployed or operated the product on their side; self-deployment is planned for Week 7.
- Solver quality depends on `time_limit` and instance size; very large or tightly-constrained instances may fail to find a feasible solution.
- The current Gantt/schedule visualization scope is limited (see roadmap).
- A minor cost-calculation edge case exists where driver return-to-depot routes split by zeros are counted as separate drivers (deferred to Sprint 5).
- This is a course project; long-term production hardening (HA, backups, monitoring) is out of scope.

## 10. Remaining actions and blockers

| Action | Blocks full transition? |
|---|---|
| Customer to self-deploy from `master` branch and verify deployment | Yes — needed before moving to "Independently used by customer" |
| Customer to run the algorithm from sources and verify against baseline | Yes — confirms algorithm results match team's claims |
| Customer to run the algorithm through the web interface and verify consistency | Yes — confirms UI and algorithm versions are synchronised |
| Address driver return-to-depot cost-calculation edge case | No — minor edge case, deferred to Sprint 5 |
| Complete Gantt chart visualisation | No — in progress for Sprint 4 |

Reaching `Independently used by customer` depends on the customer successfully deploying and running the product independently, which is planned for Week 7.

## 11. Related documentation

- [README.md](../README.md) — public entry point and quick start
- [Deployment](deployment.md) — full deployment, redeploy, and rollback
- [Interface documentation](interface.md) — web UI and REST API
- [Architecture](architecture/README.md) — system architecture and ADRs
- [Development process](development-process.md) — workflow, CI, and configuration management
- [Testing strategy](testing.md) and [Quality requirements](quality-requirements.md)
- [User acceptance tests](user-acceptance-tests.md)
- [Roadmap](roadmap.md)
- [Hosted documentation site](https://team-9-swp.github.io/Route-optimization-Platform-swp/)

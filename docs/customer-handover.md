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
| Latest release | [`v1.4.0`](https://github.com/Team-9-swp/Route-optimization-Platform-swp/releases/tag/v1.4.0) — Assignment 6 Week 6 trial / handover-candidate release on protected `main` |
| Source repository | [Team-9-swp/Route-optimization-Platform-swp](https://github.com/Team-9-swp/Route-optimization-Platform-swp) |
| Repository ownership | Retained by the team (course project). Read access granted to the customer and TA. |
| Hosted trial deployment | University VM, reachable **only from the Innopolis campus network** |
| Customer-side deployment | **Not verified** — the customer expects to reproduce the product in their own environment |
| **Handover level reached** | **Ready for independent use** |
| **Customer-confirmation status** | **Accepted** |

**Handover level: `Ready for independent use`.** The source repository and Docker Compose instructions are the main handover path. The product can be built and run independently, but customer-side deployment or operation has not been verified.

**Customer-confirmation status: `Accepted`.** The customer confirmed that the current customer-facing documentation is sufficient, the run/deployment guidance and transition model are clear, the final changes and product state are accepted, and the documented package is suitable for the reached level of independent use. This acceptance does not assert that the customer deployed, operated, health-checked, or reproduced results from the product independently.

## 3. How the customer accesses and uses the product

The intended operational model is internal or local use. A permanent public commercial internet service is not required. Two access paths are available:

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

### Support window

- Until final course delivery, the team provides reasonable clarification and triage through the agreed team channel and the [repository issue tracker](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues).
- Regular team support ends after final course delivery unless a separate arrangement is explicitly agreed.
- After that point, reproducible defects or documentation gaps should be filed in the issue tracker with sanitized steps, expected behavior, actual behavior, and relevant logs. Do not include credentials, private access details, or customer data.
- This handover does not promise indefinite maintenance, hosting, or operational support.

## 9. Known limitations and risks

- The hosted deployment is **campus-network-only**; external customer access requires the customer to be on the network/VPN or use an agreed temporary tunnel.
- The customer has **not been verified** as having deployed or operated the product on their side.
- Solver quality depends on `time_limit` and instance size; very large or tightly-constrained instances may fail to find a feasible solution.
- The finished interactive route and schedule visualization was not demonstrated to the customer during the 2026-07-16 meeting; the implementation is team-verified but not customer-executed UAT.
- This is a course project; long-term production hardening (HA, backups, monitoring) is out of scope.

## 10. Remaining actions and blockers

| Classification | Follow-up item | Current evidence or action |
|---|---|---|
| Technical limitation | Finished-visualization customer execution is not recorded | The implementation is merged in [PR #205](https://github.com/Team-9-swp/Route-optimization-Platform-swp/pull/205); the Week 7 review record remains conservative. |
| Technical limitation | Final SemVer packaging is not published | The final product state is prepared, but release creation remains tracked in open [#190](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/190). |
| Customer-side | Run the repository/Compose stack and compare representative results with the team's results | Customer expectation was discussed, but successful reproduction is not yet inspectable; track transition evidence in [#187](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/187). |
| External | Customer network, environment, and organizational timing may affect deployment or follow-up contact | Record concrete environment problems in #187 without publishing private access details. |

Administrative confirmation items are closed: the customer accepted the documentation set, transition model, final handover, and final corrections. Customer-side execution remains a follow-up activity rather than a blocker to that acceptance.

Reaching `Independently used by customer` requires inspectable evidence that the customer ran the product independently. Reaching `Deployed or operated on customer side` additionally requires customer-side deployment or operational evidence. Neither stronger level is claimed here.

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

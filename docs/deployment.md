# Deployment

This document describes how the Route Optimization Platform is deployed and operated. It covers the automatic deployment pipeline from protected `main`, the required secrets, manual redeploy and rollback, health verification, and failure handling.

The runtime topology (services, volumes, network boundary) is documented in the deployment view (`docs/architecture/deployment-view/`) and in `docs/architecture/adr/0004-docker-compose-deployment.md` (ADR-0004 — Docker Compose deployment), both maintained by A5-04 and A5-05.

## Deployment model

The product runs as a three-service Docker Compose stack on a single host:

- `db` — PostgreSQL 16 with the persistent `pgdata` volume.
- `api` — FastAPI app (uvicorn), depends on a healthy `db`.
- `frontend` — nginx serving the built React SPA and reverse-proxying `/api` to `api`.

The Compose file is `docker-compose.yml`, overridden for production by `docker-compose.prod.yml` (restart policy, production `CORS_ORIGINS`, `LOG_LEVEL=warning`).

## Automatic deployment from protected `main`

Deployment is automated in the [CI Pipeline](../.github/workflows/ci.yml). A `deploy` job runs **only after the `backend` and `frontend` jobs pass**, and only for:

- a push to `main`; or
- a manual `workflow_dispatch` run.

The `deploy` job:

1. Connects to the host over SSH using `appleboy/ssh-action`.
2. Fetches and checks out the deployed commit (`git reset --hard <commit>`).
3. Builds and starts the stack with `docker compose ... up -d --build --wait --remove-orphans`. `--wait` blocks until the `api` and `db` health checks pass.
4. Applies database migrations explicitly: `docker compose ... exec api alembic upgrade head`. (The API also applies migrations on startup; this step makes migration execution explicit and visible in the deploy log.)
5. Runs a post-deployment health check from the runner: `curl -fsS --retry 5 --retry-delay 5 $DEPLOY_HEALTH_URL/health`.

Because the `deploy` job depends on `backend` and `frontend`, a failing CI check on `main` prevents deployment. A failed SSH command (`script_stop: true`) or a failing `curl` (`-f`) fails the job, so failures are visible in the GitHub Actions UI.

## Required GitHub Secrets

The `deploy` job reads its host access and paths from GitHub Secrets (stored in the `production` environment). They are never committed to the repository.

| Secret | Purpose | Example |
|---|---|---|
| `DEPLOY_HOST` | Hostname or IP of the deployment VM, reachable from GitHub Actions over SSH. | `vm.example.dev` |
| `DEPLOY_USER` | SSH user used for deployment. | `deploy` |
| `DEPLOY_SSH_KEY` | Private SSH key for `DEPLOY_USER`. Stored as a secret only. | `-----BEGIN OPENSSH PRIVATE KEY----- ...` |
| `DEPLOY_PORT` | SSH port. Optional; the action defaults to 22 if empty. | `22` |
| `DEPLOY_PATH` | Absolute path of the checked-out repository on the host. | `/srv/route-optimizer` |
| `DEPLOY_HEALTH_URL` | Base URL used for the post-deploy `/health` check, reachable from GitHub Actions. | `https://route-optimizer.example.dev` |

The host must expose a public SSH endpoint and a health URL reachable from GitHub Actions runners. If the VM is behind a campus network (as noted in the root `README.md`), expose it through an agreed tunnel (for example ngrok) or a public endpoint; the tunnel command itself is not deployment evidence.

To set the secrets, use the GitHub UI (Settings → Environments → `production` → Environment secrets) or the CLI:

```bash
gh secret set DEPLOY_HOST --body "vm.example.dev" --env production
gh secret set DEPLOY_USER --body "deploy" --env production
gh secret set DEPLOY_SSH_KEY --env production < ~/.ssh/id_route_optimizer_deploy
gh secret set DEPLOY_PATH --body "/srv/route-optimizer" --env production
gh secret set DEPLOY_HEALTH_URL --body "https://route-optimizer.example.dev" --env production
```

## Manual redeploy and rollback

Trigger the workflow manually from the Actions tab ("CI Pipeline" → "Run workflow"). Provide a `ref` (branch, tag, or commit SHA) to deploy a specific version.

- **Redeploy the current release:** run the workflow with an empty `ref` (deploys the default branch tip).
- **Rollback:** run the workflow with the commit SHA of the last known-good release. The job does `git reset --hard <ref>` on the host and rebuilds, so the stack returns to that exact commit.

Rollback can also be performed directly on the host if Actions is unavailable:

```bash
ssh deploy@<DEPLOY_HOST>
cd "$DEPLOY_PATH"
git fetch --all --prune
git reset --hard <previous-good-sha>
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build --wait --remove-orphans
docker compose -f docker-compose.yml -f docker-compose.prod.yml exec -T api alembic upgrade head
curl -fsS "$DEPLOY_HEALTH_URL/health"
```

## Recovery from a failed deployment

A failed `deploy` job is visible in the GitHub Actions run log (SSH errors surface because of `script_stop`, and a non-200 `/health` fails `curl -f`). To recover:

1. Inspect the failed job output to identify whether it failed at checkout, build/start, migration, or health check.
2. On the host, check container status and logs:
   ```bash
   docker compose -f docker-compose.yml -f docker-compose.prod.yml ps
   docker compose -f docker-compose.yml -f docker-compose.prod.yml logs api
   ```
3. Roll back to the last good commit using the manual rollback procedure above.
4. Re-run the workflow once the underlying issue is fixed.

Database migrations are forward-compatible by convention. If a migration must be reverted, revert it through a new Alembic revision rather than editing applied history.

## Security notes

- All host access and credentials are delivered through GitHub Secrets (`production` environment), never through committed files.
- The local Compose defaults (`optimizer:optimizer`) are for local/CI use only; production overrides `DATABASE_URL`, `CORS_ORIGINS`, and other values through the host environment or Docker secrets.
- The `production` environment can be configured with required reviewers or deployment branches for additional control.

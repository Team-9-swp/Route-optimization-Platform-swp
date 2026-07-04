# Deployment

This document describes how the Route Optimization Platform is deployed and operated. It covers the automatic deployment pipeline from protected `main`, the self-hosted GitHub Actions runner that performs deployment, manual redeploy and rollback, health verification, and failure handling.

The runtime topology (services, volumes, network boundary) is documented in the deployment view (`docs/architecture/deployment-view/`) and in `docs/architecture/adr/0004-docker-compose-deployment.md` (ADR-0004 — Docker Compose deployment), both maintained by A5-04 and A5-05.

## Deployment model

The product runs as a three-service Docker Compose stack on a single host:

- `db` — PostgreSQL 16 with the persistent `pgdata` volume.
- `api` — FastAPI app (uvicorn), depends on a healthy `db`.
- `frontend` — nginx serving the built React SPA and reverse-proxying `/api` to `api`.

The Compose file is `docker-compose.yml`, overridden for production by `docker-compose.prod.yml` (restart policy, production `CORS_ORIGINS`, `LOG_LEVEL=warning`).

## How automatic deployment works

Deployment is automated in the [CI Pipeline](../.github/workflows/ci.yml). The workflow has three jobs:

- `backend` and `frontend` run on **GitHub-hosted** runners (`ubuntu-latest`) on every pull request and every push to `main`. They are the quality gate (lint, tests, QRTs, build).
- `deploy` runs on a **self-hosted runner that lives on the VM** (`runs-on: self-hosted`). It starts **only after `backend` and `frontend` pass**, and only for a push to `main` or a manual `workflow_dispatch` run.

Because the VM is behind the Innopolis campus network and has no public IP, the runner connects **outbound** to GitHub over HTTPS (long-poll) to pick up jobs. This works through the NAT without opening any inbound port, without a tunnel, and without storing host SSH keys in GitHub.

The `deploy` job:

1. Checks out the deployed commit with `actions/checkout` (honoring the optional `workflow_dispatch` `ref` input).
2. Builds and starts the stack with `docker compose ... up -d --build --wait --remove-orphans`. `--wait` blocks until the `api` and `db` health checks pass.
3. Applies database migrations explicitly: `docker compose ... exec api alembic upgrade head`. (The API also applies migrations on startup; this step makes migration execution explicit and visible in the deploy log.)
4. Runs a post-deployment health check **locally on the VM**: `curl -fsS --retry 5 --retry-delay 5 http://localhost:8000/health`.

Because `deploy` depends on `backend` and `frontend`, a failing CI check on `main` prevents deployment. A failing `docker compose` command or a non-200 `/health` (`curl -f`) fails the job, so failures are visible in the GitHub Actions UI.

## Self-hosted runner setup (on the VM, one time)

Prerequisites on the VM: `bash`, `git`, `docker`, and `docker compose` (already present). The runner needs outbound HTTPS access to `github.com` (available through the campus network).

```bash
# 1. Dedicated user for the runner (do not run it as root)
sudo useradd -m -s /bin/bash github-runner
sudo usermod -aG docker github-runner        # allow `docker compose` without sudo

# 2. Download the runner as that user
sudo -iu github-runner
mkdir actions-runner && cd actions-runner
# Use the exact version/URL shown in the GitHub UI (Settings → Actions → Runners → New self-hosted runner → Linux x64)
curl -o actions-runner.tar.gz -L https://github.com/actions/runner/releases/download/v<VERSION>/actions-runner-linux-x64-<VERSION>.tar.gz
tar xzf actions-runner.tar.gz

# 3. Register (token from the same UI page; it expires in ~1 hour)
./config.sh --url https://github.com/Team-9-swp/Route-optimization-Platform-swp \
  --token <TOKEN> \
  --name vm-runner \
  --labels self-hosted,Linux \
  --unattended

# 4. Smoke test, then stop with Ctrl+C once you see it is "Listening for Jobs"
./run.sh

# 5. Install as a systemd service so it survives reboots (run as root)
exit
cd /home/github-runner/actions-runner
sudo ./svc.sh install github-runner
sudo ./svc.sh start
sudo ./svc.sh status
```

After this, the runner shows as **Idle** in the repo's *Settings → Actions → Runners* list and is ready to execute the `deploy` job. No GitHub Secrets are required for deployment.

## Required GitHub Secrets

**None.** With a self-hosted runner on the VM, the deploy job runs locally: it checks out the code with `actions/checkout` and runs `docker compose`/`alembic`/`curl` directly on the host. There is no SSH step, no tunnel, and no host credential stored in GitHub.

Production runtime configuration (`DATABASE_URL`, `CORS_ORIGINS`, `LOG_LEVEL`) comes from `docker-compose.prod.yml` and the VM environment, not from GitHub Secrets. Optionally, keep the `production` environment configured in the workflow and enable **Required reviewers** on it (Settings → Environments → `production`) so a human must approve each deployment before the `deploy` job runs.

## Manual redeploy and rollback

Trigger the workflow manually from the Actions tab ("CI Pipeline" → "Run workflow"). Provide a `ref` (branch, tag, or commit SHA) to deploy a specific version.

- **Redeploy the current release:** run the workflow with an empty `ref` (deploys the default branch tip).
- **Rollback:** run the workflow with the commit SHA of the last known-good release. `actions/checkout` fetches that exact SHA and the stack is rebuilt from it.

Rollback can also be performed directly on the VM if Actions is unavailable:

```bash
cd /srv/route-optimizer        # or wherever the repo is checked out on the VM
git fetch --all --prune
git reset --hard <previous-good-sha>
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build --wait --remove-orphans
docker compose -f docker-compose.yml -f docker-compose.prod.yml exec -T api alembic upgrade head
curl -fsS http://localhost:8000/health
```

## Recovery from a failed deployment

A failed `deploy` job is visible in the GitHub Actions run log. To recover:

1. Inspect the failed step output to identify whether it failed at checkout, build/start, migration, or health check.
2. On the VM, check container status and logs:
   ```bash
   docker compose -f docker-compose.yml -f docker-compose.prod.yml ps
   docker compose -f docker-compose.yml -f docker-compose.prod.yml logs api
   ```
3. Roll back to the last good commit using the manual rollback procedure above.
4. Re-run the workflow once the underlying issue is fixed.

Database migrations are forward-compatible by convention. If a migration must be reverted, revert it through a new Alembic revision rather than editing applied history.

## Security notes

- The runner runs as a dedicated `github-runner` user (not root) and is in the `docker` group only so it can run `docker compose`. No host SSH credentials are stored in GitHub.
- Only the `deploy` job uses `runs-on: self-hosted`, and it runs only on `main` (or manual `workflow_dispatch`). The `backend` and `frontend` jobs stay on GitHub-hosted runners, so code from pull requests is never executed on the VM.
- The local Compose defaults (`optimizer:optimizer`) are for local/CI use only; production overrides `DATABASE_URL`, `CORS_ORIGINS`, and other values through `docker-compose.prod.yml` and the VM environment.
- The `production` environment can be configured with required reviewers or deployment branches for additional control.

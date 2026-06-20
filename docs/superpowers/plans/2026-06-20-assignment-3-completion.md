# Assignment 3 Completion Plan

> **For agentic workers:** This is a process/artifact-completion plan, not a feature plan. Steps are tracked with `- [ ]` checkboxes.

**Goal:** Close the remaining formal gaps so the repository and Week 3 report satisfy the Assignment 3 rubric, then submit the team PDF.

**Architecture:** Keep the existing MVP v1 code and stacked-PR structure unchanged; only update GitHub issue metadata, create board views, finalize reports, recreate the release on `main`, and package the Moodle submission.

**Tech Stack:** GitHub Issues / Projects / Milestones / Releases, Markdown reports, `gh` CLI (optional) or manual web UI, Docker Compose for the demo.

---

## Task 0: Collect required team and access information

**Files:** none (information needed before the rest can be finished)

- [ ] **Step 0.1: Gather the team roster**
  Collect for every team member:
  - Full name (as required by the university)
  - GitHub username
  - Scrum role (Product Owner, Scrum Master, Developer, etc.)
  - Assigned PBIs / user stories
  - Created PRs
  - Reviewed PRs and meaningful review comments

- [ ] **Step 0.2: Confirm GitHub access**
  Decide whether the team will:
  - Use the GitHub web UI to update issues / projects / releases manually, or
  - Provide a GitHub personal access token so the CLI/agent can automate updates.

- [ ] **Step 0.3: Confirm customer-review permissions**
  - Was the Sprint Review recorded?
  - Did the customer permit public publication of the transcript?
  - If not, did they permit private instructor sharing?
  - If neither, prepare `reports/week3/customer-review-notes.md` instead of `customer-review-transcript.md`.

---

## Task 1: Bring GitHub Issues into compliance

**Goal:** Every MVP v1 / Sprint 1 issue has the metadata Assignment 3 requires.

**Reference list (from `docs/user-stories.md`):**

User stories in Sprint 1:
- US-01a Vehicle route output — #18
- US-01b Vehicle arrival schedule — #19
- US-02 Loader route — #6
- US-03 Hard constraint validation — #7
- US-04 Docker execution — #8
- US-05 Algorithm time limit — #9
- US-06 Reproducible random seed — #10
- US-07 Objective function value — #11
- US-08 Planned routes overview — #12
- US-11 REST API for solver submission — #20
- US-12 React web frontend — #21

Supporting PBIs in Sprint 1 / MVP v1:
- PBI-01 CORS middleware — #30
- PBI-02 Expand JobRecord schemas — #31
- PBI-03 Extend JobStore — #32
- PBI-04 Validation wrapper service — #33
- PBI-05 Runner auto-validate/objective — #34
- PBI-06 Extend SolverService — #35
- PBI-07 New API endpoints — #36
- PBI-08 Stabilize e2e test — #37
- PBI-09 Dashboard API connection — #38
- PBI-10 New Job API connection — #39
- PBI-11 Job Detail API connection — #40
- PBI-12 Validate page API connection — #41
- PBI-13 Frontend Dockerfile/nginx — #42
- PBI-14 Docker Compose frontend service — #43
- PBI-15 SemVer release v1.0.0 — #44

- [ ] **Step 1.1: Verify the `mvp-v1` label and Sprint 1 milestone**
  Ensure every issue above has:
  - Label: `mvp-v1`
  - Milestone: `Sprint 1`

- [ ] **Step 1.2: Add / verify acceptance criteria**
  For every MVP v1 PBI (the 15 PBIs above and the Sprint 1 user stories), add at least three acceptance criteria in the issue description, using the checklist format:
  ```markdown
  ## Acceptance criteria
  - [ ] Criterion 1
  - [ ] Criterion 2
  - [ ] Criterion 3
  ```
  Acceptance criteria must be verifiable and specific (e.g., “`GET /jobs` returns 200 with a list of jobs”, “Frontend build passes with `npm run build`”).

- [ ] **Step 1.3: Assign every Sprint PBI to a team member**
  In GitHub, set the Assignee field on every Sprint 1 issue.

- [ ] **Step 1.4: Record a reviewer in each issue**
  Add a line near the top of each Sprint 1 issue description:
  ```markdown
  **Reviewer:** @github-username
  ```
  The reviewer must be a different team member than the assignee.

- [ ] **Step 1.5: Add Story Points**
  Ensure every qualifying PBI has a Story Points value recorded (e.g., in a custom field, a label like `sp-3`, or directly in the issue description). The README currently claims 34 total Story Points; verify the numbers sum to 34 or update the README.

- [ ] **Step 1.6: Update Work Status on issues**
  Set each Sprint 1 issue to the correct Work Status:
  - `Done` for implemented/reviewed/merged PBIs.
  - `In Progress` only for items still open.
  - `Ready` / `To Do` for backlog items not in the current Sprint.

- [ ] **Step 1.7: Sync `docs/user-stories.md` to the issue state**
  Update the `Work Status` column for every active story to match the issue state. Ensure removed stories (e.g., US-01) remain listed with status `Removed`.

---

## Task 2: Create inspectable backlog board views

**Goal:** Assignment 3 requires a saved Product Backlog view and a saved Sprint Backlog view.

- [ ] **Step 2.1: Create a GitHub Project for the repository**
  In the GitHub web UI:
  - Projects → New project → Board (or Table).
  - Link it to the repository issues.

- [ ] **Step 2.2: Build the Product Backlog view**
  Add a view named **Product Backlog** that shows all open issues grouped by **Work Status** (or by MoSCoW priority).

- [ ] **Step 2.3: Build the Sprint Backlog view**
  Add a view named **Sprint Backlog** filtered to Milestone = `Sprint 1`, grouped by **Work Status**.

- [ ] **Step 2.4: Add custom fields**
  Add at least the following custom fields in the project:
  - `Work Status` (single select: To Do, Ready, In Progress, Done)
  - `MoSCoW priority` (Must Have, Should Have, Could Have, Won't Have)
  - `Story Points` (number)
  - `MVP version` (single select: MVP v1, MVP v2, MVP v3)

- [ ] **Step 2.5: Update `reports/week3/README.md` board links**
  Replace the issue-search URLs with direct links to the two saved project views.

---

## Task 3: Finish the PR / merge workflow

**Goal:** Provide evidence of reviewed, issue-linked PRs and a merge-commit workflow.

Current stacked PRs (from `reports/week3/README.md`):
- Backend: #45 – #53
- Frontend: #54 – #58
- DevOps/docs: #59 – #60

- [ ] **Step 3.1: Ensure every PR is issue-linked**
  Each PR description must contain `Closes #<issue>` or `Part of #<issue>`. Verify or add the link.

- [ ] **Step 3.2: Assign reviewers and leave meaningful comments**
  Every open PR must have at least one reviewer assigned. Each reviewer should leave at least one meaningful review comment (not just “LGTM”).

- [ ] **Step 3.3: Obtain approvals**
  Every PR needs an approval from a team member other than the author.

- [ ] **Step 3.4: Merge using merge commits**
  Merge the PRs in order (backend stack first, then frontend, then DevOps/docs). Use **Create a merge commit**.

- [ ] **Step 3.5: Verify `main` is healthy**
  After all merges, run:
  ```bash
  .venv/Scripts/python -m pytest -q
  cd frontend && npm run build
  ```
  Both must pass before tagging.

---

## Task 4: Recreate the SemVer release on `main`

**Goal:** The `v1.0.0` release must point to the merged `main` branch, not to the release branch.

- [ ] **Step 4.1: Delete the existing draft/pre-release `v1.0.0`**
  If the release currently targets `44-release-v1.0.0`, delete or edit it.

- [ ] **Step 4.2: Create `v1.0.0` on the latest `main` commit**
  Use a tag `v1.0.0` on the merge commit at the tip of `main`.

- [ ] **Step 4.3: Write release notes**
  Include:
  - Summary of MVP v1 scope.
  - Links to key PRs / issues.
  - Docker Compose run instructions.
  - Link to the video demonstration (after it is recorded).

- [ ] **Step 4.4: Update `CHANGELOG.md`**
  Ensure `CHANGELOG.md` has a `## [1.0.0]` section matching the release notes.

---

## Task 5: Record and publish the MVP v1 demo video

**Goal:** A public, sanitized video shorter than two minutes demonstrating the delivered MVP v1.

- [ ] **Step 5.1: Prepare the demo script**
  Show in order:
  1. `docker compose up --build` (or the already-running local stack).
  2. Swagger UI at `http://localhost:8000/docs`.
  3. Submit a job via the frontend New Job page.
  4. View the job in the Dashboard.
  5. Open Job Detail and zoom/pan the route map.
  6. Run validation and show the validation report.

- [ ] **Step 5.2: Record the video**
  Use OBS, Loom, or similar. Keep it under 2 minutes.

- [ ] **Step 5.3: Upload to a public platform**
  YouTube (unlisted or public), Loom, or GitHub release asset. Ensure it is viewable without login.

- [ ] **Step 5.4: Add the link to the Week 3 report**
  Edit `reports/week3/README.md` and replace `*(link to be added after recording)*` with the real URL.

---

## Task 6: Capture screenshots

**Goal:** `reports/week3/images/` must contain the required screenshots.

- [ ] **Step 6.1: Product Backlog view**
  Screenshot the GitHub Project Product Backlog view.

- [ ] **Step 6.2: Sprint Backlog view**
  Screenshot the GitHub Project Sprint Backlog view.

- [ ] **Step 6.3: Sprint milestone page**
  Screenshot `https://github.com/Team-9-swp/Route-optimization-Platform-swp/milestone/2`.

- [ ] **Step 6.4: MVP v1 grouped/filtered view**
  Screenshot the project view grouped by `MVP version` or the `mvp-v1` label filter.

- [ ] **Step 6.5: SemVer release**
  Screenshot the `v1.0.0` release page.

- [ ] **Step 6.6: Delivered MVP v1**
  Two screenshots:
  - Swagger UI with a successful `/solve` response.
  - Web UI showing the Dashboard or Job Detail map.

- [ ] **Step 6.7: Example reviewed issue-linked PR**
  Screenshot a PR page showing the linked issue, reviewer, approval, and at least one review comment.

- [ ] **Step 6.8: Embed screenshots in `reports/week3/README.md`**
  Use relative Markdown image links:
  ```markdown
  ![Product Backlog](./images/product-backlog.png)
  ```

---

## Task 7: Complete the Week 3 report artifacts

- [ ] **Step 7.1: Fill the contribution traceability table**
  In `reports/week3/README.md`, replace the placeholder row with one row per team member containing:
  - Name
  - GitHub username
  - Role
  - Assigned issues/PBIs
  - Created PRs
  - Reviews and meaningful review comments

- [ ] **Step 7.2: Verify verification evidence numbers**
  Update the test counts in `reports/week3/README.md` to the current values:
  - Backend: `40 passed`
  - Frontend build: succeeds
  - Optionally add `npx tsc --noEmit` if run.

- [ ] **Step 7.3: Review and complete `customer-review-summary.md`**
  Ensure it contains: date, participants, artifacts demonstrated, scope reviewed, approvals/requested changes, risks, action points, and resulting backlog updates.

- [ ] **Step 7.4: Add customer transcript or notes**
  - If publication permitted: add `reports/week3/customer-review-transcript.md` and link it.
  - If only private sharing permitted: keep the transcript out of the repo and note this in `README.md`; prepare it for the Moodle PDF.
  - If neither: write `reports/week3/customer-review-notes.md` and link it instead.

- [ ] **Step 7.5: Review `reflection.md`, `retrospective.md`, and `llm-report.md`**
  Ensure each file covers the required sections and contains concrete, non-generic content.

- [ ] **Step 7.6: Verify all links in `reports/week3/README.md`**
  Every link must resolve. Fix or remove broken links.

---

## Task 8: Prepare the Moodle submission PDF

- [ ] **Step 8.1: Create the PDF content**
  Include:
  1. Project name and team number.
  2. Team-member table (names, GitHub usernames, roles, university identity mapping).
  3. Summary of contributions.
  4. Commit-hash permalink to `reports/week3/README.md` on `main`.
  5. Commit-hash permalink to the repository tree at the submission commit on `main`.
  6. Live links: Product Backlog view, Sprint Backlog view, Sprint milestone, MVP v1 view, SemVer release, delivered MVP v1 deployment, video demo.
  7. Live links: `docs/user-stories.md`, `Process_Requirements.md`, `docs/roadmap.md`, `docs/definition-of-done.md`, `CHANGELOG.md`.
  8. Links to reviewed issue-linked PRs.
  9. Exact access/run instructions.
  10. Customer recording link or transcript/notes (as permitted).
  11. Customer feedback summary and resulting backlog updates.

- [ ] **Step 8.2: Submit one PDF per team on Moodle**

---

## Task 9: Final repository validation

- [ ] **Step 9.1: Run the full test suite on `main`**
  ```bash
  .venv/Scripts/python -m pytest -q
  cd frontend && npm run build
  ```

- [ ] **Step 9.2: Run Docker Compose smoke test**
  ```bash
  docker compose up --build -d
  # verify http://localhost:8000/docs and http://localhost:3000 are reachable
  ```

- [ ] **Step 9.3: Check that all required files exist**
  ```bash
  ls docs/user-stories.md docs/roadmap.md docs/definition-of-done.md CHANGELOG.md reports/week3/README.md reports/week3/customer-review-summary.md reports/week3/reflection.md reports/week3/retrospective.md reports/week3/llm-report.md
  ```

- [ ] **Step 9.4: Confirm `main` is the protected default branch**
  The submission commit must be on `main`.

---

## Self-review checklist

- [ ] All 15+ qualifying PBIs have clear title, description, type, Work Status, MoSCoW, Story Points, milestone, assignee, and reviewer.
- [ ] Every MVP v1 PBI has ≥3 acceptance criteria.
- [ ] Product Backlog and Sprint Backlog saved views exist and are linked.
- [ ] All stacked PRs are reviewed, approved, and merged into `main` with merge commits.
- [ ] `v1.0.0` release points to `main`.
- [ ] `CHANGELOG.md` is current.
- [ ] Video is public and under two minutes.
- [ ] Required screenshots are in `reports/week3/images/` and embedded in README.
- [ ] Contribution table is filled.
- [ ] Moodle PDF contains all required elements.

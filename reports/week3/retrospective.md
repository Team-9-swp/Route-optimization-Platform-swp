# Sprint Retrospective

## What went well

1. **Decomposition into small PBIs** — splitting each user story into focused backend/frontend/devops PBIs made the work easy to review and kept PRs small.
2. **Automated test coverage** — backend pytest and frontend TypeScript/build checks caught regressions quickly before opening PRs.
3. **Stacked branching strategy** — basing each new branch on the previous open-PR branch let the team pull in dependencies without waiting for merges.

## What did not go well

1. **Rebasing stacked branches** — amending an earlier branch forced a rebase of all downstream branches; this was error-prone and required resolving conflicts.
2. **Late addition of the health endpoint** — the `/health` endpoint was initially missed from the endpoints PBI and had to be added after the branch was already in review.
3. **Missing project board** — relying on issue/milestone links made it harder for outsiders to see Sprint progress at a glance.

## Action points

1. Freeze the scope of branches once a PR is opened; if changes are needed, add them in a follow-up branch rather than amending.
2. Create a lightweight GitHub Project board for the next Sprint so the whole team and customer can see progress in one view.

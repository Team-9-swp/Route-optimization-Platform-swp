# Week 3 Reflection

## Learning points

- Migrating user stories into GitHub Issues with stable IDs preserved traceability while allowing technical decomposition into smaller PBIs.
- Defining acceptance criteria before implementation made PR review faster and reduced rework.
- Stacking PRs on top of each previous feature branch kept in-progress work isolated, but required careful rebasing when earlier branches were amended.
- Adding a solver time-limit parameter was essential for a stable e2e test and for frontend usability.
- TypeScript type checking caught several integration mismatches between the frontend and backend shapes early.

## Validated assumptions

- The FastAPI async job-store pattern is sufficient for MVP v1 traffic and keeps the backend simple.
- A single-page React app polling the backend is good enough for real-time job status updates in MVP v1.
- The existing `validator.py` can be wrapped cleanly for API use without changing its logic.

## Friction and gaps

- In-memory job storage means jobs are lost on container restart; this is acceptable for MVP v1 but must be addressed in MVP v2.
- The solver runtime for real instances can exceed CI timeout without configurable limits.
- No project board was configured; issue/milestone queries provided equivalent visibility but a dedicated board may be clearer for the team.
- Customer review was conducted online; a recorded session would provide stronger evidence.

## Planned response

- MVP v2 will introduce persistent storage (SQLite or PostgreSQL) and replace in-memory `JobStore`.
- Add route visualization and skipped-optional-orders reporting as planned follow-ups.
- Set up a GitHub Project board if the team finds milestone queries insufficient.
- Continue requiring acceptance criteria and test evidence before marking PBIs as Done.

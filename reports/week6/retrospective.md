# Week 6 Sprint Retrospective

**Date:** 2026-07-12
**Participants:** Team 9
**Project:** Route Optimization Platform 

## What Went Well

*   **Successful Trial Release (MVP v2):** Successfully deployed and tagged `v1.2.0` and `v1.3.0` (MVP v2). The product is runnable via Docker Compose, and a university VM deployment is in place, providing a tangible environment for customer access (even if limited).
*   **Comprehensive Documentation Review:** The team conducted a thorough review of key documentation, including `docs/customer-handover.md`, `README.md`, `CONTRIBUTING.md`, and `AGENTS.md`. This ensured alignment between the codebase, its purpose, and the handover strategy.
*   **Effective Customer Meeting:** The meeting provided critical insights into the customer's operational environment and their perceived value of the product.
*   **Clear Identification of Transition Blockers:** The primary blockers (network access limitations, live demo stability, feature completion for MVP v3) are now clearly defined and understood by the whole team.
*   **Strong CI/CD Pipeline:** Confidence in the CI process is high, evidenced by successful automated deployment from the `protected main` branch to the university VM.

## What Could Be Improved

*   **Customer Access and Verification:** The most critical improvement area is resolving the external accessibility issue. The current deployment is only reachable from the university network, preventing the customer from using the product in their daily workflow and limiting the value of our UAT.
*   **Demo and Handover Preparedness:** The team was aware of the deployment environment's constraints but a concrete, rehearsed plan for a stable live demonstration was lacking. This is a significant risk for the upcoming Week 8 Demo Day.
*   **UAT Scenario Execution:** While UAT scenarios are defined and maintained (`reports/` and `docs/`), executing them in a representative environment outside the campus network was not completed for this release.
*   **Transition Plan Granularity:** While the handover document exists, specific, actionable steps with clear owners and deadlines for the final transition (MVP v3) are not fully detailed.

## Action Items

| Action | Owner | Due Date |
| :--- | :--- | :--- |
| **Resolve deployment accessibility.** Investigate and implement an agreed solution (e.g., ngrok tunnel, internal VPN access) to make the deployed VM externally reachable for the customer. | Team Lead / DevOps | Week 7 Start |
| **Prepare and rehearse a pre-recorded demo.** Finalize a stable, 2-minute screen recording showcasing all MVP v3 features for the presentation. | All Team Members | Week 7 Lab Rehearsal |
| **Complete and review final UAT scenarios.** Execute the latest user acceptance tests based on the new `test_cases/` and provide feedback to the development team. | QA Lead | Week 7, Mid |
| **Finalize MVP v3 Features.** Address all remaining tasks for the next release, including the evaluation feature and any resulting fixes from the trial release. | Development Team | Week 7 End |
| **Refine the Handover Plan.** Create a detailed transition checklist (code, docs, credentials, access) and schedule a handover meeting with the customer. | All Team Members | Week 7 End |

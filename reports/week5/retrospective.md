# Sprint Retrospective - Week 5 (Sprint 5)

**Project:** Route Optimization Platform
**Team:** Team-9-swp
**Date:** 2026-07-05
**Sprint:** Sprint 5 — MVP v2 (following Assignment 4 Sprint: Quality & Reliability)

## 1. What Went Well

*   **Strong Foundation from Assignment 4:** The successful completion of Assignment 4 (Quality, Reliability, UAT) provided a robust and validated base. The transition to the PyVRP solver, the establishment of measurable Quality Requirements, and the passing of all 5 UAT scenarios gave us high confidence in the product's core stability before adding new features.
*   **Successful MVP v2 Feature Delivery:** We fully completed the critical MVP v2 features, including the validator-compatible solution export endpoint (`/export-solution`) and the reporting of skipped optional orders. These additions significantly enhance the product's practical value.
*   **Mature Workflow Adherence:** The team demonstrated strong discipline in following our refined Git workflow. All features were developed in dedicated branches, passed CI checks, and were merged via Pull Requests, minimizing integration conflicts.
*   **Effective ADR Utilization:** Creating and following Architecture Decision Records (ADRs) for key technical choices (e.g., export format) kept the team aligned and prevented technical drift.
*   **Customer-Centric Focus:** Leveraging the successful Assignment 4 UAT and the ngrok deployment, we presented the new features during the Sprint Review. The customer provided positive feedback, particularly on the usability of the export functionality and the continued quality of the solver.

## 2. What Could Be Improved

*   **Deployment Accessibility:** The university VM remains unreachable externally, requiring a temporary `ngrok` tunnel for every customer demonstration. This is a brittle process that could hinder feedback and adoption.
*   **Test Suite Execution Speed:** The full test suite (backend and frontend) takes longer than desired to run, slowing down the CI pipeline and local development feedback loops.
*   **Frontend Error Handling:** While the API now returns user-friendly error messages, the frontend does not always display them in an intuitive manner. Improving UI/UX for error feedback is needed.
*   **Definition of Done (DoD) Clarity:** There was a minor miscommunication regarding the DoD for the solution export feature, specifically concerning the level of data validation required in the endpoint.

## 3. Key Learnings

1.  **Quality Gates are Essential:** The hard work in Assignment 4 to define and implement quality requirements and a robust CI pipeline paid off. We could add new features with confidence, knowing that the core functionality was stable and tested.
2.  **Automation Pays Off:** Having a robust CI/CD pipeline (which we have) gives the team the confidence to release quickly and reliably.
3.  **Architecture Documentation is a Living Asset:** Our architecture documentation became a single source of truth, helping both the team and the customer understand the system.
4.  **Configuration Management is Critical:** Managing configuration for different environments (local, Docker, deployment) is a common challenge. Our approach with `.env` files works, but it requires constant vigilance and clear documentation.

## 4. Concrete Process Changes for the Next Sprint

1.  **Improve Deployment Strategy:** We will research and implement a more reliable and permanent externally accessible deployment solution to eliminate the dependency on `ngrok` for demos. **Action:** Create an issue to investigate solutions (e.g., cloud VM, more stable tunnel).
2.  **Optimize Test Suite:** We will refactor the test suite to speed up CI, potentially by moving slower integration tests to a separate job. **Action:** Create an issue for test performance optimization.
3.  **Improve Frontend UX:** We will dedicate time in the next sprint to improve the display of error messages and overall user feedback in the UI. **Action:** Add user stories to the backlog.
4.  **Refine the Definition of Done:** We will create a checklist in the Pull Request template to explicitly confirm that all DoD criteria are met before merging. **Action:** Update the `.github/PULL_REQUEST_TEMPLATE.md` file.

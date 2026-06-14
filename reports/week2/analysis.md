# Week 2 Analysis

## Learning Points

* During interface design, we initially considered a CLI sufficient for the current version. After further discussion, we decided to build a web user interface as the primary interface for MVP v1 because it improves usability for dispatchers and aligns with the customer's feedback that a web UI would be a valuable addition.
* The MVP v0 work showed that the current greedy algorithm can already generate valid solutions and outperform the provided baseline solutions.
* Customer feedback helped identify possible improvement directions: VRP solvers, server-side computation, route visualization, and a web interface.
* Separating the solver into a FastAPI microservice makes it easier to support both the web UI and direct API usage.

## Validated Assumptions

* We assumed that the current greedy algorithm could serve as the foundation of MVP v0. This was confirmed through testing and discussion with the customer.
* We assumed that the proposed user stories and MoSCoW priorities reflected the main user needs. The customer reviewed and approved them.
* We assumed that route visualization would help analyze solution quality. The customer supported this idea.
* We assumed that a web interface would be a desirable addition. The customer confirmed this in the meeting.

## Needs Clarification

* ~~Which environment and university computing resources will be used for deployment.~~ Resolved: the MVP v0 service is hosted on the university VM at `http://10.93.26.188:8000`.
* Which approach will produce the best results on large scenarios: PyVRP, OR-Tools, or the current algorithm.
* How loader schedules should be integrated with vehicle routes when using an external VRP solver.
* ~~Whether the customer will grant public permission to publish the sanitized meeting transcript.~~ Permission was granted.

## Planned Response

* Implement a React + TypeScript web UI and document it in `docs/interface.md`.
* Keep Docker execution for **US-04** and extend the Docker Compose setup to include the frontend.
* Continue improving vehicle and loader routes for **US-01** and **US-02**.
* Integrate the validator into the service and UI for **US-03**.
* Test PyVRP and OR-Tools on large scenarios and compare them with the current solver.



# Week 2 Analysis

## Learning Points

* During interface design, we learned that a CLI is sufficient for the current version, while a web interface can be added later.
* The MVP v0 work showed that the current greedy algorithm can already generate valid solutions and outperform the provided baseline solutions.
* Customer feedback helped identify possible improvement directions: VRP solvers, server-side computation, and route visualization.

## Validated Assumptions

* We assumed that a CLI would be sufficient for the first version of the product. The customer confirmed this.
* We assumed that the current greedy algorithm could serve as the foundation of MVP v0. This was confirmed through testing and discussion with the customer.
* We assumed that the proposed user stories and MoSCoW priorities reflected the main user needs. The customer reviewed and approved them.
* We assumed that route visualization would help analyze solution quality. The customer supported this idea.

## Needs Clarification

* Which environment and university computing resources will be used for deployment.
* Which approach will produce the best results on large scenarios: PyVRP, OR-Tools, or the current algorithm.
* How loader schedules should be integrated with vehicle routes when using an external VRP solver.

## Planned Response

* Keep the CLI and Docker execution as the main MVP v1 interface for **US-04** and document it in `docs/interface.md`.
* Continue improving vehicle and loader routes for **US-01** and **US-02**.
* Test PyVRP and OR-Tools on large scenarios and compare them with the current solver.



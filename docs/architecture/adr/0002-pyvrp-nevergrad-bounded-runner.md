# ADR-0002: Use a PyVRP + Nevergrad solver pipeline inside a bounded async job runner

- **Status:** Accepted
- **Date:** 2026-07-04
- **Addresses quality requirements:** [QR-FC-01 — Solver Functional Correctness](../../quality-requirements.md), [QR-PE-01 — Solver Time Behaviour](../../quality-requirements.md)

## Context

The core product value is a correct, well-optimized solution to the BIA CVRPTW variant (vehicles, drivers, loaders, time windows, optional orders). Two quality requirements constrain the solver directly:

- **QR-FC-01:** every returned solution must pass the project validator with zero hard-constraint violations for supported inputs.
- **QR-PE-01:** a fixed reference instance must be solved and validated within a predictable time budget (the configured `time_limit`, and the 900-second CI benchmark ceiling), and the job must reach a terminal state instead of hanging.

The team previously experimented with a hand-rolled metaheuristic and a separate greedy stage. That made solution quality and runtime hard to reason about and made the pipeline brittle. We needed an engine with strong VRP support and a predictable termination behaviour, plus a way to tune it without hand-tuning parameters per instance.

## Decision

We adopt **PyVRP** as the route-optimization engine, tuned with **Nevergrad**, and run it through an **asynchronous job runner** that enforces a bounded time budget.

Concretely:

- The solver pipeline is implemented at the repository root (`solver.py`) and integrated through `app/runner.py`, which exposes solve execution to the service layer (`app/service.py`).
- The runner accepts a `time_limit` and a `seed`, enforces the runtime budget, and always drives the job to a terminal state (`completed`, `failed`, or timeout-handled) rather than leaving it in progress indefinitely.
- Nevergrad is used to search solver parameters/seeds so that quality is improved without per-instance manual tuning.
- Every solver result is validated by the project validator (`app/validation.py`); the solution is only accepted as a success when it passes with zero hard-constraint violations.
- Skipped optional orders are reported back through the job result (`unserved_optional`), so correctness evidence includes optional-order handling.

## Consequences

- **Positive:** Functional correctness is enforced by the validator gate, satisfying QR-FC-01.
- **Positive:** Runtime is bounded by the configured limit and reaches a controlled terminal state, satisfying QR-PE-01.
- **Positive:** PyVRP gives a well-maintained, high-quality VRP core; Nevergrad removes manual parameter tuning.
- **Negative:** The product depends on PyVRP and Nevergrad as external libraries; their release changes must be tracked.
- **Negative:** Large instances can still exceed practical runtime; the current QRT threshold is scoped to the fixed reference fixture, and large-instance benchmarking remains separate backlog work.

## Alternatives considered

- **Custom metaheuristic only:** rejected because correctness and runtime were harder to guarantee and maintain.
- **External optimization service / MILP solver:** rejected for this increment because of deployment complexity and the need for the customer to run the system directly.

## Follow-up work

Sprint 5 includes investigating a more joint optimization approach and a column-generation research spike (issues for "Re-evaluate solver pipeline and greedy-stage impact" and "Investigate column generation for route optimization"). Any decision to replace or significantly alter this pipeline will be recorded as a new ADR that supersedes this one.

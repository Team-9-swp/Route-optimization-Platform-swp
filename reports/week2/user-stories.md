## US-01: Vehicle route and schedule

**Requirement status:** Active
**MoSCoW priority:** Must Have

As a driver,
I want to receive my route and order visit schedule,
so that I can arrive at orders within the allowed time windows.

### Notes and constraints

The vehicle route must respect time windows, vehicle capacity, shift duration, and depot start/end requirements.

---

## US-02: Loader route

**Requirement status:** Active
**MoSCoW priority:** Must Have

As a loader,
I want to receive the list of orders I need to visit,
so that I can arrive on time at orders where unloading assistance is required.

### Notes and constraints

Loaders should be assigned only to orders where the required number of loaders is greater than zero.

---

## US-03: Hard constraint validation

**Requirement status:** Active
**MoSCoW priority:** Must Have

As a dispatcher,
I want to see whether the solution violates any hard constraints,
so that I do not submit an invalid solution.

### Notes and constraints

The solution should be checked against time windows, vehicle capacity, shift duration, route structure, and required loader availability.

---

## US-04: Docker execution

**Requirement status:** Active
**MoSCoW priority:** Must Have

As a technical user,
I want to run the solver through Docker,
so that I can get a reproducible execution without manual environment setup.

### Notes and constraints

The Docker command should allow the user to provide input and output file paths.

---

## US-05: Algorithm time limit

**Requirement status:** Active
**MoSCoW priority:** Should Have

As a project manager,
I want to set the algorithm time limit,
so that the solver finishes within the project constraints.

### Notes and constraints

The time limit may be provided as a CLI parameter, for example `--time-limit 900`.

---

## US-06: Reproducible random seed

**Requirement status:** Active
**MoSCoW priority:** Should Have

As a developer,
I want to set a random seed,
so that repeated runs of the algorithm can produce reproducible results.

### Notes and constraints

This is important for stochastic methods such as simulated annealing, ALNS, PyVRP, or parameter tuning.

---

## US-07: Objective function value

**Requirement status:** Active
**MoSCoW priority:** Should Have

As a manager,
I want to see the objective function value of the generated solution,
so that I can evaluate the route cost and compare different runs.

### Notes and constraints

The objective value may be calculated by the official validator or by an internal evaluator.

---

## US-08: Planned routes overview

**Requirement status:** Active
**MoSCoW priority:** Should Have

As a dispatcher,
I want to see all planned vehicle and loader routes,
so that I can monitor the delivery execution plan.

### Notes and constraints

For MVP, the overview may be represented as structured JSON or textual output; a graphical interface is not mandatory.

---

## US-09: Skipped optional orders report

**Requirement status:** Active
**MoSCoW priority:** Could Have

As a manager,
I want to see a list of skipped optional orders,
so that I can understand which orders were not completed and why.

### Notes and constraints

Skipped optional orders may be identified from orders that are absent from the generated routes.

---

## US-10: Route visualization

**Requirement status:** Active
**MoSCoW priority:** Could Have

As a dispatcher,
I want to see route visualization on a coordinate plane,
so that I can analyze solution quality faster.

### Notes and constraints

Visualization is not required for the core solver and can be added as an additional analysis feature.



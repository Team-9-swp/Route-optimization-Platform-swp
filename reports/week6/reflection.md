# Week 6 Reflection

**Project:** Route Optimization Platform
**Team:** Team-9-swp
**Date:** 2026-07-12

## Learning points

1. **Determinism is a prerequisite for customer trust.** Non-deterministic solver results undermine the customer's ability to validate and benchmark the system. The team learned that fixing determinism early was essential for the customer's willingness to accept the product. The fix (passing seed 42 to Nevergrad) was straightforward once the root cause was identified.

2. **Self-deployment is the preferred handover model.** The customer preferred self-deployment (deploying from the repository independently) over a demo-only handover. This ensures the customer has full control and can make future modifications. The team learned that providing a single-container deployment with full UI is the right approach for this customer.

3. **Algorithm architecture communication builds trust.** Explaining the solver architecture (Nevergrad → PyVRP → greedy loader assignment → simulated annealing) to the customer helped them understand the system's internals and made the baseline comparison more meaningful. Technical transparency is valuable for customer confidence.

4. **Concise meetings are effective.** The Sprint Review was ~20 minutes and focused. Short, focused meetings with clear agendas are more effective than lengthy discussions. The team should continue this approach for future customer interactions.

## Validated assumptions

1. **The customer will deploy independently.** The team assumed the customer would prefer self-deployment, and the meeting confirmed this. The customer explicitly said "I'll deploy it and try then during next week" and "spin everything up through a single container without any shamanism."

2. **Seed 42 produces deterministic results.** The team assumed that passing a fixed seed to Nevergrad would resolve non-determinism. The customer confirmed this during the meeting — the algorithm now produces identical results on the same input.

3. **The baseline can be beaten.** The team assumed the solver improvements (optional order skipping probability, driver return-to-depot) would improve objective values. The meeting confirmed a ~0.5% improvement on test case 4.

4. **The customer understands the product scope.** The team assumed the customer understood the difference between algorithm-only and full UI delivery. The meeting confirmed the customer wants "with a wrapper, of course" — the full web interface.

## Friction and gaps

1. **Driver return-to-depot edge case discovered late.** The cost-calculation issue (routes split by zeros counted as separate drivers) was identified during the Sprint Review rather than during development or testing. This suggests insufficient integration testing of the solver output format.

2. **Gantt chart progress unclear.** Although the Gantt chart was confirmed as in-scope for Sprint 4, it was not demonstrated during the review. The team does not have clear visibility into its status.

3. **Feature status communication gap.** The customer asked about calculation time on dashboard and was told it was "already there by status" but it was unclear whether it was fully implemented or just planned. This created confusion about what is actually delivered.

4. **Customer-facing documentation review was not explicitly conducted.** The assignment required a documentation review during the Week 6 meeting, but the meeting focused on transition-readiness and algorithm details. The customer expressed general confidence ("I hope everything is transparent") but did not walk through specific documentation pages.

5. **Meeting platform risk.** The customer may have limited network access next week, requiring a switch to Zoom. This was not anticipated and could affect future meeting reliability.

## Planned response

1. **Add determinism verification to CI.** Run the solver twice with the same seed and assert identical results to prevent regressions. This directly addresses the friction of discovering non-determinism late.

2. **Fix driver return-to-depot cost calculation.** Investigate and fix the routes-split-by-zeros edge case. This addresses the late-discovered bug and improves solver output accuracy.

3. **Complete Gantt chart visualisation.** Ensure the Gantt chart is demonstrable by the end of Sprint 5. Assign clear ownership and track progress.

4. **Improve feature status communication.** Before customer meetings, verify that each feature's implementation status is clearly communicated (implemented vs. planned vs. in-progress). This prevents ambiguity.

5. **Conduct explicit documentation review in Week 7.** Since the documentation review was not conducted in Week 6, schedule it for the Week 7 meeting. Ask the customer to review README, customer-handover, and deployment docs specifically.

6. **Prepare Zoom fallback.** Verify Zoom works for all participants before the Week 7 meeting. Have a backup communication plan if Zoom fails.

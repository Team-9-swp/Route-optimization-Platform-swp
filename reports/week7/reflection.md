# Week 7 Reflection

## Learning points

Sprint 5 showed that final delivery is both a product and evidence problem. The merged maintenance and frontend changes ([PR #200](https://github.com/Team-9-swp/Route-optimization-Platform-swp/pull/200), [PR #205](https://github.com/Team-9-swp/Route-optimization-Platform-swp/pull/205), and [PR #207](https://github.com/Team-9-swp/Route-optimization-Platform-swp/pull/207)) prepared the MVP v3 product state, while the handover, UAT, and report work made its real transition status understandable.

Customer-facing completion required more than listing features. The team had to state how to run and deploy the stack, what support ends with the course, what limitations remain, and which claims are supported. The final confirmation established that the documentation set, transition model, corrections, and reached scope are accepted.

The most important distinction is between **readiness**, **acceptance**, and **operation**. `Ready for independent use` says the product and instructions are prepared. `Accepted` says the customer accepted the documented result and handover scope. Neither statement proves that the customer deployed, health-checked, operated, or reproduced the product independently.

## Validated assumptions

- Small UI improvements improve customer interpretation: actual execution duration and readable Objective formatting were completed in [#201](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/201) and [#202](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/202).
- A combined route/schedule view is a useful final-state improvement, implemented in [#203](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/203).
- Source plus Docker Compose is an appropriate handover path for the customer's internal/local-use model; permanent public hosting is not required.
- Customer acceptance can be recorded honestly while keeping customer-side execution as `Not executed` in the [UAT record](../../docs/user-acceptance-tests.md#week-7-review-record).
- The final course product state can correspond to MVP v3 while the latest published release remains `v1.4.0` and final packaging stays open in [#190](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/190).

## Friction and gaps

- The Sprint size and overlapping issue structure needed a late audit; [#183](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/183) records the canonical 73 SP calculation.
- The finished visualization was merged after the customer meeting, so repository verification cannot be presented as customer-executed UAT.
- Customer-side reproduction remains unverified even though the documentation and reached transition scope are accepted.
- Some closed issues retained stale work-status text, weakening traceability.
- The expected dedicated solver determinism regression from [#185](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/185) was not readily identifiable during the final repository audit.
- The final release, screenshots, stable commit permalinks, and Moodle-only wrapper/evidence are still pending in [#190](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/190) and [#194](https://github.com/Team-9-swp/Route-optimization-Platform-swp/issues/194).

## Planned response

- Keep the [customer handover](../../docs/customer-handover.md), [roadmap](../../docs/roadmap.md), and [UAT record](../../docs/user-acceptance-tests.md) aligned with the accepted status and actual operational evidence.
- Complete release packaging only through #190 after the final branch state, checks, and review are satisfied; do not pre-announce a version.
- Add real screenshots and commit-hash permalinks to the Moodle evidence through #194 without fabricated files or broken links.
- Keep the public sanitized demo separate from private Sprint Review and rehearsal artifacts.
- If maintenance continues after the course, prioritize an inspectable determinism regression and keep dependencies, Compose guidance, and security patches current.

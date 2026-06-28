# Week 4 Reflection

## Learning points

The team learned that customer feedback must be converted into explicit backlog decisions rather than stored only in meeting notes. Each important feedback point should result in an implementation issue, an investigation issue, or a documented deferral reason.

The team also learned that quality requirements must be measurable. General statements such as “the solver should be fast” are not sufficient. Stable IDs, thresholds, test conditions, rationale, and automated QRT links make quality expectations verifiable.

Deployment accessibility is part of product quality. A working university VM is not sufficient when the customer cannot access it from their location.

The team also learned that documentation is not a replacement for executable evidence. QRT specifications must be supported by real automated tests and passing CI runs.

Finally, the failed meeting recording showed that evidence collection requires the same preparation as product work.

## Validated assumptions

* Docker can serve as a fallback method for running the product locally.
* The university-network-only deployment is insufficient for customer UAT.
* Customer feedback can be traced effectively through GitHub issues and pull requests.
* Broad solver-refactoring work should be split into smaller measurable investigations.
* The current quality requirements can be expressed using different ISO/IEC 25010 sub-characteristics.

The assumption that the greedy stage is responsible for weaker solver results has not yet been validated. Issue #97 was created to test it through baseline comparison.

The assumption that a more joint optimization approach will improve results has also not been validated and remains investigation work under #23.

## Friction and gaps

* Customer access to the deployed product is blocked outside the university network.
* Customer-executed UAT is incomplete.
* The Sprint Review recording was not saved.
* Final automated QRT implementations are incomplete.
* Protected-main CI evidence is incomplete.
* Some pull requests depend on earlier unmerged branches.
* GitHub Project access is limited.
* Solver quality relative to the baseline still requires reproducible measurement.
* The final release, changelog, deployment evidence, and report index are not complete.

## Planned response

* Complete external or explicitly agreed customer access under #90.
* Conduct at least three customer-executed UAT scenarios under #91.
* Conduct a recorded follow-up Sprint Review and complete #92.
* Implement automated QRTs and CI evidence under #88.
* Complete and review the quality specifications under #87.
* Compare the solver with the baseline and analyze the greedy stage under #97.
* Continue broader solver investigation under #23.
* Rebase dependent documentation branches after earlier pull requests are merged.
* Update the Week 4 report with final UAT, CI, release, and Sprint Review evidence.

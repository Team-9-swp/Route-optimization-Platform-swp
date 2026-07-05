# LLM Usage Report — Week 5 (Assignment 5)

## Tools Used

The team continued using the same AI tools established in Week 4:

* **ChatGPT** for planning, document drafting, requirement analysis, and review checklists;
* **OpenAI Codex** for repository inspection, issue updates, Markdown file creation, branch creation, commits, and pull-request preparation.

## Usage During Assignment 5 (MVP v2)

AI tools were used to assist with:

### Planning and Requirements
* interpreting Assignment 5 requirements and MVP v2 scope;
* refining the Sprint 5 backlog based on customer feedback from Assignment 4 UAT;
* creating and updating issues for MVP v2 features (#126, #130, #111, #112, #113);
* tracing customer feedback from Assignment 4 to new backlog items.

### Implementation Support
* drafting code structure for the `/export-solution` endpoint (#126);
* generating unit test skeletons and mock objects for the new export functionality;
* suggesting error handling improvements for user-friendly API responses;
* generating realistic test JSON payloads for API validation logic.

### Documentation
* drafting Architecture Decision Records (ADRs) for key technical decisions (#113);
* documenting the development process and configuration management strategy (#111);
* creating architecture, dataflow, and domain model PlantUML diagrams;
* preparing the hosted documentation site structure and content;
* drafting the Week 5 retrospective report (`retrospective.md`);
* drafting the Week 5 reflection report (`reflection.md`);
* drafting the LLM usage report (`llm-report.md`).

### Process and Reporting
* preparing the Sprint Review notes and summary structure;
* drafting issue and pull-request descriptions;
* checking whether required document sections were present;
* identifying missing links, reviews, CI evidence, and deployment-access requirements;
* creating focused follow-up PBIs from broad customer feedback.

### Video and Release Preparation
* outlining the public sanitized demo video script and key talking points;
* drafting the SemVer release description for MVP v2 (v1.2.0);
* verifying that public documents contain no private information.

## Human Contribution and Verification

Team members remained responsible for:

* deciding the actual Sprint 5 scope and priorities;
* confirming customer feedback from real meeting notes and UAT results;
* selecting priorities, Story Points, implementers, and reviewers;
* reviewing AI-generated requirements and thresholds;
* verifying issue and pull-request links;
* checking repository changes before merge;
* approving pull requests;
* implementing and testing the product (including `/export-solution` endpoint);
* conducting customer meetings and Sprint Review;
* confirming that public documents and videos contain no private information;
* deciding whether AI suggestions were appropriate for the project;
* **recording the public sanitized demo video** and verifying its content;
* **creating the hosted documentation site** and ensuring all links work;
* **conducting the Sprint Retrospective** and validating all findings.

AI-generated content was not treated as evidence by itself. Repository files, issues, pull requests, automated tests, CI runs, deployment results, customer feedback, UAT results, the hosted documentation site, and the public demo video remain the authoritative project evidence.

## Limitations and Corrections

AI tools did not have complete knowledge of the final product state unless repository information was explicitly checked.

The team corrected or rejected AI suggestions when they:

* described unfinished work as completed (e.g., claimed `/export-solution` was already deployed before it was implemented);
* assumed that a recording, hosted documentation, or UAT result existed before it was completed;
* used incorrect issue statuses or milestone assignments;
* suggested closing issues before review and merge;
* required repository permissions that were not available;
* produced generic text that was not supported by project evidence;
* generated code that was suboptimal or did not align with our architecture decisions (e.g., incorrect validation logic for the export endpoint);
* suggested unrealistic timelines or scope for MVP v2 features.

No customer feedback, approval, recording permission, UAT result, CI result, test measurement, or evidence of hosted documentation was intentionally fabricated.

## Responsible Use

The team reviewed AI-generated content before committing it. Sensitive credentials, private recording links, university emails, customer-identifying information, and private access instructions were excluded from the public repository.

## Key Differences from Week 4

| Aspect | Week 4 (Assignment 4) | Week 5 (Assignment 5) |
|--------|----------------------|----------------------|
| **Primary Focus** | Quality, reliability, and UAT | Documentation, reflection, and MVP v2 features |
| **LLM Main Role** | Requirements interpretation and quality gates | Documentation drafting and reporting |
| **New LLM Use** | Drafting quality requirements and UAT scenarios | Drafting ADRs, architecture diagrams, and hosted documentation |
| **Human Critical Work** | Implementing solver transition and CI/CD | Recording demo video and hosting documentation site |
| **Verification Emphasis** | UAT execution and CI evidence | Documentation links, video content, and release artifacts |

## Conclusion

In Week 5, LLM tools continued to serve as valuable assistants for drafting, planning, and reporting tasks. The team maintained a disciplined approach of "generate, review, validate, and commit," ensuring that all AI-generated content was verified against actual project evidence. The successful delivery of MVP v2, including the hosted documentation site and public demo video, was achieved through effective collaboration between human expertise and AI-assisted productivity.

param(
    [string]$Repository = "Team-9-swp/Route-optimization-Platform-swp"
)

$ErrorActionPreference = "Stop"

if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    throw "GitHub CLI 'gh' is required. Install it and run 'gh auth login' before running this script."
}

gh auth status | Out-Null

$EmDash = [char]0x2014
$MilestoneTitle = "Sprint 5 $EmDash MVP v2"
$MilestoneDue = "2026-07-05T00:00:00Z"
$MilestoneDescription = @"
## Sprint

Assignment 5 $EmDash Sprint 5

## Sprint dates

- Start: 2026-06-29
- Finish: 2026-07-05

## Sprint Goal

Deliver MVP v2 with improved solution usability and maintainability by fixing validator-compatible JSON export, improving loader workload distribution, adding Gantt schedule visualization, investigating stronger optimization approaches, documenting the architecture and development process, and automating deployment from the protected main branch.

## Planned outcome

A customer-accessible MVP v2 increment with selected product improvements, updated architecture and development-process documentation, extended testing and CI evidence, hosted documentation, UAT evidence, Sprint Review evidence, and a SemVer release from the protected default branch.
"@

function Ensure-Label {
    param(
        [string]$Name,
        [string]$Color,
        [string]$Description
    )

    $encoded = [System.Uri]::EscapeDataString($Name)
    try {
        gh api "repos/$Repository/labels/$encoded" | Out-Null
    }
    catch {
        gh api "repos/$Repository/labels" `
            -X POST `
            -f name="$Name" `
            -f color="$Color" `
            -f description="$Description" | Out-Null
    }
}

Ensure-Label -Name "assignment-5" -Color "5319E7" -Description "Work selected for Assignment 5 / Sprint 5"
Ensure-Label -Name "To Do" -Color "CCCCCC" -Description "Work Status or requirement status"
Ensure-Label -Name "priority: must-have" -Color "B60205" -Description "MoSCoW priority: Must Have"
Ensure-Label -Name "priority: should-have" -Color "FBCA04" -Description "MoSCoW priority: Should Have"
Ensure-Label -Name "priority: could-have" -Color "C2E0C6" -Description "MoSCoW priority: Could Have"

$milestones = gh api "repos/$Repository/milestones?state=all&per_page=100" | ConvertFrom-Json
$milestone = $milestones | Where-Object { $_.title -eq $MilestoneTitle } | Select-Object -First 1

if (-not $milestone) {
    $milestone = gh api "repos/$Repository/milestones" `
        -X POST `
        -f title="$MilestoneTitle" `
        -f description="$MilestoneDescription" `
        -f due_on="$MilestoneDue" | ConvertFrom-Json
}

Write-Host "Milestone: $($milestone.html_url)"

$issues = @(
    [pscustomobject]@{ Title = "A5-01: Refine Product Backlog and plan Sprint 5"; Implementer = "belelvser"; Reviewer = "Adelevere"; SP = "3"; Priority = "Must Have"; Expected = "The Product Backlog is refined, Sprint 5 is planned for MVP v2, and selected PBIs are traceable through GitHub Issues, the Sprint 5 milestone, the GitHub Project, and docs/roadmap.md."; Criteria = @("Sprint 5 milestone contains dates, Sprint Goal, and selected PBIs.", "Every selected PBI has outcome, acceptance criteria, Story Points, implementer, different reviewer, priority, MVP version, and Work Status.", "Sprint 5 Backlog view contains all milestone issues.", "docs/roadmap.md describes Sprint 5, MVP v2, and expected next work.") },
    [pscustomobject]@{ Title = "A5-02: Trace and respond to MVP v1 customer feedback"; Implementer = "belelvser"; Reviewer = "Adelevere"; SP = "2"; Priority = "Must Have"; Expected = "Customer feedback from MVP v1 and Assignment 4 is reviewed, linked to Sprint 5 scope or deferred with rationale, and reflected in the Week 5 report."; Criteria = @("Available MVP v1 and Assignment 4 feedback is reviewed before Sprint 5 implementation decisions are finalized.", "Feedback selected for MVP v2 is linked to Sprint 5 PBIs.", "Deferred feedback has a documented reason and follow-up backlog link where useful.", "Week 5 public or Moodle evidence contains a feedback response table without exposing private data.") },
    [pscustomobject]@{ Title = "A5-03: Document development process and configuration management"; Implementer = "whateverwillbewillbe"; Reviewer = "FuFill"; SP = "3"; Priority = "Must Have"; Expected = "The repository documents the maintained development workflow and configuration-management rules used for MVP v2."; Criteria = @("Development-process documentation describes branch, issue, review, CI, and release workflow.", "Configuration-management documentation covers environment variables, Docker configuration, dependencies, migrations, and secret handling.", "Required evidence and traceability locations are documented.", "Documentation avoids private credentials and private customer information.") },
    [pscustomobject]@{ Title = "A5-04: Document static, dynamic, and deployment architecture views"; Implementer = "whateverwillbewillbe"; Reviewer = "Aydar-art"; SP = "5"; Priority = "Must Have"; Expected = "The architecture documentation explains MVP v2 through static, dynamic, and deployment views that match the implemented system."; Criteria = @("Static view describes main backend, frontend, database, solver, validator, and deployment components.", "Dynamic view covers the solve/export/validate workflow and the deployment workflow.", "Deployment view shows Docker-based services, protected-main CI, deployment target, and external access boundaries.", "Architecture views are linked from the documentation index and reviewed by a different team member.") },
    [pscustomobject]@{ Title = "A5-05: Create and link Architecture Decision Records"; Implementer = "whateverwillbewillbe"; Reviewer = "FuFill"; SP = "3"; Priority = "Must Have"; Expected = "At least three Architecture Decision Records document important MVP v2 technical decisions and are linked to the architecture documentation."; Criteria = @("At least three ADRs are added under a maintained ADR location.", "Each ADR has context, decision, consequences, and status.", "ADRs cover meaningful MVP v2 architecture, deployment, solver, or documentation decisions.", "Architecture documentation links to the ADRs.") },
    [pscustomobject]@{ Title = "A5-06: Extend testing, QA, and Definition of Done for MVP v2"; Implementer = "FuFill"; Reviewer = "whateverwillbewillbe"; SP = "5"; Priority = "Must Have"; Expected = "Testing, QA documentation, and Definition of Done are updated so MVP v2 changes have clear quality expectations and evidence."; Criteria = @("MVP v2 test strategy identifies required unit, integration, frontend, UAT, and regression coverage.", "Definition of Done includes validation, review, documentation, CI, and release expectations for Sprint 5.", "New product PBIs identify required automated or UAT coverage.", "CI and QA evidence locations are documented without inventing test results.") },
    [pscustomobject]@{ Title = "A5-07: Deploy and release MVP v2"; Implementer = "FuFill"; Reviewer = "whateverwillbewillbe"; SP = "5"; Priority = "Must Have"; Expected = "MVP v2 is deployed from protected main, verified, documented, and published as a SemVer release."; Criteria = @("Deployment uses a protected main commit after required CI checks pass.", "Customer-accessible deployment or agreed access method is documented.", "Release notes link the Sprint 5 milestone, relevant evidence, and changelog entry.", "No private credentials, private access details, or private recording links are published.") },
    [pscustomobject]@{ Title = "A5-08: Update and execute MVP v2 UAT scenarios"; Implementer = "Aydar-art"; Reviewer = "FuFill"; SP = "3"; Priority = "Must Have"; Expected = "MVP v2 UAT scenarios are updated, executed with customer-relevant workflows, and linked to sanitized evidence."; Criteria = @("UAT scenarios cover selected MVP v2 product changes.", "Expected results and actual results are recorded.", "Defects or follow-up feedback are linked to backlog items.", "Public evidence is sanitized and private evidence is kept only in approved private submission locations.") },
    [pscustomobject]@{ Title = "A5-09: Conduct Sprint 5 Review"; Implementer = "Aydar-art"; Reviewer = "belelvser"; SP = "3"; Priority = "Must Have"; Expected = "Sprint 5 Review is conducted with MVP v2 evidence, customer feedback, and backlog follow-up decisions."; Criteria = @("Sprint Review agenda and demonstrated scope are documented.", "Customer or stakeholder feedback is recorded with sanitized public notes.", "Accepted, rejected, and deferred outcomes are linked to Sprint 5 PBIs or future backlog items.", "Review evidence is linked from the Week 5 report.") },
    [pscustomobject]@{ Title = "A5-10: Conduct Sprint Retrospective"; Implementer = "Adelevere"; Reviewer = "belelvser"; SP = "2"; Priority = "Must Have"; Expected = "The team conducts a Sprint Retrospective and records actionable improvement items for future work."; Criteria = @("Retrospective notes summarize what went well, what was difficult, and what to improve.", "Action items have owners or follow-up locations.", "Private or sensitive discussion is not published.", "Retrospective summary is linked from Week 5 evidence.") },
    [pscustomobject]@{ Title = "A5-11: Publish hosted documentation"; Implementer = "Adelevere"; Reviewer = "whateverwillbewillbe"; SP = "3"; Priority = "Must Have"; Expected = "Project documentation is hosted and publicly accessible without exposing private data."; Criteria = @("Documentation site builds from repository documentation sources.", "Hosted documentation link is public and verified.", "Architecture, development-process, testing, ADR, deployment, and user-facing evidence pages are reachable.", "Hosting instructions or workflow are documented.") },
    [pscustomobject]@{ Title = "A5-12: Write Week 5 reflection"; Implementer = "Adelevere"; Reviewer = "belelvser"; SP = "2"; Priority = "Must Have"; Expected = "Week 5 reflection documents team learning, contribution, process observations, and responsible use of tools."; Criteria = @("Reflection covers Sprint 5 planning, implementation, quality, deployment, and teamwork.", "Individual or team contributions are described accurately.", "Reflection does not claim unverified work as complete.", "Reflection is linked from Week 5 public or Moodle report as appropriate.") },
    [pscustomobject]@{ Title = "A5-13: Record public MVP v2 demo video"; Implementer = "Adelevere"; Reviewer = "FuFill"; SP = "2"; Priority = "Must Have"; Expected = "A public sanitized demo video shows the MVP v2 increment and is linked from Week 5 evidence."; Criteria = @("Demo covers selected MVP v2 features and workflow.", "Recording contains no private credentials, customer private data, or private access links.", "Public video link is verified before submission.", "Demo is linked from the Week 5 public report and release evidence where appropriate.") },
    [pscustomobject]@{ Title = "A5-14: Prepare Assignment 5 LLM usage report"; Implementer = "Adelevere"; Reviewer = "belelvser"; SP = "1"; Priority = "Must Have"; Expected = "Assignment 5 LLM usage is documented transparently with prompts, outputs, human decisions, and limitations."; Criteria = @("LLM usage report identifies where LLM tools were used.", "Important prompts, generated outputs, and human validation steps are summarized.", "The report distinguishes completed work from suggestions or drafts.", "No private credentials, tokens, or private customer data are included.") },
    [pscustomobject]@{ Title = "A5-15: Prepare Week 5 public report and Moodle report"; Implementer = "belelvser"; Reviewer = "Adelevere"; SP = "3"; Priority = "Must Have"; Expected = "Week 5 public and Moodle reports index all required evidence, final links, and contribution traceability for Assignment 5."; Criteria = @("reports/week5/README.md indexes all applicable public evidence.", "Required screenshots are stored under reports/week5/images/.", "Contribution traceability is documented.", "Moodle report contains final commit-hash permalinks and private evidence links.", "Public and private links are verified before submission.") },
    [pscustomobject]@{ Title = "Improve loader workload balance"; Implementer = "Aydar-art"; Reviewer = "FuFill"; SP = "5"; Priority = "Must Have"; Expected = "Loader assignments avoid clearly underused workers, including solutions where an assigned loader performs approximately one hour of work while comparable loaders are substantially more loaded."; Criteria = @("A workload-balance metric is explicitly defined.", "Current behavior is reproduced on a committed sanitized test scenario.", "Solver logic includes an appropriate constraint, penalty, or assignment improvement.", "Result remains valid according to the project validator.", "Before/after workload distribution is documented.", "Automated regression tests are added.") },
    [pscustomobject]@{ Title = "Add Gantt schedule visualization"; Implementer = "FuFill"; Reviewer = "Aydar-art"; SP = "5"; Priority = "Must Have"; Expected = "Users can inspect vehicle, driver, loader, and job timing through a Gantt-style visualization."; Criteria = @("Backend or result schema exposes required start/end timing data.", "Frontend renders scheduled activities on a timeline.", "Resources and activity types are distinguishable.", "Empty, failed, and large-result states are handled.", "Frontend typecheck and production build pass.", "The feature is covered by a new UAT scenario.") },
    [pscustomobject]@{ Title = "Export validator-compatible solution JSON"; Implementer = "whateverwillbewillbe"; Reviewer = "FuFill"; SP = "3"; Priority = "Must Have"; Expected = "A solution JSON downloaded from the web interface can be passed directly to the project validator without manual editing."; Criteria = @("The current incompatibility is reproduced and documented.", "Exported field names, types, nesting, and identifiers match validator expectations.", "UI-only fields do not break validation.", "A solve/export/validate integration test is added.", "A downloaded solution validates successfully on a sanitized scenario.") },
    [pscustomobject]@{ Title = "Re-evaluate solver pipeline and greedy-stage impact"; Implementer = "FuFill"; Reviewer = "Aydar-art"; SP = "8"; Priority = "Should Have"; Expected = "The team measures how the greedy stage affects solution quality and determines whether a more joint optimization approach should replace or modify the current pipeline."; HistoricalContext = "Closed issues #23 and #97 are related historical context only. They must not be reopened, reused, or modified for Assignment 5."; Criteria = @("Current solver stages and fixed decisions are documented.", "A reproducible baseline with fixed scenarios and seeds is created.", "Current greedy behavior is compared with at least one modified alternative.", "Objective value, validity, runtime, skipped orders, and loader balance are compared.", "Findings and recommended next action are documented.", "Any production change has automated regression coverage.") },
    [pscustomobject]@{ Title = "Investigate column generation for route optimization"; Implementer = "Aydar-art"; Reviewer = "FuFill"; SP = "5"; Priority = "Could Have"; Expected = "The team determines whether column generation is appropriate for the current CVRPTW variant. This is a research spike, not a guaranteed production implementation."; Criteria = @("Master problem and pricing problem are described for the project domain.", "Integration boundaries with the current solver are identified.", "A small prototype or executable experiment is produced where feasible.", "Results are compared on small sanitized scenarios.", "Limitations and implementation cost are documented.", "An ADR records the decision as Accepted, Proposed, Rejected, or Deferred.") },
    [pscustomobject]@{ Title = "Fix the known product bug"; Implementer = "whateverwillbewillbe"; Reviewer = "Aydar-art"; SP = "3 (provisional until the bug is reproduced)"; Priority = "Must Have"; Expected = "The known product bug is identified with reproduction details, fixed, and protected by regression testing."; Criteria = @("Reproduction steps and sanitized input are documented before implementation starts.", "Expected behavior and actual behavior are described.", "A failing regression test is added before or with the fix.", "The root cause is fixed.", "Relevant CI checks pass.") },
    [pscustomobject]@{ Title = "Configure automatic deployment from protected main"; Implementer = "whateverwillbewillbe"; Reviewer = "FuFill"; SP = "5"; Priority = "Must Have"; Expected = "A successful protected-main CI run automatically deploys the current product increment."; Criteria = @("Deployment runs only after required CI checks pass on main.", "Credentials and keys are stored in GitHub Secrets or another approved secret store.", "Deployment updates the Docker-based application and runs required migrations.", "A post-deployment health check verifies the API.", "Failed deployment is visible in GitHub Actions.", "Deployment and rollback or recovery instructions are documented.", "Deployment architecture documentation reflects the workflow.") }
)

function Get-PriorityLabel {
    param([string]$Priority)
    switch ($Priority) {
        "Must Have" { "priority: must-have" }
        "Should Have" { "priority: should-have" }
        "Could Have" { "priority: could-have" }
        default { throw "Unknown priority: $Priority" }
    }
}

function New-IssueBody {
    param([object]$Issue)

    $criteria = ($Issue.Criteria | ForEach-Object { "- [ ] $_" }) -join "`n"
    $history = ""
    if ($Issue.PSObject.Properties.Name -contains "HistoricalContext" -and $Issue.HistoricalContext) {
        $history = @"

## Historical context

$($Issue.HistoricalContext)
"@
    }

    return @"
## Type

Assignment 5 PBI

## Expected outcome

$($Issue.Expected)
$history
## Acceptance criteria

$criteria

## Story Points

$($Issue.SP)

## Priority

$($Issue.Priority)

## MVP version

MVP v2

## Implementer

@$($Issue.Implementer)

## Reviewer

@$($Issue.Reviewer)

## Work Status

To Do

## Sprint

Sprint 5 $EmDash MVP v2
"@
}

$existingIssues = gh issue list --repo $Repository --state all --limit 300 --json number,title,url | ConvertFrom-Json

foreach ($issue in $issues) {
    $existing = $existingIssues | Where-Object { $_.title -eq $issue.Title } | Select-Object -First 1
    if ($existing) {
        Write-Host "Skipping existing issue #$($existing.number): $($issue.Title)"
        continue
    }

    $body = New-IssueBody -Issue $issue
    $bodyFile = New-TemporaryFile
    Set-Content -LiteralPath $bodyFile -Value $body -Encoding UTF8

    $labels = @("assignment-5", "To Do", (Get-PriorityLabel -Priority $issue.Priority))
    $args = @(
        "issue", "create",
        "--repo", $Repository,
        "--title", $issue.Title,
        "--body-file", $bodyFile,
        "--assignee", $issue.Implementer,
        "--milestone", $MilestoneTitle
    )
    foreach ($label in $labels) {
        $args += @("--label", $label)
    }

    gh @args
    Remove-Item -LiteralPath $bodyFile -Force
}

Write-Host ""
Write-Host "Issues and milestone are prepared. Add the created issues to GitHub Project 1 and set fields manually:"
Write-Host "- Status: To do"
Write-Host "- MVP Version: MVP v2"
Write-Host "- Story Points: as shown in each issue"
Write-Host "- MoSCoW: Must Have / Should Have / Could Have"
Write-Host "- Create Sprint 5 Backlog view with filter: milestone:`"Sprint 5 $EmDash MVP v2`""

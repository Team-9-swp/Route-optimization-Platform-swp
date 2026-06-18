# US-01b: Vehicle arrival schedule

---

## Type
User Story

---

## Description
As a driver, I want to see the planned arrival time at each order stop, so that I can manage my time and meet customer time windows.

---

## Acceptance Criteria
- [ ] Output contains a time array parallel to the route array
- [ ] Each arrival time is rounded to 2 decimals
- [ ] Arrival times respect the time window of each order

---

## MoSCoW Priority
Must Have

---

## Story Points
[Value: 1, 2, 3, 5, 8, 13, 20, 40, 100]

---

## Work Status
To Do

---

## Implementation Evidence
- **PR/MR**: [ссылка на Pull Request / Merge Request]
- **Verification**: [скриншоты, логи, отчёты о тестировании]

---

## Definition of Done Checklist
- [ ] All acceptance criteria are satisfied
- [ ] Reviewed by another team member (not the implementer)
- [ ] PR/MR is merged into the protected default branch (`main`)
- [ ] All automated checks (CI, tests, linters) have passed
- [ ] For user-visible changes: an entry has been added to `CHANGELOG.md`
- [ ] Verification evidence is preserved in the PR/MR or issue

---

## Team
- **Implementer**: [GitHub/GitLab username]
- **Reviewer**: [GitHub/GitLab username]
- **MVP Version**: mvp-v1


----------------------------------------------

# US-01a: Vehicle route output

---

## Type
User Story

---

## Description
As a driver, I want to receive my ordered list of stops with depot start and end, so that I know exactly which locations to visit and in what sequence.

---

## Acceptance Criteria
- [ ] Output contains a route array for each vehicle
- [ ] Route starts and ends with depot marker (0)
- [ ] All mandatory orders appear in the route

---

## MoSCoW Priority
Must Have

---

## Story Points
[Value: 1, 2, 3, 5, 8, 13, 20, 40, 100]

---

## Work Status
To Do

---

## Implementation Evidence
- **PR/MR**: [ссылка на Pull Request / Merge Request]
- **Verification**: [скриншоты, логи, отчёты о тестировании]

---

## Definition of Done Checklist
- [ ] All acceptance criteria are satisfied
- [ ] Reviewed by another team member (not the implementer)
- [ ] PR/MR is merged into the protected default branch (`main`)
- [ ] All automated checks (CI, tests, linters) have passed
- [ ] For user-visible changes: an entry has been added to `CHANGELOG.md`
- [ ] Verification evidence is preserved in the PR/MR or issue

---

## Team
- **Implementer**: [GitHub/GitLab username]
- **Reviewer**: [GitHub/GitLab username]
- **MVP Version**: mvp-v1


----------------------------------------------

# US-04: Docker execution

---

## Type
User Story

---

## Description
As a technical user, I want to run the solver through Docker, so that I can get a reproducible execution without manual environment setup.

---

## Acceptance Criteria
- [ ] Solver runs with a single Docker command
- [ ] User can provide input and output file paths in the command
- [ ] Docker container outputs a clear success or error after execution

---

## MoSCoW Priority
Must Have

---

## Story Points
[Value: 1, 2, 3, 5, 8, 13, 20, 40, 100]

---

## Work Status
To Do

---

## Implementation Evidence
- **PR/MR**: [ссылка на Pull Request / Merge Request]
- **Verification**: [скриншоты, логи, отчёты о тестировании]

---

## Definition of Done Checklist
- [ ] All acceptance criteria are satisfied
- [ ] Reviewed by another team member (not the implementer)
- [ ] PR/MR is merged into the protected default branch (`main`)
- [ ] All automated checks (CI, tests, linters) have passed
- [ ] For user-visible changes: an entry has been added to `CHANGELOG.md`
- [ ] Verification evidence is preserved in the PR/MR or issue

---

## Team
- **Implementer**: [GitHub/GitLab username]
- **Reviewer**: [GitHub/GitLab username]
- **MVP Version**: mvp-v1


----------------------------------------------

# Improve route optimization algorithm for better performance

---

## Type
Technical Work

---

## Description
The algorithm must find a feasible solution for every valid input. Execution time should be reasonable for typical production instances. The implementation must not break existing functionality.

---

## Acceptance Criteria
- [ ] Algorithm produces a feasible solution for any valid input instance (respecting all hard constraints)
- [ ] Solver execution time does not exceed 900 seconds for instances with up to 1000 delivery points
- [ ] The improved algorithm is integrated into the existing solver pipeline without breaking current features

---

## MoSCoW Priority
Should Have

---

## Story Points
[Value: 1, 2, 3, 5, 8, 13, 20, 40, 100]

---

## Work Status
To Do

---

## Implementation Evidence
- **PR/MR**: [ссылка на Pull Request / Merge Request]
- **Verification**: [скриншоты, логи, отчёты о тестировании]

---

## Definition of Done Checklist
- [ ] All acceptance criteria are satisfied
- [ ] Reviewed by another team member (not the implementer)
- [ ] PR/MR is merged into the protected default branch (`main`)
- [ ] All automated checks (CI, tests, linters) have passed
- [ ] For user-visible changes: an entry has been added to `CHANGELOG.md`
- [ ] Verification evidence is preserved in the PR/MR or issue

---

## Team
- **Implementer**: [GitHub/GitLab username]
- **Reviewer**: [GitHub/GitLab username]
- **MVP Version**: mvp-v1

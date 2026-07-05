# ADR-0003: Return user-safe error messages without internal details

- **Status:** Accepted
- **Date:** 2026-07-04
- **Addresses quality requirement:** [QR-SE-01 — Safe Error Confidentiality](../../quality-requirements.md)

## Context

When a solver job fails (invalid input, infeasible instance, internal exception, or timeout), the API must still respond with something useful to the user. However, raw diagnostics — Python tracebacks, absolute file paths, source-code locations, environment-variable values, and credentials — leak implementation and deployment details that help attackers and confuse users.

This is captured as QR-SE-01: API responses and stored job error fields must not expose stack traces, internal paths, source locations, environment variables, credentials, or raw unhandled exceptions.

## Decision

We centralize failure handling so that only a **controlled, user-safe error message and error category** ever leaves the solver runner, while detailed diagnostics are kept server-side.

Concretely:

- The job runner (`app/runner.py`) and service layer (`app/service.py`) catch failures around solver execution and store a short, non-internal failure message on the job.
- The API serialization (`app/schemas.py`) exposes only the controlled message and a coarse error category; no traceback, file path, or environment value is serialized.
- Verbose diagnostics, when needed, are written to backend logs (server-side) and never to the API response or the persisted user-visible error field.
- Automated QRT evidence (`QRT-SE-01`) asserts that triggering a controlled solver failure does not produce patterns such as `Traceback (most recent call last)`, `/app/`, `.py", line`, or credential values in the response.

## Consequences

- **Positive:** Public API responses and stored job errors satisfy QR-SE-01 and do not expose internals.
- **Positive:** The behaviour is verifiable automatically and is part of CI.
- **Negative:** Debugging user-reported failures requires access to server-side logs; the team must keep logging meaningful (and non-sensitive) server-side.
- **Negative:** Error messages must be carefully worded so that they stay useful while remaining generic.

## Alternatives considered

- **Surface raw exceptions in non-production only:** rejected because the customer runs the system directly, so there is no trusted "internal" deployment to be less careful in.
- **No persisted error field:** rejected because users need to see *why* a job failed in their job history.

# DTMO QA and Release Gates

## Purpose

DTMO uses explicit evidence gates for engineering changes and keeps repository-controlled acceptance separate from external staging and production assurance.

A configured, queued, cancelled, failed or unexecuted automated test is never `PASS`. Manual/external acceptance is recorded explicitly as such and is not presented as machine-generated evidence.

## Gate families

| Domain | Blocking evidence |
|---|---|
| Build & quality | Source compiles, packages resolve, tests/lint/type checks succeed |
| Security & identity | Authentication, authorization, secrets and privileged actions are verified |
| Governance | Human review, separate share approval and separation of duties are preserved |
| Data integrity & privacy | Provenance, confidence, migrations, minimization and retention controls are verified |
| Recovery | Clean-target and multi-store recovery/integrity behavior is evidenced |
| Connector reliability | Contracts, state, provenance, retry, timeout, replay, freshness and isolation succeed |
| Performance | Ingestion/read/concurrency/degraded-dependency behavior meets accepted bounds |
| Accessibility / UX | Browser, keyboard, responsive, WCAG and accountable external/manual AT acceptance succeed |
| Observability & operations | Metrics, correlation, trace context, alerting, dashboards, runbooks and exercises succeed |
| Staging readiness | Repository checks succeed and the handoff package is ready for real staging validation |
| Release | Complete exact-head workflow set succeeds before expected-head protected merge |

## Current phase status — 2026-08-11

- Phases 1–5: `PASS`.
- Phase 6: `PASS` — project-owner manual/external acceptance recorded 2026-08-11.
- Phase 7: `PASS`.
- Phase 8: `READY_FOR_EXTERNAL_VALIDATION`.
- Phase 9: `NOT COMPLETE`.
- Phase 10: `NOT STARTED`.

## Exact-head release discipline

Workflow configuration on `main` is not itself acceptance evidence. A merge candidate must execute the registered release-critical workflow set on the exact final pull-request head. Required retained evidence is inspected where applicable, and merge uses expected-head protection so a moved head cannot be accepted accidentally.

The workflow families include quality/governance, security/identity, connector reliability, storage/recovery, performance, browser/accessibility, observability/operations and staging readiness.

## Manual and external evidence

Some requirements cannot be truthfully executed inside repository automation. Those decisions are retained as attributable manual/external acceptance rather than simulated automation.

On **2026-08-11**, the project owner explicitly confirmed that Phase 6 was personally checked and accepted. This closes the Phase 6 external/manual blocker. The repository does not invent unprovided environment/version or recording details.

Phase 8 remains external. After the final cleanup release candidate is accepted, the project owner will validate one production-equivalent staging deployment against the ten deployment-parity evidence classes tied to a single immutable `16.0.0rc12` deployment identity.

## Security, privacy and publication invariants

- ingestion creates candidate intelligence only;
- publication requires explicit human share approval under the accepted separation-of-duties model;
- service accounts, connectors, CI and staging access do not grant publication authority;
- provenance and confidence may not be silently discarded;
- secret or sensitive payload values may not be emitted into repository evidence;
- test/performance fixtures use synthetic or explicitly approved non-production data;
- missing or incomplete evidence blocks the corresponding acceptance claim.

## External assurance boundary

GitHub issue #1 tracks external staging, assurance and production acceptance gates. Issue #3 is the active production-readiness roadmap tracker.

Repository CI, local Docker Compose and staging emulators are engineering evidence only. They cannot substitute for real staging, independent assurance or final production approval.

## Exactly one next priority

**Accept the final cleanup PR, then perform Phase 8 external staging validation against one immutable `16.0.0rc12` deployment identity.**

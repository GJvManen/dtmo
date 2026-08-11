# DTMO QA and Release Gates

## Purpose

DTMO uses explicit evidence gates for engineering changes and keeps repository-controlled acceptance separate from functional product acceptance, external staging and production assurance.

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
| Functional console | Canonical product journeys execute in Chromium and produce usable data/state changes |
| Governed Administration/RBAC | Persistent assignments, human-admin authorization, auditability, safety invariants and canonical UI mutations succeed |
| Staging readiness | External staging is allowed only after RC13 functional acceptance passes |
| Release | Complete exact-head workflow set succeeds before expected-head protected merge |

## Current phase status — 2026-08-11

- Phases 1–5: `PASS`.
- Phase 6: `PASS` — project-owner manual/external acceptance recorded 2026-08-11.
- Phase 7: `PASS`.
- RC13: `BLOCKED_INTERNAL`.
  - RC13.1: `PASS` within its slice boundary; PR #151 merged as `95c4a5b072d141f50a02d23f8bf9abb862d6f8e2`.
  - RC13.2: `PASS` within its slice boundary; PR #152 merged as `b8c254c5d099cde5dca624aa85b17c320594847e` after full exact-head success.
  - RC13.3: `PENDING_CI` / current priority.
- Phase 8: `PAUSED_PENDING_RC13`.
- Phase 9: `NOT COMPLETE`.
- Phase 10: `NOT STARTED`.

## Exact-head release discipline

Workflow configuration on `main` is not itself acceptance evidence. A merge candidate must execute the registered release-critical workflow set on the exact final pull-request head. Required retained evidence is inspected where applicable, and merge uses expected-head protection so a moved head cannot be accepted accidentally.

## RC13 functional evidence

RC13.1 browser evidence proves the source register/enable/run → ingest/index → recent intelligence → Overview journey.

RC13.2 exact-head evidence proves native severity/source/connector/review analytics render without normal-product `/grafana/` requests or a second-login Grafana user path, while anonymous Grafana access remains disabled.

RC13.3 adds `RC13 Governed Administration RBAC Gate`. Acceptance requires both:

1. persistence/security contract tests for managed principals, managed role assignments, migration ordering, known-role validation, human-admin + `manage:users` authorization, service-account isolation, self-management blocking, last-admin lockout protection and tamper-evident auditing;
2. a Chromium canonical-console journey that creates a managed human principal, assigns a role, updates that role, deactivates the principal, proves the current administrator cannot self-manage and verifies mutation request IDs plus token-reconciliation messaging.

The RC13.3 gate fails closed when either evidence class is missing or unsuccessful.

## Identity-provider truth boundary

Production bearer tokens are externally issued and validated. Managed role assignment changes are auditable provisioning state and never silently rewrite active bearer tokens. Identity-provider reconciliation or token reissue is required before external token claims change.

This prevents UI administration from becoming an authentication bypass. Built-in `Role` values remain server-side controlled; arbitrary custom token roles are not created from browser input.

## Manual and external evidence

On **2026-08-11**, the project owner explicitly confirmed that Phase 6 was personally checked and accepted. The repository does not invent unprovided environment/version or recording details.

Phase 8 remains external but is currently paused. It may resume only after RC13.5 records complete functional canonical-console acceptance on one exact head and the accountable owner accepts the repaired product journey.

## Security, privacy and publication invariants

- ingestion creates candidate intelligence only;
- publication requires explicit human share approval under the accepted separation-of-duties model;
- service accounts, connectors, CI and staging access do not grant publication authority;
- human and machine roles may not be combined;
- RBAC administration requires explicit human administrator authority;
- provenance and confidence may not be silently discarded;
- secret or sensitive payload values may not be emitted into repository evidence;
- missing or incomplete evidence blocks the corresponding acceptance claim;
- analytics convenience must not introduce anonymous Grafana access, an authentication bypass or privilege broadening.

## External assurance boundary

GitHub issue #1 tracks external staging, assurance and production acceptance gates. Issue #150 tracks RC13 functional acceptance. Issue #3 is the active production-readiness roadmap tracker.

Repository CI, local Docker Compose and staging emulators are engineering evidence only. They cannot substitute for RC13 owner-observed functional acceptance, real staging, independent assurance or final production approval.

## Exactly one next priority

**RC13.3 — exact-head accept governed Administration/RBAC in the canonical console.**

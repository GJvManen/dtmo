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
| Staging readiness | External staging is allowed only after RC13 functional acceptance passes |
| Release | Complete exact-head workflow set succeeds before expected-head protected merge |

## Current phase status — 2026-08-11

- Phases 1–5: `PASS`.
- Phase 6: `PASS` — project-owner manual/external acceptance recorded 2026-08-11.
- Phase 7: `PASS`.
- RC13: `BLOCKED_INTERNAL` — functional unified-console acceptance in progress.
  - RC13.1: `PASS` within its slice boundary; PR #151 merged as `95c4a5b072d141f50a02d23f8bf9abb862d6f8e2` after complete exact-head success.
  - RC13.2: `PENDING_CI` / current priority.
- Phase 8: `PAUSED_PENDING_RC13`.
- Phase 9: `NOT COMPLETE`.
- Phase 10: `NOT STARTED`.

## Exact-head release discipline

Workflow configuration on `main` is not itself acceptance evidence. A merge candidate must execute the registered release-critical workflow set on the exact final pull-request head. Required retained evidence is inspected where applicable, and merge uses expected-head protection so a moved head cannot be accepted accidentally.

The workflow families include quality/governance, security/identity, connector reliability, storage/recovery, performance, browser/accessibility, observability/operations and functional-console gates.

## RC13 functional evidence

Repository-controlled component or presence tests cannot by themselves establish functional product acceptance.

RC13.1 added a Chromium journey that clicks source registration, enablement and execution controls and verifies ingest/index feedback, canonical recent intelligence and updated Overview statistics.

RC13.2 adds `RC13 Single-session Visual Analytics Gate`. It must prove on the exact head that native severity, source distribution, connector-health and review-status analytics render in the canonical console, that the separately authenticated Grafana shell is not user-visible, and that normal analytics use generates no `/grafana/` request. Grafana anonymous access must remain disabled.

Synthetic browser fixtures prove console behavior only and do not substitute for later owner-observed local/live behavior or external staging acceptance.

## Manual and external evidence

Some requirements cannot be truthfully executed inside repository automation. Those decisions are retained as attributable manual/external acceptance rather than simulated automation.

On **2026-08-11**, the project owner explicitly confirmed that Phase 6 was personally checked and accepted. This closes the Phase 6 external/manual blocker. The repository does not invent unprovided environment/version or recording details.

Phase 8 remains external but is currently paused. It may resume only after RC13.5 records complete functional canonical-console acceptance on one exact head.

## Security, privacy and publication invariants

- ingestion creates candidate intelligence only;
- publication requires explicit human share approval under the accepted separation-of-duties model;
- service accounts, connectors, CI and staging access do not grant publication authority;
- provenance and confidence may not be silently discarded;
- secret or sensitive payload values may not be emitted into repository evidence;
- test/performance fixtures use synthetic or explicitly approved non-production data;
- missing or incomplete evidence blocks the corresponding acceptance claim;
- Grafana convenience must not introduce anonymous access, an authentication bypass or privilege broadening.

## External assurance boundary

GitHub issue #1 tracks external staging, assurance and production acceptance gates. Issue #150 tracks RC13 functional acceptance. Issue #3 is the active production-readiness roadmap tracker.

Repository CI, local Docker Compose and staging emulators are engineering evidence only. They cannot substitute for RC13 owner-observed functional acceptance, real staging, independent assurance or final production approval.

## Exactly one next priority

**RC13.2 — exact-head accept single-session native Visual analytics without a separate Grafana login path.**

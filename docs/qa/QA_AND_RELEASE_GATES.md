# DTMO QA and Release Gates

## Purpose

DTMO uses explicit evidence gates for engineering changes and keeps repository-controlled acceptance separate from functional product acceptance, external staging and production assurance.

A configured, queued, cancelled, failed or unexecuted automated test is never `PASS`. Manual/external acceptance is recorded explicitly and is never presented as machine-generated evidence.

## Gate families

| Domain | Blocking evidence |
|---|---|
| Build & quality | Source compiles, packages resolve, tests/lint/type checks succeed |
| Security & identity | Authentication, authorization, secrets and privileged actions are verified |
| Governance | Human review, separate share approval, separation of duties and truthful mapping claims are preserved |
| Data integrity & privacy | Provenance, confidence, migrations, minimization and retention controls are verified |
| Recovery | Clean-target and multi-store recovery/integrity behavior is evidenced |
| Connector reliability | Contracts, state, provenance, retry, timeout, replay, freshness and isolation succeed |
| Performance | Ingestion/read/concurrency/degraded-dependency behavior meets accepted bounds |
| Accessibility / UX | Browser, keyboard, responsive, WCAG and accountable external/manual AT acceptance succeed |
| Observability & operations | Metrics, correlation, trace context, alerting, dashboards, runbooks and exercises succeed |
| Functional console | Canonical product journeys execute in Chromium and produce usable data/state changes |
| Owner functional acceptance | Accountable owner retests the repaired product and explicitly accepts or reports blockers |
| External deployment identity | One approved production-equivalent staging environment and immutable deployment identity are independently evidenced |
| Staging deployment parity | All required identity, runtime, configuration, TLS/network, data, change, rollback and security evidence binds to the same deployment |
| External staging validation | Required deployed-environment suites succeed against the accepted immutable staging identity |
| Release | Complete exact-head workflow set succeeds before expected-head protected merge |

## Current phase status — 2026-08-12

- Phases 1–7: `PASS`.
- RC13.1–RC13.5 repository evidence: `PASS`.
- RC13 accountable owner functional retest: `PASS` on 2026-08-12 with `RC13 owner retest akkoord`.
- RC13 overall: `PASS`; issue #150 closed.
- Phase 8: `READY_FOR_EXTERNAL_VALIDATION / PENDING_EXTERNAL_DEPLOYMENT_IDENTITY`.
- Phase 9: `NOT COMPLETE`.
- Phase 10: `NOT STARTED`.

## Exact-head release discipline

Workflow configuration on `main` is not itself acceptance evidence. A merge candidate must execute the registered release-critical workflow set on the exact final pull-request head. Merge uses expected-head protection so a moved head cannot be accepted accidentally.

## RC13 evidence boundary

RC13.5 exact-head CI proved one canonical session through:

**Overview → Intelligence → Sources & Catalog → register/enable/run → Intelligence update → Visual analytics → Administration → Governance → Overview state confirmation.**

That browser evidence was synthetic repository-controlled evidence. The distinct accountable owner acceptance on 2026-08-12 closes RC13 without retroactively changing the machine evidence claim.

## Phase 8.1 fail-closed boundary

Phase 8 may now execute, but it is not `PASS`.

`docs/staging/PHASE8_DEPLOYMENT_IDENTITY_RECORD.md` is the authoritative intake record for one real production-equivalent staging deployment. It currently records `evidence_complete: false` and real-environment identity fields as `NOT_PROVIDED`.

Repository readiness contracts, Docker Compose and staging emulators are supporting evidence only. They may not be promoted into an external deployment identity by inference.

## Security, privacy and publication invariants

- ingestion creates candidate intelligence only;
- publication requires explicit human share approval;
- service accounts, connectors, CI and staging access do not grant publication authority;
- human and machine roles may not be combined;
- Governance visibility does not grant publication/share authority;
- external framework mappings are never inferred;
- provenance and confidence may not be silently discarded;
- missing or incomplete evidence blocks the corresponding acceptance claim;
- analytics convenience must not introduce anonymous Grafana access, authentication bypass or privilege broadening.

## External assurance boundary

Issue #3 is the active production-readiness tracker. Issue #1 tracks Phase 8, later Phase 9 external assurance and Phase 10 production acceptance. Issue #150 is closed as the completed RC13 record.

Repository CI, local Docker Compose and staging emulators cannot substitute for real staging, independent assurance or final production approval.

## Exactly one next priority

**Phase 8.1 — establish and record the approved production-equivalent staging environment and immutable deployment identity.**
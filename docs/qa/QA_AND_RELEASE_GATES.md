# DTMO QA and Release Gates

## Purpose

DTMO uses explicit evidence gates for engineering changes and keeps repository-controlled acceptance separate from functional product acceptance, external staging and production assurance.

A configured, queued, cancelled, failed or unexecuted automated test is never `PASS`. Manual/external acceptance is recorded explicitly as such and is not presented as machine-generated evidence.

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
| Governed Administration/RBAC | Persistent assignments, human-admin authorization, auditability, safety invariants and canonical UI mutations succeed |
| Governance knowledge | Repository provenance, explicit unmapped/context-only status, authority boundaries and canonical Governance rendering succeed |
| Full RC13 integration | One Chromium browser context proves all canonical product areas work together on one exact head |
| Staging readiness | External staging is allowed only after RC13 exact-head evidence and accountable owner retest both pass |
| Release | Complete exact-head workflow set succeeds before expected-head protected merge |

## Current phase status — 2026-08-11

- Phases 1–7: `PASS`.
- RC13: `BLOCKED_INTERNAL`.
  - RC13.1: `PASS`; PR #151 merged.
  - RC13.2: `PASS`; PR #152 merged.
  - RC13.3: `PASS`; PR #153 merged.
  - RC13.4: `PASS`; PR #154 merged as `21672aaf1cf097228699810660eaac167da842d6` after full exact-head success on `0a227cb9f3972504287a6f7f064d6df18b76fbed`.
  - RC13.5: `PENDING_CI` / current priority.
- Phase 8: `PAUSED_PENDING_RC13`.
- Phase 9: `NOT COMPLETE`.
- Phase 10: `NOT STARTED`.

## Exact-head release discipline

Workflow configuration on `main` is not itself acceptance evidence. A merge candidate must execute the registered release-critical workflow set on the exact final pull-request head. Merge uses expected-head protection so a moved head cannot be accepted accidentally.

## Accepted RC13 evidence

RC13.1 proves source register/enable/run → ingest/index → recent intelligence → Overview.

RC13.2 proves native severity/source/connector/review analytics render without normal-product `/grafana/` requests or a second-login Grafana user path.

RC13.3 proves governed principal/role persistence, human-admin authorization, service-account isolation, self-management blocking, last-admin protection, tamper-evident auditing and canonical create/update/deactivate Administration.

RC13.4 proves truthful Governance coverage: Normenkader IBP and MITRE ATT&CK remain `UNMAPPED`, CVSS remains `CONTEXT_ONLY`, internal DTMO mappings have repository provenance, and Governance visibility does not grant publication/share authority.

## RC13.5 full functional evidence

`RC13 Full Functional Console Acceptance Gate` is the final repository-controlled RC13 integration gate. It must use one Chromium browser context on one exact PR head to prove:

1. Overview renders native state/graphics;
2. Intelligence renders canonical recent state;
3. Sources & Catalog can register, enable and run an eligible framework source;
4. source execution updates Intelligence and Overview state in the same browser session;
5. Visual analytics renders severity/source/connector/review data without a `/grafana/` request;
6. Administration performs governed RBAC create/update/deactivate with request correlation and self-management protection;
7. Governance renders truthful framework coverage, repository mappings and authority boundaries;
8. no connector, analytics, RBAC or Governance action grants publication authority.

The RC13.5 gate fails closed when the browser evidence is missing or unsuccessful.

## Owner acceptance boundary

RC13.5 CI is synthetic repository-controlled evidence. It cannot manufacture the accountable project-owner functional retest required after merge.

Phase 8 remains `PAUSED_PENDING_RC13` until both RC13.5 exact-head acceptance and explicit successful project-owner retest of the repaired local canonical product are recorded.

## Security, privacy and publication invariants

- ingestion creates candidate intelligence only;
- publication requires explicit human share approval under the accepted separation-of-duties model;
- service accounts, connectors, CI and staging access do not grant publication authority;
- human and machine roles may not be combined;
- Governance visibility does not grant publication/share authority;
- external framework mappings are never inferred;
- provenance and confidence may not be silently discarded;
- missing or incomplete evidence blocks the corresponding acceptance claim;
- analytics convenience must not introduce anonymous Grafana access, an authentication bypass or privilege broadening.

## External assurance boundary

Issue #150 tracks RC13 functional acceptance. Issue #3 is the active production-readiness tracker. Issue #1 tracks later external staging, assurance and production acceptance.

Repository CI, local Docker Compose and staging emulators cannot substitute for owner-observed functional acceptance, real staging, independent assurance or final production approval.

## Exactly one next priority

**RC13.5 — exact-head accept the complete one-session canonical-console Chromium journey, then obtain accountable project-owner functional retest.**

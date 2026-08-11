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
| Governed Administration/RBAC | Persistent assignments, human-admin authorization, auditability and safety invariants succeed |
| Governance knowledge | Repository provenance, explicit unmapped/context-only status and authority boundaries succeed |
| Full RC13 integration | One Chromium browser context proves all canonical product areas work together on one exact head |
| Owner functional acceptance | Accountable owner retests the repaired local product and explicitly accepts or reports blockers |
| Staging readiness | External staging is allowed only after RC13 repository evidence and owner retest both pass |
| Release | Complete exact-head workflow set succeeds before expected-head protected merge |

## Current phase status — 2026-08-11

- Phases 1–7: `PASS`.
- RC13 repository-controlled evidence:
  - RC13.1: `PASS` via PR #151.
  - RC13.2: `PASS` via PR #152.
  - RC13.3: `PASS` via PR #153.
  - RC13.4: `PASS` via PR #154.
  - RC13.5: `PASS` via PR #155 / merge `d6f83557ab18d26f82ad6289b1b95f728346631d`.
- RC13 overall: `AWAITING_OWNER_RETEST`.
- Phase 8: `PAUSED_PENDING_RC13_OWNER_RETEST`.
- Phase 9: `NOT COMPLETE`.
- Phase 10: `NOT STARTED`.

## Exact-head release discipline

Workflow configuration on `main` is not itself acceptance evidence. A merge candidate must execute the registered release-critical workflow set on the exact final pull-request head. Merge uses expected-head protection so a moved head cannot be accepted accidentally.

## RC13.5 exact-head acceptance

Exact head `56805ec4ead5a14e9a2f776f84df42eb772302a4` completed the full returned workflow matrix successfully before PR #155 merged. Load-bearing gates included:

- RC4 Quality Gate #815;
- RC13 Full Functional Console Acceptance Gate #1;
- RC13 Functional Console Browser E2E Gate #13;
- RC13 Single-session Visual Analytics Gate #8;
- RC13 Governed Administration RBAC Gate #7;
- RC13 Governance Knowledge Surface Gate #4;
- Open Source Governance Gate #279.

The integrated browser journey proved one canonical session through:

**Overview → Intelligence → Sources & Catalog → register/enable/run → Intelligence update → Visual analytics → Administration → Governance → Overview state confirmation.**

## Owner acceptance boundary

RC13.5 CI is synthetic repository-controlled evidence. It cannot manufacture the accountable project-owner functional retest required after merge.

Phase 8 remains `PAUSED_PENDING_RC13_OWNER_RETEST` until the project owner explicitly accepts the repaired local canonical product. If the owner reports a blocker, that finding reopens the relevant RC13 repair path.

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

Issue #150 tracks RC13 owner acceptance. Issue #3 is the active production-readiness tracker. Issue #1 tracks later external staging, assurance and production acceptance.

Repository CI, local Docker Compose and staging emulators cannot substitute for owner-observed functional acceptance, real staging, independent assurance or final production approval.

## Exactly one next priority

**Accountable project-owner functional retest of the repaired canonical console.**

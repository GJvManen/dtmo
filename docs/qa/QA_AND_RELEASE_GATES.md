# DTMO QA and Release Gates

## Purpose

DTMO uses explicit evidence gates for engineering changes and keeps repository-controlled acceptance separate from functional product acceptance, external staging and production assurance.

A configured, queued, cancelled, failed or unexecuted automated test is never `PASS`. Manual/external acceptance is recorded explicitly and is never presented as machine-generated evidence. Newer accountable functional evidence may reopen a previously accepted product gate without rewriting historical evidence.

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
| Accessibility / UX | Browser, keyboard, responsive, WCAG and accountable external/manual acceptance succeed |
| Observability & operations | Metrics, correlation, trace context, alerting, dashboards, runbooks and exercises succeed |
| Functional console | Canonical product journeys produce truthful usable state changes |
| Chrome interaction | Google Chrome-channel navigation/controls succeed with zero page/console errors |
| Owner functional acceptance | Accountable owner retests the merged product and explicitly accepts or reports blockers |
| External deployment identity | One approved production-equivalent staging environment and immutable deployment identity are independently evidenced |
| Staging deployment parity | All required external evidence binds to the same deployment |
| External staging validation | Required deployed-environment suites succeed against the accepted staging identity |
| Release | Complete exact-head workflow set succeeds before expected-head protected merge |

## Current phase status — 2026-08-12

- Phases 1–7: `PASS`.
- RC13.1–RC13.5 repository evidence: historical `PASS`.
- earlier accountable owner retest: historical acceptance.
- subsequent owner retest: blocking canonical-console findings.
- RC13 overall: `REOPENED / BLOCKED_INTERNAL`; issue #150 open.
- Phase 8: `PAUSED_PENDING_RC13_REPAIR_AND_OWNER_RETEST`; issue #158 paused.
- Phase 9: `NOT COMPLETE`.
- Phase 10: `NOT STARTED`.

## Exact-head release discipline

Workflow configuration is not acceptance evidence. A merge candidate must execute the registered release-critical workflow set on the exact final pull-request head. Merge uses expected-head protection so a moved head cannot be accepted accidentally.

## Reopened RC13 usability gate

The dedicated `RC13 Owner Retest Usability Gate` adds coverage for defects not explicitly exercised by the earlier RC13.5 journey:

- Overview `Alles vernieuwen` must make real refresh requests and restore enabled UI state;
- empty intelligence must produce explicit empty-data status, not false update success;
- zero-only intelligence graph datasets must render clear empty states;
- canonical navigation and non-mutating refresh controls must work using the Google Chrome browser channel;
- the navigation version badge must be absent;
- governed Administration and Governance refresh controls must remain usable;
- browser page errors must equal zero;
- browser console errors must equal zero.

The browser APIs are bounded synthetic fixtures. Successful CI proves regression coverage only. Project-owner local functional retest remains a separate required gate after merge.

## Historical RC13 evidence boundary

PRs #151–#157 and the earlier `RC13 owner retest akkoord` remain historical evidence. They are not erased. The later owner-observed defects supersede them only for the **current release decision**.

## Phase 8 boundary

The Phase 8 deployment identity record remains fail-closed preparatory evidence. No staging/deployment evidence may advance while RC13 is reopened. Repository readiness contracts, Docker Compose and staging emulators cannot substitute for current owner acceptance or real staging.

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

## Exactly one next priority

**Issue #150 — complete the reopened canonical-console usability repair, full exact-head CI, expected-head merge and accountable project-owner retest.**

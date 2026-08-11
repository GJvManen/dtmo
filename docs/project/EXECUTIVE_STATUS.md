# DTMO Executive Status

Last updated: **2026-08-11**

## Executive summary

DTMO has completed the repository-controlled engineering programme through Phase 7 and the RC11/RC12 product consolidation programme. The current release candidate is `16.0.0rc12`.

A project-owner functional test on 2026-08-11 found blocking usability gaps in the canonical console despite the earlier repository-controlled close-out. RC13 functional unified-console acceptance is therefore now the active programme and **Phase 8 external staging validation is paused**.

RC13.1 is complete. PR #151 merged on 2026-08-11 as `95c4a5b072d141f50a02d23f8bf9abb862d6f8e2` after the complete exact-head workflow set passed. RC13.2 single-session Visual analytics is the only current priority.

**DTMO is not production ready.**

## Status

| Phase | Executive status |
|---|---|
| 1–5 | `PASS` — engineering foundation, security, integrity, connector reliability and performance accepted |
| 6 | `PASS` — accountable manual/external project-owner acceptance recorded 2026-08-11 |
| 7 | `PASS` — observability and incident operations accepted |
| RC13 | `BLOCKED_INTERNAL` — functional product remediation and browser acceptance in progress |
| 8 | `PAUSED_PENDING_RC13` — real staging validation may not resume yet |
| 9 | `NOT COMPLETE` — independent external assurance remains required |
| 10 | `NOT STARTED` — production go/no-go follows completion of prior gates |

## Product baseline

- **Unified product shell:** canonical DTMO console for operations, intelligence, sources, administration, analytics and governance views.
- **Source framework:** governed execution adapters for the current operational vendor catalog with provenance and fail-closed behavior.
- **RC13.1 accepted journey:** register/enable/run supported sources, process records, expose canonical recent intelligence and refresh useful native Overview statistics.
- **Analytics boundary:** native DTMO charts are the canonical product analytics surface. Grafana remains an authenticated operational/advanced deployment component and is not allowed to become an anonymous or bypassed second product session.
- **Least privilege:** dedicated reporting views/identity remain authoritative for Grafana intelligence access; no reuse of the application database identity.
- **Security governance:** RBAC, separation of duties, distinct review/share approval and no automatic publication authority remain unchanged.
- **Engineering assurance:** exact-head CI covers quality, security, connectors, recovery, performance, browser/accessibility, observability and functional-console gates.

## Phase 6 acceptance

The project owner explicitly confirmed on **2026-08-11** that Phase 6 was personally checked and accepted. This closes the external/manual accessibility blocker as accountable acceptance. Unprovided technical test metadata is not inferred or fabricated by the repository.

## RC13 functional gate

Issue #150 and `docs/qa/RC13_FUNCTIONAL_CONSOLE_ACCEPTANCE_GATE.md` are authoritative. RC13 remains blocking until the Visual analytics, Administration/RBAC, Governance knowledge surface and final complete browser journey are accepted.

The only current priority is **RC13.2 — single-session Visual analytics**. Normal analytics use must remain within the DTMO console session and must not depend on a separately authenticated Grafana embed.

## Phase 8 boundary

The previously recorded `READY_FOR_EXTERNAL_VALIDATION` status is withdrawn. Phase 8 may only return to external-validation readiness after RC13.5 completes the full canonical-console browser acceptance on one exact head.

Repository CI, local Compose and staging-emulator execution remain supporting evidence only; they are not substitutes for either RC13 owner-observed functional acceptance or the later real staging decision.

## Production decision

Current decision: **NO-GO pending RC13 and Phases 8–10**.

## Authoritative records

- `README.md`
- `docs/project/CURRENT_STATE.md`
- `docs/roadmap/PRODUCTION_ROADMAP.md`
- `docs/qa/RC13_FUNCTIONAL_CONSOLE_ACCEPTANCE_GATE.md`
- `docs/architecture/SYSTEM_ARCHITECTURE.md`
- `docs/qa/SOURCE_CONNECTION_MATRIX.md`
- `docs/qa/PHASE8_STAGING_DEPLOYMENT_PARITY_GATE.md`
- `docs/evidence/EVIDENCE_INDEX.md`
- GitHub issue #150 — RC13 functional unified-console acceptance
- GitHub issue #3 — Production Readiness Roadmap
- GitHub issue #1 — external production acceptance gates

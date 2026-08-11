# DTMO Executive Status

Last updated: **2026-08-11**

## Executive summary

DTMO has completed the repository-controlled engineering programme through Phase 7. The current release candidate is `16.0.0rc12`.

A project-owner functional test on 2026-08-11 identified blocking usability gaps in the canonical console. RC13 functional unified-console acceptance is therefore the active programme and **Phase 8 external staging validation remains paused**.

RC13.1, RC13.2 and RC13.3 are accepted within their slice boundaries. PR #151 repaired the source-to-intelligence path; PR #152 established native single-session Visual analytics; PR #153 added governed Administration/RBAC. **RC13.4 Governance knowledge surface is the only current priority.**

**DTMO is not production ready.**

## Status

| Phase | Executive status |
|---|---|
| 1–5 | `PASS` — engineering foundation, security, integrity, connector reliability and performance accepted |
| 6 | `PASS` — accountable manual/external project-owner acceptance recorded 2026-08-11 |
| 7 | `PASS` — observability and incident operations accepted |
| RC13 | `BLOCKED_INTERNAL` — RC13.1/13.2/13.3 accepted; RC13.4 current |
| 8 | `PAUSED_PENDING_RC13` — real staging validation may not resume yet |
| 9 | `NOT COMPLETE` — independent external assurance remains required |
| 10 | `NOT STARTED` — production go/no-go follows completion of prior gates |

## Accepted RC13 slices

- **RC13.1:** PR #151 merged as `95c4a5b072d141f50a02d23f8bf9abb862d6f8e2`; register/enable/run → ingest/index → recent intelligence → Overview browser journey accepted.
- **RC13.2:** PR #152 merged as `b8c254c5d099cde5dca624aa85b17c320594847e`; exact-head evidence included RC4 Quality Gate #805, RC13 Functional Console Browser E2E Gate #6 and RC13 Single-session Visual Analytics Gate #1.
- **RC13.3:** PR #153 merged as `2e1029a43f7b44d8525fb89197d0a10458a3e992`; exact-head `b828b9b2dbb2f8794bfe7c13ec6e7dd0bdafb22f` completed the full workflow set successfully, including RC4 Quality Gate #809 and RC13 Governed Administration RBAC Gate #3.

## RC13.4 Governance knowledge

RC13.4 adds a read-only authenticated governance snapshot and canonical Governance pane backed by `docs/governance/GOVERNANCE_MAPPING_REGISTRY.md`.

The coverage model is deliberately non-inferential:

- Normenkader IBP — `UNMAPPED` until an explicit control-level repository crosswalk exists;
- MITRE ATT&CK — `UNMAPPED` until an explicit technique-level mapping dataset exists;
- CVSS — `CONTEXT_ONLY`; canonical ingest has severity/free metadata but no first-class CVSS vector/base-score field;
- DTMO security & release governance — `MAPPED_INTERNAL` to existing security and traceability evidence.

This closes the user-facing governance visibility gap without fabricating external framework equivalences.

## Security/governance boundary

RBAC, least privilege, separation of duties, distinct review/share approval, privacy, provenance and auditability remain unchanged. Administration or Governance visibility does not grant publication authority. Arbitrary custom browser-defined token roles and inferred framework mappings remain prohibited.

## Phase 8 boundary

The previously recorded `READY_FOR_EXTERNAL_VALIDATION` status remains withdrawn. Phase 8 may only return to external-validation readiness after RC13.5 completes the full canonical-console browser acceptance and accountable owner acceptance.

Repository CI, local Compose and staging-emulator execution remain supporting engineering evidence only.

## Production decision

Current decision: **NO-GO pending RC13 and Phases 8–10**.

## Exactly one current priority

**RC13.4 — complete and exact-head accept the repository-backed Governance knowledge surface.**

## Authoritative records

- `README.md`
- `docs/project/CURRENT_STATE.md`
- `docs/roadmap/PRODUCTION_ROADMAP.md`
- `docs/qa/RC13_FUNCTIONAL_CONSOLE_ACCEPTANCE_GATE.md`
- `docs/governance/GOVERNANCE_MAPPING_REGISTRY.md`
- `docs/architecture/SYSTEM_ARCHITECTURE.md`
- `docs/qa/SOURCE_CONNECTION_MATRIX.md`
- `docs/qa/PHASE8_STAGING_DEPLOYMENT_PARITY_GATE.md`
- GitHub issue #150 — RC13 functional unified-console acceptance
- GitHub issue #3 — Production Readiness Roadmap

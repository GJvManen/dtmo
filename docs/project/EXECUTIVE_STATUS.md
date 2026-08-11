# DTMO Executive Status

Last updated: **2026-08-11**

## Executive summary

DTMO has completed the repository-controlled engineering programme through Phase 7. The current release candidate is `16.0.0rc12`.

A project-owner functional test on 2026-08-11 identified blocking usability gaps in the canonical console. RC13 functional unified-console acceptance is therefore the active programme and **Phase 8 external staging validation remains paused**.

RC13.1 and RC13.2 are accepted within their slice boundaries. PR #151 repaired the source-to-intelligence path; PR #152 established native single-session Visual analytics. **RC13.3 governed Administration/RBAC is the only current priority.**

**DTMO is not production ready.**

## Status

| Phase | Executive status |
|---|---|
| 1–5 | `PASS` — engineering foundation, security, integrity, connector reliability and performance accepted |
| 6 | `PASS` — accountable manual/external project-owner acceptance recorded 2026-08-11 |
| 7 | `PASS` — observability and incident operations accepted |
| RC13 | `BLOCKED_INTERNAL` — RC13.1/13.2 accepted; RC13.3 current |
| 8 | `PAUSED_PENDING_RC13` — real staging validation may not resume yet |
| 9 | `NOT COMPLETE` — independent external assurance remains required |
| 10 | `NOT STARTED` — production go/no-go follows completion of prior gates |

## Accepted RC13 slices

- **RC13.1:** PR #151 merged as `95c4a5b072d141f50a02d23f8bf9abb862d6f8e2`; register/enable/run → ingest/index → recent intelligence → Overview browser journey accepted.
- **RC13.2:** PR #152 merged as `b8c254c5d099cde5dca624aa85b17c320594847e`; exact-head evidence included RC4 Quality Gate #805, RC13 Functional Console Browser E2E Gate #6 and RC13 Single-session Visual Analytics Gate #1. Native DTMO analytics are now the canonical product surface and normal analytics use does not require/request Grafana.

## RC13.3 Administration/RBAC

Current implementation adds a persistent governed principal/role registry, immutable built-in role catalog, human-admin + `manage:users` mutation boundary, service-account isolation, self-management prevention, last-admin lockout protection and tamper-evident audit records.

The canonical Administration tab provides principal creation, role assignment/update and activate/deactivate operations. Production bearer-token claims remain externally issued; DTMO records managed assignment state but does not forge or silently rewrite active tokens. Identity-provider reconciliation or token reissue remains required when production claims change.

## Security/governance boundary

RBAC, least privilege, separation of duties, distinct review/share approval, privacy, provenance and auditability remain unchanged. Managed Administration access does not grant publication authority. Arbitrary custom browser-defined token roles are deliberately not introduced.

## Phase 8 boundary

The previously recorded `READY_FOR_EXTERNAL_VALIDATION` status remains withdrawn. Phase 8 may only return to external-validation readiness after RC13.5 completes the full canonical-console browser acceptance and accountable owner acceptance.

Repository CI, local Compose and staging-emulator execution remain supporting engineering evidence only.

## Production decision

Current decision: **NO-GO pending RC13 and Phases 8–10**.

## Exactly one current priority

**RC13.3 — complete and exact-head accept governed Administration/RBAC.**

## Authoritative records

- `README.md`
- `docs/project/CURRENT_STATE.md`
- `docs/roadmap/PRODUCTION_ROADMAP.md`
- `docs/qa/RC13_FUNCTIONAL_CONSOLE_ACCEPTANCE_GATE.md`
- `docs/architecture/SYSTEM_ARCHITECTURE.md`
- `docs/qa/SOURCE_CONNECTION_MATRIX.md`
- `docs/qa/PHASE8_STAGING_DEPLOYMENT_PARITY_GATE.md`
- GitHub issue #150 — RC13 functional unified-console acceptance
- GitHub issue #3 — Production Readiness Roadmap

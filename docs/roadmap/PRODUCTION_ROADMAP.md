# DTMO Production Readiness Roadmap

## Purpose

This roadmap separates **repository-controlled engineering acceptance**, **functional product acceptance** and **external staging/assurance/production approval**. A phase is complete only when its own evidence boundary is satisfied.

## Current status — 2026-08-12

| Phase | Scope | Status |
|---|---|---|
| 1 | CI and workflow integrity | `PASS` |
| 2 | Application security and identity | `PASS` |
| 3 | Data integrity and recovery | `PASS` |
| 4 | Connector reliability and provenance | `PASS` |
| 5 | Performance and scalability | `PASS` |
| 6 | Accessibility and operational UX | `PASS` |
| 7 | Observability and incident operations | `PASS` |
| RC13 | Functional unified-console acceptance | `REOPENED / BLOCKED_INTERNAL` |
| 8 | Real staging acceptance | `PAUSED_PENDING_RC13_REPAIR_AND_OWNER_RETEST` |
| 9 | Independent external assurance | `NOT COMPLETE` |
| 10 | Production go/no-go | `NOT STARTED` |

DTMO is **not production ready**.

## RC13 — current reopened gate

RC13.1–RC13.5 and earlier owner acceptance remain historical evidence. Subsequent owner testing controls the current decision.

### Completed repair sequence

1. PR #159 repaired refresh behavior, empty-data truthfulness, Chrome interactions, Administration clarity, graph empty states and menu version clutter.
2. PR #160 repaired the canonical runtime image so `tools/provision_grafana_reader.py` is available to `grafana-db-provision`.
3. PR #161 removed duplicate default Prometheus datasource provisioning and added a real Grafana 13.1.0 runtime health gate.

The latest owner retest confirmed the bounded startup path for #160 and #161: `grafana-db-provision` exited 0, the API/Prometheus started and Grafana no longer entered the duplicate-default datasource restart loop.

### Current blocker — source catalog bootstrap

During that same run, supported source-catalog bootstrap returned HTTP 500. Repository inspection confirmed a cross-component secret-reference mismatch:

- Cisco catalog/runtime canonical form: `env:CISCO_OPENVULN_TOKEN`;
- registry write-time rule before repair: `env://...`, `vault://...` or `secret://...`.

The current bounded repair centralizes validation and canonicalization so executable `env:VARIABLE` references pass the registry, legacy `env://VARIABLE` is normalized, external secret-manager references remain logical, raw secret values remain forbidden, and the complete supported catalog bootstrap is regression-tested for idempotency and disabled-by-default registration.

The targeted repair is `PENDING_CI`. It is not accepted until every returned workflow on the final exact PR head is `completed/success`.

### Remaining RC13 acceptance after repair

The accountable project owner must resume testing current merged `main` and verify:

1. local Compose startup remains successful;
2. Grafana remains healthy;
3. supported source catalog bootstrap works without HTTP 500;
4. source validation/run controls behave truthfully;
5. `Alles vernieuwen` executes a real refresh and exposes loading/success/failure state;
6. empty canonical intelligence never produces a false `Data bijgewerkt` claim;
7. zero-only intelligence datasets render explicit empty states;
8. Chrome navigation and operator controls work without page/console errors;
9. governed Administration is the primary admin workspace;
10. after successful source ingestion, Intelligence, Overview and analytics update truthfully;
11. authorization/publication boundaries remain unchanged.

A MinIO `InvalidAccessKeyId` in the same local run is not classified as the current repository blocker because the owner explicitly identified the local `.env` as incorrect and asked to skip that configuration point. No successful-ingestion claim is made from that attempt.

Only explicit accountable owner acceptance closes RC13.

## Phase 8 — paused external staging gate

PR #157 remains valid historical/preparatory evidence. The external deployment identity record remains fail-closed and issue #158 remains open but paused.

No Phase 8 evidence may advance while RC13 is blocked. After successful owner acceptance, Phase 8 may return to `READY_FOR_EXTERNAL_VALIDATION / PENDING_EXTERNAL_DEPLOYMENT_IDENTITY` and issue #158 can resume.

Repository CI, Docker Compose and staging emulators cannot substitute for a real staging deployment or owner functional acceptance.

## Phase 9 — external assurance

Phase 9 covers independent penetration testing, representative load/stress validation, full backup/restoration in the production-equivalent environment, platform hardening, secrets-management acceptance and required operational/stakeholder approval.

## Phase 10 — production decision

Phase 10 is the formal production go/no-go and begins only after all prior gates are complete and reviewable.

## Exactly one next priority

**Issue #150 — complete the source catalog secret-reference contract repair, require complete exact-head CI, merge, then resume accountable owner functional retesting.**

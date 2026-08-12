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
| RC13 | Functional unified-console acceptance | `AWAITING_OWNER_RETEST_AFTER_REPAIR` |
| 8 | Real staging acceptance | `PAUSED_PENDING_RC13_OWNER_RETEST` |
| 9 | Independent external assurance | `NOT COMPLETE` |
| 10 | Production go/no-go | `NOT STARTED` |

DTMO is **not production ready**.

## RC13 — current gate

RC13.1–RC13.5 and the earlier accountable owner acceptance remain historical evidence. Subsequent owner retesting exposed additional functional/runtime defects; repository-controlled repairs have now been completed through PR #161.

### Repair sequence

1. PR #159 repaired refresh behavior, empty-data truthfulness, Chrome interactions, Administration clarity, graph empty states and menu version clutter.
2. PR #160 repaired the canonical runtime image so `tools/provision_grafana_reader.py` is available to `grafana-db-provision`.
3. PR #161 removed duplicate default Prometheus datasource provisioning and added a real Grafana 13.1.0 runtime health gate.

PR #161 final exact head `e471d6368639a45cee6dccadd353a9068e5205e9` completed every returned workflow successfully and merged with expected-head protection as `79037f82d0e6f42fa1cf57457b02f3aeaaa92bd5`.

### Remaining RC13 acceptance

The accountable project owner must retest current merged `main` and verify:

1. local Compose startup is successful;
2. Grafana remains healthy without datasource provisioning restart loops;
3. `Alles vernieuwen` executes a real refresh and exposes loading/success/failure state;
4. empty canonical intelligence never produces a false `Data bijgewerkt` claim;
5. zero-only intelligence datasets render explicit empty states;
6. Chrome navigation and operator controls work without page/console errors;
7. governed Administration is the primary admin workspace;
8. after source ingestion, Intelligence, Overview and analytics update truthfully;
9. authorization/publication boundaries remain unchanged.

Only explicit accountable owner acceptance closes RC13.

## Phase 8 — paused external staging gate

PR #157 remains valid historical/preparatory evidence. The external deployment identity record remains fail-closed and issue #158 remains open but paused.

No Phase 8 evidence may advance while RC13 awaits owner retest. After successful owner acceptance, Phase 8 may return to `READY_FOR_EXTERNAL_VALIDATION / PENDING_EXTERNAL_DEPLOYMENT_IDENTITY` and issue #158 can resume.

Repository CI, Docker Compose and staging emulators cannot substitute for a real staging deployment or owner functional acceptance.

## Phase 9 — external assurance

Phase 9 covers independent penetration testing, representative load/stress validation, full backup/restoration in the production-equivalent environment, platform hardening, secrets-management acceptance and required operational/stakeholder approval.

## Phase 10 — production decision

Phase 10 is the formal production go/no-go and begins only after all prior gates are complete and reviewable.

## Exactly one next priority

**Issue #150 — accountable project-owner local Compose and functional-console retest of current merged `main`.**

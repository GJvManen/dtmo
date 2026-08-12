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

RC13.1–RC13.5 and the earlier owner acceptance remain historical evidence. A subsequent owner retest on 2026-08-12 found blocking usability defects involving Overview refresh, truthful empty-data status, Chrome button interaction, menu clutter, Administration clarity and graph empty-state behavior.

Issue #150 is reopened and controls the current readiness decision.

### Current repair acceptance

The repair must prove:

1. `Alles vernieuwen` executes a real refresh and exposes loading/success/failure state;
2. empty canonical intelligence never produces a false `Data bijgewerkt` claim;
3. zero-only intelligence datasets render explicit empty states;
4. Chrome navigation and operator controls work without page/console errors;
5. the menu version badge is removed;
6. governed Administration is the primary admin workspace;
7. authorization/publication boundaries remain unchanged;
8. complete exact-head CI succeeds;
9. the accountable project owner retests and explicitly accepts the merged repair.

## Phase 8 — paused external staging gate

PR #157 remains valid historical/preparatory evidence. The external deployment identity record remains fail-closed and issue #158 remains open but paused.

No Phase 8 evidence may advance while RC13 is reopened. After a successful owner retest, Phase 8 may return to `READY_FOR_EXTERNAL_VALIDATION / PENDING_EXTERNAL_DEPLOYMENT_IDENTITY` and issue #158 can resume.

Repository CI, Docker Compose and staging emulators cannot substitute for a real staging deployment or owner functional acceptance.

## Phase 9 — external assurance

Phase 9 covers independent penetration testing, representative load/stress validation, full backup/restoration in the production-equivalent environment, platform hardening, secrets-management acceptance and required operational/stakeholder approval.

## Phase 10 — production decision

Phase 10 is the formal production go/no-go and begins only after all prior gates are complete and reviewable.

## Exactly one next priority

**Issue #150 — complete the canonical-console usability repair, exact-head Chrome/browser evidence, merge and accountable project-owner retest.**

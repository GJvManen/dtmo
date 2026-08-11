# RC13 — Functional Console Acceptance Gate

Status: `AWAITING_OWNER_RETEST` — repository-controlled RC13.1–RC13.5 are `PASS`; accountable project-owner functional retest remains.

## Trigger

A project-owner functional test of `http://localhost:8000/` on 2026-08-11 found that the repository-controlled product was not yet functionally usable despite the earlier RC12 close-out. RC13 supersedes the previous Phase 8 handoff until the repaired product journey is both technically proven and explicitly retested by the accountable project owner.

## Required acceptance journey

The canonical console must support, as one usable product journey:

1. Overview with useful statistics and graphics;
2. canonical recent Intelligence independently of OpenSearch search availability;
3. Sources & Catalog with truthful execution states;
4. register, enable/configure and manually execute an eligible framework source;
5. fetched/inserted/indexed feedback, connector health and resulting Intelligence state;
6. native Visual analytics without a separate Grafana login prerequisite;
7. governed principal/role administration without weakening token or service-account boundaries;
8. repository-backed Governance coverage, mappings, provenance and authority boundaries;
9. preservation of RBAC, separation of duties, privacy, provenance, auditability, human review and separate external share approval.

## Accepted RC13 slices

- **RC13.1 — PASS.** PR #151 merged as `95c4a5b072d141f50a02d23f8bf9abb862d6f8e2`.
- **RC13.2 — PASS.** PR #152 merged as `b8c254c5d099cde5dca624aa85b17c320594847e`.
- **RC13.3 — PASS.** PR #153 merged as `2e1029a43f7b44d8525fb89197d0a10458a3e992`.
- **RC13.4 — PASS.** PR #154 merged as `21672aaf1cf097228699810660eaac167da842d6`; exact head `0a227cb9f3972504287a6f7f064d6df18b76fbed` completed the full returned workflow set successfully.
- **RC13.5 — PASS within the repository-controlled evidence boundary.** PR #155 merged as `d6f83557ab18d26f82ad6289b1b95f728346631d`. Exact head `56805ec4ead5a14e9a2f776f84df42eb772302a4` completed the full returned workflow matrix successfully, including RC4 Quality Gate #815, RC13 Full Functional Console Acceptance Gate #1, RC13 Functional Console Browser E2E Gate #13, RC13 Single-session Visual Analytics Gate #8, RC13 Governed Administration RBAC Gate #7, RC13 Governance Knowledge Surface Gate #4 and Open Source Governance Gate #279.

## RC13.5 integrated browser evidence

`RC13 Full Functional Console Acceptance Gate` executed one Chromium browser context through:

**Overview → Intelligence → Sources & Catalog → source register/enable/run → Intelligence state update → Visual analytics → Administration → Governance → Overview state confirmation.**

The gate proves that the repaired RC13 slices operate together in one canonical session and fail closed when the browser journey is unsuccessful.

## Owner acceptance boundary

RC13.5 CI is **synthetic repository-controlled evidence only**. It does not manufacture the project owner's functional acceptance.

The only remaining RC13 acceptance action is an accountable project-owner functional retest of the repaired local canonical product. The retest must verify actual usability, not merely the presence of controls.

If the owner explicitly accepts the complete journey, RC13 may close and Phase 8 may return to external-validation readiness. If any blocker remains, RC13 stays open and the finding becomes the next repair priority.

## Phase 8 boundary

Phase 8 external staging validation is **`PAUSED_PENDING_RC13_OWNER_RETEST`**.

Repository CI, Docker Compose, staging emulators, successful builds or UI-control presence do not substitute for the owner-observed repaired product journey.

## Release rule

Do not claim `READY_FOR_EXTERNAL_VALIDATION`, external staging acceptance, pentest readiness or production readiness until the accountable project-owner retest explicitly accepts the repaired canonical console.

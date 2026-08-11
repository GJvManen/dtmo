# RC13 — Functional Console Acceptance Gate

Status: `PASS`

## Trigger

A project-owner functional test of `http://localhost:8000/` on 2026-08-11 found that the repository-controlled product was not yet functionally usable despite the earlier RC12 close-out. RC13 superseded the previous Phase 8 handoff until the repaired product journey was technically proven and explicitly retested by the accountable project owner.

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
- **RC13.4 — PASS.** PR #154 merged as `21672aaf1cf097228699810660eaac167da842d6`.
- **RC13.5 — PASS within the repository-controlled evidence boundary.** PR #155 merged as `d6f83557ab18d26f82ad6289b1b95f728346631d`; exact head `56805ec4ead5a14e9a2f776f84df42eb772302a4` completed the full returned workflow matrix successfully, including RC4 Quality Gate #815, RC13 Full Functional Console Acceptance Gate #1, RC13 Functional Console Browser E2E Gate #13, RC13 Single-session Visual Analytics Gate #8, RC13 Governed Administration RBAC Gate #7, RC13 Governance Knowledge Surface Gate #4 and Open Source Governance Gate #279.
- **RC13.5 status reconciliation — PASS.** PR #156 merged as `e0119b2eb1865ad5b4f2634fd71ccd809fba96a0` after exact head `22a04c8511c5d43cbf78b1ddb39a7be993dc7a1a` completed the full returned workflow set successfully.

## Integrated browser evidence

`RC13 Full Functional Console Acceptance Gate` executed one Chromium browser context through:

**Overview → Intelligence → Sources & Catalog → source register/enable/run → Intelligence state update → Visual analytics → Administration → Governance → Overview state confirmation.**

The CI journey used bounded synthetic repository-controlled fixtures. That evidence proves integration but does not manufacture manual owner acceptance.

## Accountable owner acceptance

On **2026-08-12**, the project owner explicitly accepted the repaired canonical product journey with the statement:

`RC13 owner retest akkoord`

No unprovided browser, operating-system, recording, assistive-technology or environment details are inferred or fabricated.

## Final decision

**RC13 = PASS.** Issue #150 is closed as completed.

The accepted owner retest closes the functional-console remediation programme. Phase 8 may proceed to real production-equivalent staging validation.

## Phase 8 boundary

RC13 acceptance does **not** establish Phase 8 staging acceptance. Real staging must still satisfy `PHASE8_STAGING_DEPLOYMENT_PARITY_GATE.md` against one immutable production-equivalent deployment identity.

Repository CI, Docker Compose and staging emulators remain supporting engineering evidence only and cannot substitute for real staging evidence.

## Release rule

Do not claim Phase 8 `PASS`, pentest readiness or production readiness until the separate external staging, assurance and production gates are complete.
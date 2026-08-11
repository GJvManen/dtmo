# DTMO Production Readiness Roadmap

## Purpose

This roadmap separates **repository-controlled engineering acceptance**, **functional product acceptance** and **external staging/assurance/production approval**. A phase is complete only when its own evidence boundary has been satisfied.

## Current status — 2026-08-11

| Phase | Scope | Status |
|---|---|---|
| 1 | CI and workflow integrity | `PASS` |
| 2 | Application security and identity | `PASS` |
| 3 | Data integrity and recovery | `PASS` |
| 4 | Connector reliability and provenance | `PASS` |
| 5 | Performance and scalability | `PASS` |
| 6 | Accessibility and operational UX | `PASS` — project-owner manual/external acceptance recorded 2026-08-11 |
| 7 | Observability and incident operations | `PASS` |
| RC13 | Functional unified-console acceptance | `BLOCKED_INTERNAL` — RC13.1–RC13.4 accepted; RC13.5 current |
| 8 | Real staging acceptance | `PAUSED_PENDING_RC13` |
| 9 | Independent external assurance | `NOT COMPLETE` |
| 10 | Production go/no-go | `NOT STARTED` |

DTMO is **not production ready**.

## Why RC13 was inserted

The RC11/RC12 repository-controlled implementation and CI gates established the connector framework, unified console and analytics architecture, but a project-owner functional test of the canonical console on 2026-08-11 identified product gaps that prior presence/contract tests did not catch.

The earlier Phase 8 `READY_FOR_EXTERNAL_VALIDATION` claim remains withdrawn. Issue #150 and `docs/qa/RC13_FUNCTIONAL_CONSOLE_ACCEPTANCE_GATE.md` are authoritative for the remediation.

## Accepted RC13 slices

### RC13.1 — source-to-intelligence path

`PASS`. PR #151 merged as `95c4a5b072d141f50a02d23f8bf9abb862d6f8e2`. Browser evidence proves source state → register → enable/configure → run → ingest/index → recent canonical intelligence → updated Overview statistics.

### RC13.2 — single-session visual analytics

`PASS`. PR #152 merged as `b8c254c5d099cde5dca624aa85b17c320594847e`. Native analytics are canonical; normal use does not request Grafana; Grafana remains separately authenticated for advanced/operations use.

### RC13.3 — Administration/RBAC

`PASS`. PR #153 merged as `2e1029a43f7b44d8525fb89197d0a10458a3e992`. Acceptance covers persistent managed principals/roles, immutable built-in roles, human-admin authorization, service-account isolation, self-management blocking, final-admin protection, tamper-evident auditing and explicit external IdP/token reconciliation.

### RC13.4 — Governance knowledge surface

`PASS`. PR #154 merged as `21672aaf1cf097228699810660eaac167da842d6` after complete exact-head success on `0a227cb9f3972504287a6f7f064d6df18b76fbed`, including RC4 Quality Gate #813, RC13 Governance Knowledge Surface Gate #3 and Open Source Governance Gate #278.

The canonical Governance area now distinguishes actual repository-backed mappings from external framework context. Normenkader IBP and MITRE ATT&CK remain `UNMAPPED`, CVSS remains `CONTEXT_ONLY`, and internal DTMO governance mappings remain `MAPPED_INTERNAL`. Missing crosswalks are not inferred.

## RC13.5 — complete console acceptance

Status: `PENDING_CI` / current and only engineering priority.

One exact PR head must pass `RC13 Full Functional Console Acceptance Gate`, which uses one Chromium browser context to exercise:

**Overview → Intelligence → Sources & Catalog → register/enable/run → Intelligence update → Visual analytics → Administration → Governance → Overview state confirmation.**

The browser evidence must prove the accepted RC13 slices work together in one canonical session, including source-to-intelligence state propagation, native analytics without a Grafana second-login dependency, governed RBAC mutations, Governance provenance and authority boundaries.

Synthetic browser evidence cannot itself close RC13. After exact-head CI succeeds and RC13.5 is merged, the accountable project owner must functionally retest the repaired local product. Only an explicit successful owner retest may close RC13 and restore Phase 8 readiness for external validation.

## Identity-provider boundary

DTMO validates externally issued bearer tokens and does not currently operate an internal production token issuer. Managed assignments are governed provisioning state and do not mint, forge or rewrite active bearer tokens. Production role changes require identity-provider reconciliation or token reissue.

## Phase 8 — paused external staging gate

Phase 8 requires one immutable real staging deployment identity and the deployment-parity evidence classes defined in `docs/qa/PHASE8_STAGING_DEPLOYMENT_PARITY_GATE.md`. External activity remains paused until RC13.5 exact-head acceptance and accountable owner functional retest are complete.

Repository CI, Docker Compose, staging emulators and component smoke tests are supporting engineering evidence only.

## Phase 9 — external assurance

Phase 9 covers independent penetration testing, representative load/stress validation, full backup/restoration in the production-equivalent environment, platform hardening, secrets-management acceptance and required operational/stakeholder approval.

## Phase 10 — production decision

Phase 10 is the formal production go/no-go and begins only after all blocking functional, staging and external-assurance evidence is complete and reviewable.

## Exactly one next priority

**RC13.5 — complete exact-head canonical-console browser acceptance, then obtain accountable project-owner functional retest.**

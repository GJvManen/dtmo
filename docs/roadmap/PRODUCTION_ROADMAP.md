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
| RC13 | Functional unified-console acceptance | `BLOCKED_INTERNAL` — RC13.1/13.2 accepted; RC13.3 current |
| 8 | Real staging acceptance | `PAUSED_PENDING_RC13` |
| 9 | Independent external assurance | `NOT COMPLETE` |
| 10 | Production go/no-go | `NOT STARTED` |

DTMO is **not production ready**.

## Why RC13 was inserted

The RC11/RC12 repository-controlled implementation and CI gates established the connector framework, unified console and analytics architecture, but a project-owner functional test of the canonical console on 2026-08-11 identified product gaps that prior presence/contract tests did not catch.

The earlier Phase 8 `READY_FOR_EXTERNAL_VALIDATION` claim remains withdrawn. Issue #150 and `docs/qa/RC13_FUNCTIONAL_CONSOLE_ACCEPTANCE_GATE.md` are authoritative for the remediation.

## Accepted repository-controlled baseline

The accepted engineering baseline remains valid within its original evidence boundaries:

- governed connector/source framework and operational vendor onboarding;
- canonical unified DTMO console architecture;
- source registry and execution APIs;
- PostgreSQL canonical intelligence persistence and OpenSearch search indexing;
- native DTMO analytics plus authenticated Prometheus/Grafana operations components;
- recovery, performance, browser/accessibility and observability gates;
- exact-head CI and expected-head protected merge discipline.

RC13 does **not** invalidate those engineering controls. It establishes that a production candidate also needs a complete, owner-usable product journey rather than only component/API/presence evidence.

## RC13 — functional product acceptance

### RC13.1 — source-to-intelligence path

Status: `PASS` within the RC13.1 evidence boundary.

PR #151 merged on 2026-08-11 as `95c4a5b072d141f50a02d23f8bf9abb862d6f8e2`. The accepted browser journey proves source state → register → enable/configure → run → ingest/index → recent canonical intelligence → updated Overview statistics.

### RC13.2 — single-session visual analytics

Status: `PASS` within the RC13.2 evidence boundary.

PR #152 merged on 2026-08-11 as `b8c254c5d099cde5dca624aa85b17c320594847e` after the complete exact-head workflow set succeeded. Accepted evidence includes RC4 Quality Gate #805, RC13 Functional Console Browser E2E Gate #6 and RC13 Single-session Visual Analytics Gate #1.

Acceptance proves:

1. native severity distribution renders;
2. native source distribution renders;
3. connector-health distribution renders;
4. review-status distribution renders;
5. normal Visual analytics navigation performs no `/grafana/` request;
6. no separately authenticated Grafana shell is exposed in the canonical user journey;
7. Grafana anonymous access remains disabled;
8. Grafana remains available as a separately authenticated operations/advanced component without an authentication bypass.

### RC13.3 — Administration/RBAC

Status: `PENDING_CI` / current priority.

Administration acceptance requires:

1. a persistent managed-principal registry;
2. persistent role assignments with known built-in `Role` values;
3. a read-only role/permission catalog derived from server-side policy;
4. all RBAC mutations protected by `manage:users` and a human `admin` role;
5. service accounts restricted to the `service_account` role and barred from human/admin combinations;
6. administrator self-management blocked;
7. the final active managed admin protected from removal/deactivation;
8. principal create/update mutations recorded in the existing tamper-evident audit chain with request IDs;
9. the canonical Administration tab supports create, role update and activate/deactivate flows;
10. the UI states truthfully that production bearer-token claims require external identity-provider reconciliation/token reissue and are not silently rewritten by DTMO;
11. arbitrary custom token roles are not introduced through browser input;
12. a dedicated exact-head Chromium workflow proves the actual Administration flow.

### RC13.4 — Governance knowledge surface

Governance must present the applicable frameworks and mappings used by the project, including Normenkader IBP, MITRE ATT&CK and CVSS context, together with DTMO authority/approval boundaries.

### RC13.5 — complete console acceptance

One exact head must pass the complete canonical-console functional browser journey and all registered CI gates. Only after RC13.5 may Phase 8 return to `READY_FOR_EXTERNAL_VALIDATION`.

## Identity-provider boundary

DTMO validates externally issued bearer tokens and does not currently operate an internal production token issuer. RC13.3 managed assignments are therefore governed provisioning/assignment state. They do not mint, forge or rewrite active bearer tokens. Production role changes require identity-provider reconciliation or token reissue before changed claims become active.

This is a deliberate security boundary, not an incomplete authorization shortcut.

## Phase 6 acceptance

Phase 6 remains accepted. On 2026-08-11 the project owner explicitly confirmed personal/manual acceptance of the remaining external accessibility scope. The repository does not fabricate unprovided environment/version or recording details.

## Phase 8 — paused external staging gate

Phase 8 requires one immutable real staging deployment identity and the ten deployment-parity evidence classes defined in `docs/qa/PHASE8_STAGING_DEPLOYMENT_PARITY_GATE.md`. That external activity is intentionally paused until RC13 functional product acceptance is complete.

Repository CI, Docker Compose, staging emulators and component smoke tests remain supporting engineering evidence and are not substitutes for either RC13 owner-observed functional acceptance or Phase 8 real staging validation.

## Phase 9 — external assurance

Phase 9 covers independent penetration testing, representative load/stress validation, full backup/restoration in the production-equivalent environment, production platform hardening, secrets-management acceptance and required operational/stakeholder approval.

External pentesting is deferred until RC13 and Phase 8 establish a functionally usable, immutable staging target.

## Phase 10 — production decision

Phase 10 is the formal production go/no-go and begins only after all blocking functional, staging and external-assurance evidence is complete and reviewable.

## Exactly one next priority

**RC13.3 — complete and exact-head accept governed Administration/RBAC in the canonical console.**

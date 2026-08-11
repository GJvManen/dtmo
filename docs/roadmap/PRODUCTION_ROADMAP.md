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
| RC13 | Functional unified-console acceptance | `BLOCKED_INTERNAL` — RC13.1/13.2/13.3 accepted; RC13.4 current |
| 8 | Real staging acceptance | `PAUSED_PENDING_RC13` |
| 9 | Independent external assurance | `NOT COMPLETE` |
| 10 | Production go/no-go | `NOT STARTED` |

DTMO is **not production ready**.

## Why RC13 was inserted

The RC11/RC12 repository-controlled implementation and CI gates established the connector framework, unified console and analytics architecture, but a project-owner functional test of the canonical console on 2026-08-11 identified product gaps that prior presence/contract tests did not catch.

The earlier Phase 8 `READY_FOR_EXTERNAL_VALIDATION` claim remains withdrawn. Issue #150 and `docs/qa/RC13_FUNCTIONAL_CONSOLE_ACCEPTANCE_GATE.md` are authoritative for the remediation.

## Accepted repository-controlled baseline

The accepted engineering baseline remains valid within its original evidence boundaries: governed connector/source framework, canonical unified console, source registry/execution APIs, PostgreSQL canonical intelligence, OpenSearch indexing, native analytics, authenticated operations components, recovery/performance/browser/accessibility/observability gates and exact-head protected merge discipline.

RC13 does not invalidate those controls. It establishes that a production candidate also needs a complete, owner-usable product journey rather than component/API/presence evidence alone.

## RC13 — functional product acceptance

### RC13.1 — source-to-intelligence path

Status: `PASS` within the RC13.1 evidence boundary.

PR #151 merged on 2026-08-11 as `95c4a5b072d141f50a02d23f8bf9abb862d6f8e2`. The accepted browser journey proves source state → register → enable/configure → run → ingest/index → recent canonical intelligence → updated Overview statistics.

### RC13.2 — single-session visual analytics

Status: `PASS` within the RC13.2 evidence boundary.

PR #152 merged on 2026-08-11 as `b8c254c5d099cde5dca624aa85b17c320594847e`. Accepted evidence includes RC4 Quality Gate #805, RC13 Functional Console Browser E2E Gate #6 and RC13 Single-session Visual Analytics Gate #1. Native analytics are canonical; normal use does not request Grafana; Grafana remains separately authenticated for advanced/operations use.

### RC13.3 — Administration/RBAC

Status: `PASS` within the RC13.3 evidence boundary.

PR #153 merged on 2026-08-11 as `2e1029a43f7b44d8525fb89197d0a10458a3e992` after complete exact-head success on `b828b9b2dbb2f8794bfe7c13ec6e7dd0bdafb22f`, including RC4 Quality Gate #809 and RC13 Governed Administration RBAC Gate #3.

Acceptance covers persistent managed principals/roles, immutable built-in roles, human-admin + `manage:users`, service-account isolation, self-management blocking, final-admin lockout protection, tamper-evident mutation auditing, canonical create/update/deactivate UI and explicit external IdP/token reconciliation. Arbitrary browser-defined production token roles remain prohibited.

### RC13.4 — Governance knowledge surface

Status: `PENDING_CI` / current priority.

The authoritative registry is `docs/governance/GOVERNANCE_MAPPING_REGISTRY.md`. The canonical Governance area must render a read-only authenticated snapshot that distinguishes **actual repository mappings** from external-framework context.

Required truthful coverage:

1. Normenkader IBP — `UNMAPPED` until a control-level repository crosswalk exists;
2. MITRE ATT&CK — `UNMAPPED` until a technique-level repository mapping dataset exists;
3. CVSS — `CONTEXT_ONLY` while canonical ingest has severity/free metadata but no first-class CVSS vector/base-score field;
4. DTMO security/release governance — `MAPPED_INTERNAL`, with each mapping traceable to authoritative repository sections;
5. publication/share, human review, service-account and evidence claim boundaries remain visible;
6. no missing crosswalk is inferred from semantic similarity;
7. a dedicated exact-head Chromium workflow proves the canonical Governance journey.

### RC13.5 — complete console acceptance

One exact head must pass the complete canonical-console functional browser journey and all registered CI gates. Accountable project-owner functional acceptance must then be recorded. Only after RC13.5 may Phase 8 return to `READY_FOR_EXTERNAL_VALIDATION`.

## Identity-provider boundary

DTMO validates externally issued bearer tokens and does not currently operate an internal production token issuer. RC13.3 managed assignments are therefore governed provisioning/assignment state. They do not mint, forge or rewrite active bearer tokens. Production role changes require identity-provider reconciliation or token reissue before changed claims become active.

## Phase 6 acceptance

Phase 6 remains accepted. On 2026-08-11 the project owner explicitly confirmed personal/manual acceptance of the remaining external accessibility scope. The repository does not fabricate unprovided environment/version or recording details.

## Phase 8 — paused external staging gate

Phase 8 requires one immutable real staging deployment identity and the deployment-parity evidence classes defined in `docs/qa/PHASE8_STAGING_DEPLOYMENT_PARITY_GATE.md`. That external activity is intentionally paused until RC13 functional product acceptance is complete.

Repository CI, Docker Compose, staging emulators and component smoke tests remain supporting engineering evidence and are not substitutes for either RC13 owner-observed functional acceptance or Phase 8 real staging validation.

## Phase 9 — external assurance

Phase 9 covers independent penetration testing, representative load/stress validation, full backup/restoration in the production-equivalent environment, production platform hardening, secrets-management acceptance and required operational/stakeholder approval.

External pentesting is deferred until RC13 and Phase 8 establish a functionally usable, immutable staging target.

## Phase 10 — production decision

Phase 10 is the formal production go/no-go and begins only after all blocking functional, staging and external-assurance evidence is complete and reviewable.

## Exactly one next priority

**RC13.4 — complete and exact-head accept the repository-backed Governance knowledge surface in the canonical console.**

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
| RC13 | Functional unified-console acceptance | `BLOCKED_INTERNAL` — remediation in progress |
| 8 | Real staging acceptance | `PAUSED_PENDING_RC13` |
| 9 | Independent external assurance | `NOT COMPLETE` |
| 10 | Production go/no-go | `NOT STARTED` |

DTMO is **not production ready**.

## Why RC13 was inserted

The RC11/RC12 repository-controlled implementation and CI gates established the connector framework, unified console and graphical analytics architecture, but a project-owner functional test of the canonical console on 2026-08-11 identified product gaps that prior presence/contract tests did not catch.

The earlier Phase 8 `READY_FOR_EXTERNAL_VALIDATION` claim is therefore withdrawn. Issue #150 and `docs/qa/RC13_FUNCTIONAL_CONSOLE_ACCEPTANCE_GATE.md` are authoritative for the remediation.

## Accepted repository-controlled baseline

The accepted engineering baseline remains valid within its original evidence boundaries:

- governed connector/source framework and operational vendor onboarding;
- canonical unified DTMO console architecture;
- source registry and execution APIs;
- PostgreSQL canonical intelligence persistence and OpenSearch search indexing;
- Prometheus/Grafana observability components;
- recovery, performance, browser/accessibility and observability gates;
- exact-head CI and expected-head protected merge discipline.

RC13 does **not** invalidate those engineering controls. It establishes that a production candidate also needs a complete, owner-usable product journey rather than only component/API/presence evidence.

## RC13 — functional product acceptance

### RC13.1 — source-to-intelligence path

Required journey:

1. open the canonical console;
2. view meaningful platform/source/intelligence statistics;
3. see built-in, supported framework and research/reference sources with truthful state;
4. register supported framework sources;
5. enable/disable and configure them;
6. execute an eligible built-in or framework source;
7. process fetched records through canonical ingestion;
8. show run/fetched/inserted/indexed status;
9. show resulting recent intelligence directly from the canonical database;
10. update Overview and analytics from the resulting data.

Acceptance requires a Chromium browser journey that interacts with the actual console controls; checking only that strings/buttons exist in generated HTML is insufficient.

### RC13.2 — visual analytics

Native graphical/statistical analytics must work without a separate Grafana authentication step being required for normal product use. Grafana may remain as an advanced governed layer.

### RC13.3 — Administration/RBAC

Administration must provide governed user/role-assignment management through server-side authorization while preserving least privilege and separation of duties.

### RC13.4 — Governance knowledge surface

Governance must present the applicable frameworks and mappings used by the project, including Normenkader IBP, MITRE ATT&CK and CVSS context, together with DTMO authority/approval boundaries.

### RC13.5 — complete console acceptance

One exact head must pass the complete canonical-console functional browser journey and all registered CI gates. Only after RC13.5 may Phase 8 return to `READY_FOR_EXTERNAL_VALIDATION`.

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

**RC13.1 — complete the source-to-intelligence functional path and exact-head Chromium acceptance.**

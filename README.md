# DTMO

## Dutch Threat Monitoring for Education

**DTMO** is an open Cyber Threat Intelligence platform for the education sector. It combines vulnerability intelligence, vendor advisories, provenance, operational health, investigation and governance in one controlled platform.

**Release candidate:** `16.0.0rc12`  
**Engineering status:** Phases 1–7 accepted; RC13 reopened  
**RC13 product status:** `REOPENED / BLOCKED_INTERNAL`  
**External staging:** `PAUSED_PENDING_RC13_REPAIR_AND_OWNER_RETEST`  
**License:** Apache-2.0

> **Current release decision:** DTMO is not production ready. A subsequent project-owner functional retest on 2026-08-12 found blocking canonical-console usability defects after the earlier RC13 acceptance. Issue #150 is reopened and Phase 8 is paused until the repair is exact-head green, merged and explicitly accepted by the project owner again.

## Product scope

DTMO provides:

- **Unified threat intelligence** from official public and vendor sources;
- **Governed source operations** with registration, execution, provenance and connector health;
- **Threat investigation** with recent canonical intelligence and governed search;
- **Native visual analytics** inside the canonical DTMO session;
- **Governed Administration/RBAC** for managed principals and role assignments;
- **Repository-backed Governance knowledge** with explicit mapping/provenance truth boundaries;
- **Auditability, privacy and separation of duties** across ingestion, analysis, review and external share approval.

## RC13 functional acceptance — reopened

RC13.1–RC13.5 and the earlier project-owner acceptance remain valid historical evidence. The project owner subsequently found new product defects on 2026-08-12:

- Overview `Alles vernieuwen` was not a usable/reliable action;
- the console could report `Data bijgewerkt` while no intelligence data existed;
- buttons were not reliably functional under Chrome;
- the release/version badge in the navigation was unnecessary;
- Administration was insufficiently clear;
- graphs were not truthful/useful for empty datasets.

Repository inspection confirmed unconditional dashboard-success wording, zero-only trend rendering and stale/duplicated Administration composition. The earlier browser gate also did not explicitly gate refresh-all, zero-data semantics, Chrome page/console errors or broad button interaction.

The current repair therefore adds truthful refresh state, explicit graph empty states, Chrome-channel interaction regression coverage, a simplified Administration workspace and removal of the menu version badge.

## Historical RC13 evidence

1. **RC13.1 — source-to-intelligence — historical PASS.** PR #151.
2. **RC13.2 — single-session visual analytics — historical PASS.** PR #152.
3. **RC13.3 — Administration/RBAC — historical PASS.** PR #153.
4. **RC13.4 — Governance knowledge — historical PASS.** PR #154.
5. **RC13.5 — full integrated canonical-console browser acceptance — historical repository PASS.** PR #155.
6. **Earlier accountable owner functional retest — historical acceptance.** `RC13 owner retest akkoord` on 2026-08-12.
7. **Subsequent owner retest — blocking findings.** Current release decision is reopened.

Historical acceptance is not deleted or rewritten, but newer owner-observed evidence controls the current readiness decision.

## Phase 8 — paused

PR #157 and the fail-closed external deployment identity record remain historical/preparatory evidence. They do not permit Phase 8 to advance while RC13 is reopened.

Phase 8 is now `PAUSED_PENDING_RC13_REPAIR_AND_OWNER_RETEST`. External staging issue #158 is paused. After the canonical-console repair is exact-head green and merged, the project owner must retest the repaired local product before Phase 8 can resume.

## Governance mapping model

[`docs/governance/GOVERNANCE_MAPPING_REGISTRY.md`](docs/governance/GOVERNANCE_MAPPING_REGISTRY.md) remains authoritative:

- **Normenkader IBP:** `UNMAPPED`;
- **MITRE ATT&CK:** `UNMAPPED`;
- **CVSS:** `CONTEXT_ONLY`;
- **DTMO security & release governance:** `MAPPED_INTERNAL`.

Missing mappings are visible evidence and are never inferred.

## Security and governance model

DTMO preserves RBAC, least privilege, code-controlled roles, strict service-account/human-role separation, administrator safety controls, separate human review and external share approval, provenance, privacy/data minimization, tamper-evident auditability and request correlation. Connectors, CI, dashboards, Administration, Governance or staging access do not grant publication authority.

## Project status

| Phase | Scope | Status |
|---|---|---|
| 1–7 | Repository-controlled engineering | ✅ `PASS` |
| RC13 | Functional unified-console acceptance | ⛔ `REOPENED / BLOCKED_INTERNAL` |
| 8 | Real staging acceptance | ⏸ `PAUSED_PENDING_RC13_REPAIR_AND_OWNER_RETEST` |
| 9 | Independent external assurance | ⏳ `NOT COMPLETE` |
| 10 | Production go/no-go | ⏳ `NOT STARTED` |

The only current priority is **issue #150 — complete the canonical-console usability repair, exact-head Chrome/browser evidence and accountable owner retest**.

## Documentation

Start with [`docs/README.md`](docs/README.md). Current authoritative records include [`docs/project/CURRENT_STATE.md`](docs/project/CURRENT_STATE.md), [`docs/roadmap/PRODUCTION_ROADMAP.md`](docs/roadmap/PRODUCTION_ROADMAP.md), [`docs/qa/RC13_FUNCTIONAL_CONSOLE_ACCEPTANCE_GATE.md`](docs/qa/RC13_FUNCTIONAL_CONSOLE_ACCEPTANCE_GATE.md) and [`docs/qa/PHASE8_STAGING_DEPLOYMENT_PARITY_GATE.md`](docs/qa/PHASE8_STAGING_DEPLOYMENT_PARITY_GATE.md).

## Open source and responsible use

DTMO is licensed under the **Apache License, Version 2.0** (`Apache-2.0`). Use DTMO only with lawful access to intelligence sources and infrastructure. A technically successful connector does not itself establish legal permission to collect, process or redistribute third-party material.

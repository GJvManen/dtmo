# DTMO

## Dutch Threat Monitoring for Education

**DTMO** is an open Cyber Threat Intelligence platform for the education sector. It combines vulnerability intelligence, vendor advisories, provenance, operational health, investigation and governance in one controlled platform.

**Release candidate:** `16.0.0rc12`  
**Engineering status:** Phases 1–7 accepted  
**RC13 product status:** `AWAITING_OWNER_RETEST_AFTER_REPAIR`  
**External staging:** `PAUSED_PENDING_RC13_OWNER_RETEST`  
**License:** Apache-2.0

> **Current release decision:** DTMO is not production ready. Repository-controlled repairs through PR #161 are green and merged, but RC13 still requires accountable project-owner retesting of current `main`. Phase 8 remains paused until that explicit acceptance.

## Product scope

DTMO provides:

- **Unified threat intelligence** from official public and vendor sources;
- **Governed source operations** with registration, execution, provenance and connector health;
- **Threat investigation** with recent canonical intelligence and governed search;
- **Native visual analytics** inside the canonical DTMO session;
- **Governed Administration/RBAC** for managed principals and role assignments;
- **Repository-backed Governance knowledge** with explicit mapping/provenance truth boundaries;
- **Auditability, privacy and separation of duties** across ingestion, analysis, review and external share approval.

## RC13 current state

RC13.1–RC13.5 and the earlier owner acceptance remain historical evidence. Subsequent owner retesting exposed additional issues; repository-controlled repairs now include:

1. **PR #159 — console usability repair** — merged as `b4fffecc47f87b1edab8258514eaa130d949c195`;
2. **PR #160 — Compose runtime packaging repair** — merged as `dc6f8c6a2d3ea3e7efc8c45460caea607aa63d9c`;
3. **PR #161 — Grafana datasource provisioning repair** — final exact head `e471d6368639a45cee6dccadd353a9068e5205e9`, complete returned workflow matrix `completed/success`, merged with expected-head protection as `79037f82d0e6f42fa1cf57457b02f3aeaaa92bd5`.

Known repository blockers are therefore resolved. Automated evidence remains repository-controlled and does not substitute for accountable owner-observed functionality.

## Required owner retest

Current merged `main` must still demonstrate that:

- local Compose starts without the former Grafana provisioner file-not-found failure;
- Grafana remains healthy without the duplicate-default datasource restart loop;
- Overview refresh behaves truthfully;
- empty intelligence does not report false success;
- navigation and controls work in Chrome;
- Administration is clear;
- empty graphs are explicit;
- ingested source data flows through Intelligence, Overview and analytics correctly.

## Historical RC13 evidence

1. **RC13.1 — source-to-intelligence — historical PASS.** PR #151.
2. **RC13.2 — single-session visual analytics — historical PASS.** PR #152.
3. **RC13.3 — Administration/RBAC — historical PASS.** PR #153.
4. **RC13.4 — Governance knowledge — historical PASS.** PR #154.
5. **RC13.5 — full integrated canonical-console browser acceptance — historical repository PASS.** PR #155.
6. **Earlier accountable owner functional retest — historical acceptance.** `RC13 owner retest akkoord` on 2026-08-12.
7. **Subsequent owner testing — additional blockers found and repaired by PRs #159–#161.** Current decision is owner retest pending.

Historical acceptance is not deleted or rewritten; newer evidence controls the current readiness decision.

## Phase 8 — paused

PR #157 and the fail-closed external deployment identity record remain historical/preparatory evidence. Issue #158 remains paused while RC13 awaits owner retest.

After explicit owner acceptance, Phase 8 may return to `READY_FOR_EXTERNAL_VALIDATION / PENDING_EXTERNAL_DEPLOYMENT_IDENTITY`. Repository CI, Docker Compose and staging emulators cannot substitute for real staging evidence.

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
| RC13 | Functional unified-console acceptance | ⏳ `AWAITING_OWNER_RETEST_AFTER_REPAIR` |
| 8 | Real staging acceptance | ⏸ `PAUSED_PENDING_RC13_OWNER_RETEST` |
| 9 | Independent external assurance | ⏳ `NOT COMPLETE` |
| 10 | Production go/no-go | ⏳ `NOT STARTED` |

The only current priority is **issue #150 — accountable owner retest of current merged `main`**.

## Documentation

Start with [`docs/README.md`](docs/README.md). Current authoritative records include [`docs/project/CURRENT_STATE.md`](docs/project/CURRENT_STATE.md), [`docs/roadmap/PRODUCTION_ROADMAP.md`](docs/roadmap/PRODUCTION_ROADMAP.md), [`docs/qa/RC13_FUNCTIONAL_CONSOLE_ACCEPTANCE_GATE.md`](docs/qa/RC13_FUNCTIONAL_CONSOLE_ACCEPTANCE_GATE.md) and [`docs/qa/PHASE8_STAGING_DEPLOYMENT_PARITY_GATE.md`](docs/qa/PHASE8_STAGING_DEPLOYMENT_PARITY_GATE.md).

## Open source and responsible use

DTMO is licensed under the **Apache License, Version 2.0** (`Apache-2.0`). The repository governance entry points are `SECURITY.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SUPPORTED_VERSIONS.md`, `docs/legal/LICENSING.md` and `docs/legal/THIRD_PARTY.md`; canonical licence/notice files are `LICENSE` and `NOTICE`.

Use DTMO only with lawful access to intelligence sources and infrastructure. A technically successful connector does not itself establish legal permission to collect, process or redistribute third-party material.

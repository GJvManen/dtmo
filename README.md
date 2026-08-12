# DTMO

## Dutch Threat Monitoring for Education

**DTMO** is an open Cyber Threat Intelligence platform for the education sector. It combines vulnerability intelligence, vendor advisories, provenance, operational health, investigation and governance in one controlled platform.

**Release candidate:** `16.0.0rc12`  
**Engineering status:** Phases 1–7 accepted  
**RC13 product status:** `REOPENED / BLOCKED_INTERNAL`  
**External staging:** `PAUSED_PENDING_RC13_REPAIR_AND_OWNER_RETEST`  
**License:** Apache-2.0

> **Current release decision:** DTMO is not production ready. The latest owner retest confirmed the PR #160/#161 startup repairs, then exposed a source-catalog bootstrap HTTP 500 caused by an internal secret-reference contract mismatch. RC13 remains open and Phase 8 remains paused until that repository defect is repaired, exact-head green, merged and retested by the project owner.

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

RC13.1–RC13.5 and the earlier owner acceptance remain historical evidence. Later owner retesting has driven a bounded repair sequence:

1. **PR #159 — console usability repair** — merged as `b4fffecc47f87b1edab8258514eaa130d949c195`;
2. **PR #160 — Compose runtime packaging repair** — merged as `dc6f8c6a2d3ea3e7efc8c45460caea607aa63d9c`;
3. **PR #161 — Grafana datasource provisioning repair** — final exact head `e471d6368639a45cee6dccadd353a9068e5205e9`, complete returned workflow matrix `completed/success`, merged as `79037f82d0e6f42fa1cf57457b02f3aeaaa92bd5`.

The latest owner run progressed past both startup defects: the Grafana database-reader provisioner exited 0 and Grafana started without the former duplicate-default datasource restart loop.

That same run exposed the current blocker: `POST /api/v1/admin/sources/catalog/bootstrap` returns HTTP 500. The Cisco supported catalog entry uses `env:CISCO_OPENVULN_TOKEN`, which is also the runtime executor's supported form, while the registry previously rejected that syntax.

The current repair centralizes logical secret-reference validation, keeps raw secrets forbidden, makes `env:VARIABLE` canonical, normalizes legacy `env://VARIABLE`, and regression-tests idempotent supported catalog bootstrap.

## Owner-retest boundary

The owner run confirms the bounded PR #160/#161 startup repairs but is not full RC13 acceptance. Source-catalog bootstrap must first be repaired and exact-head green. After merge, owner testing resumes across source bootstrap/execution, Intelligence, Overview, analytics, Chrome controls and Administration.

A MinIO `InvalidAccessKeyId` also appeared during the same source-run attempt. The owner had explicitly identified the local `.env` as incorrect and asked to skip that configuration point, so it is not classified as the current repository defect and no successful-ingestion claim is made from that attempt.

## Historical RC13 evidence

1. **RC13.1 — source-to-intelligence — historical PASS.** PR #151.
2. **RC13.2 — single-session visual analytics — historical PASS.** PR #152.
3. **RC13.3 — Administration/RBAC — historical PASS.** PR #153.
4. **RC13.4 — Governance knowledge — historical PASS.** PR #154.
5. **RC13.5 — full integrated canonical-console browser acceptance — historical repository PASS.** PR #155.
6. **Earlier accountable owner functional retest — historical acceptance.** `RC13 owner retest akkoord` on 2026-08-12.
7. **Subsequent owner testing — newer blockers and bounded repairs.** Newer evidence controls the current decision.

Historical acceptance is not deleted or rewritten.

## Phase 8 — paused

PR #157 and the fail-closed external deployment identity record remain historical/preparatory evidence. Issue #158 remains paused while RC13 is blocked.

After explicit owner acceptance, Phase 8 may return to `READY_FOR_EXTERNAL_VALIDATION / PENDING_EXTERNAL_DEPLOYMENT_IDENTITY`. Repository CI, Docker Compose and staging emulators cannot substitute for real staging evidence.

## Governance mapping model

[`docs/governance/GOVERNANCE_MAPPING_REGISTRY.md`](docs/governance/GOVERNANCE_MAPPING_REGISTRY.md) remains authoritative:

- **Normenkader IBP:** `UNMAPPED`;
- **MITRE ATT&CK:** `UNMAPPED`;
- **CVSS:** `CONTEXT_ONLY`;
- **DTMO security & release governance:** `MAPPED_INTERNAL`.

Missing mappings are visible evidence and are never inferred.

## Security and governance model

DTMO preserves RBAC, least privilege, code-controlled roles, strict service-account/human-role separation, administrator safety controls, separate human review and external share approval, provenance, privacy/data minimization, tamper-evident auditability and request correlation. Credentialed integrations store logical secret references only; raw secret values remain forbidden. Connectors, CI, dashboards, Administration, Governance or staging access do not grant publication authority.

## Project status

| Phase | Scope | Status |
|---|---|---|
| 1–7 | Repository-controlled engineering | ✅ `PASS` |
| RC13 | Functional unified-console acceptance | ⛔ `REOPENED / BLOCKED_INTERNAL` |
| 8 | Real staging acceptance | ⏸ `PAUSED_PENDING_RC13_REPAIR_AND_OWNER_RETEST` |
| 9 | Independent external assurance | ⏳ `NOT COMPLETE` |
| 10 | Production go/no-go | ⏳ `NOT STARTED` |

The only current priority is **issue #150 — repair the source-catalog secret-reference contract, require exact-head CI, merge and resume accountable owner retesting**.

## Documentation

Start with [`docs/README.md`](docs/README.md). Current authoritative records include [`docs/project/CURRENT_STATE.md`](docs/project/CURRENT_STATE.md), [`docs/roadmap/PRODUCTION_ROADMAP.md`](docs/roadmap/PRODUCTION_ROADMAP.md), [`docs/qa/RC13_FUNCTIONAL_CONSOLE_ACCEPTANCE_GATE.md`](docs/qa/RC13_FUNCTIONAL_CONSOLE_ACCEPTANCE_GATE.md) and [`docs/qa/PHASE8_STAGING_DEPLOYMENT_PARITY_GATE.md`](docs/qa/PHASE8_STAGING_DEPLOYMENT_PARITY_GATE.md).

## Open source and responsible use

DTMO is licensed under the **Apache License, Version 2.0** (`Apache-2.0`). The repository governance entry points are `SECURITY.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SUPPORTED_VERSIONS.md`, `docs/legal/LICENSING.md` and `docs/legal/THIRD_PARTY.md`; canonical licence/notice files are `LICENSE` and `NOTICE`.

Use DTMO only with lawful access to intelligence sources and infrastructure. A technically successful connector does not itself establish legal permission to collect, process or redistribute third-party material.

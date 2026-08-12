# DTMO

## Dutch Threat Monitoring for Education

**DTMO** is an open Cyber Threat Intelligence platform for the education sector. It combines vulnerability intelligence, vendor advisories, provenance, operational health, investigation and governance in one controlled platform.

**Release candidate:** `16.0.0rc12`  
**Engineering status:** Phases 1–7 and RC13 accepted  
**RC13 product status:** `PASS`  
**External staging:** `READY_FOR_EXTERNAL_VALIDATION / PENDING_EXTERNAL_DEPLOYMENT_IDENTITY`  
**License:** Apache-2.0

> **Current release decision:** DTMO is not production ready. RC13 is complete after accountable project-owner functional acceptance on 2026-08-12. Phase 8 is now the active gate, beginning with one real production-equivalent staging environment and immutable deployment identity.

## Product scope

DTMO provides:

- **Unified threat intelligence** from official public and vendor sources;
- **Governed source operations** with registration, execution, provenance and connector health;
- **Threat investigation** with recent canonical intelligence and governed search;
- **Native visual analytics** inside the canonical DTMO session;
- **Governed Administration/RBAC** for managed principals and role assignments;
- **Repository-backed Governance knowledge** with explicit mapping/provenance truth boundaries;
- **Auditability, privacy and separation of duties** across ingestion, analysis, review and external share approval.

## RC13 functional acceptance

Project-owner testing on 2026-08-11 showed that earlier component-level CI did not prove a usable product journey. RC13 repaired and re-proved the canonical console before Phase 8.

1. **RC13.1 — source-to-intelligence — PASS.** PR #151.
2. **RC13.2 — single-session visual analytics — PASS.** PR #152.
3. **RC13.3 — Administration/RBAC — PASS.** PR #153.
4. **RC13.4 — Governance knowledge — PASS.** PR #154.
5. **RC13.5 — full integrated canonical-console browser acceptance — PASS within the repository-controlled evidence boundary.** PR #155 merged as `d6f83557ab18d26f82ad6289b1b95f728346631d` after exact head `56805ec4ead5a14e9a2f776f84df42eb772302a4` completed the full returned workflow matrix successfully.
6. **Accountable project-owner functional retest — PASS.** On 2026-08-12 the project owner explicitly stated `RC13 owner retest akkoord`. No unprovided test-environment metadata is inferred.

The accepted RC13.5 Chromium journey covered:

**Overview → Intelligence → Sources & Catalog → register/enable/run → Intelligence update → Visual analytics → Administration → Governance → Overview state confirmation.**

Issue #150 is closed as completed.

## Phase 8 — real staging acceptance

Phase 8 is now `READY_FOR_EXTERNAL_VALIDATION`, but **not PASS**.

The first active gate is **Phase 8.1 — external deployment identity**. DTMO requires one approved production-equivalent staging environment with an immutable, independently observable deployment identity before later external validation can be credited.

Authoritative intake record: [`docs/staging/PHASE8_DEPLOYMENT_IDENTITY_RECORD.md`](docs/staging/PHASE8_DEPLOYMENT_IDENTITY_RECORD.md).

Current Phase 8.1 decision: `PENDING_EXTERNAL_DEPLOYMENT_IDENTITY`. The repository's staging-readiness contract, Docker Compose and staging emulators do not prove a real staging deployment.

## Governance mapping model

[`docs/governance/GOVERNANCE_MAPPING_REGISTRY.md`](docs/governance/GOVERNANCE_MAPPING_REGISTRY.md) is authoritative for Governance mapping claims.

- **Normenkader IBP:** `UNMAPPED` — no control-level repository crosswalk exists yet.
- **MITRE ATT&CK:** `UNMAPPED` — no technique-level mapping dataset exists yet.
- **CVSS:** `CONTEXT_ONLY` — canonical ingest has severity/free metadata but no first-class vector/base-score field.
- **DTMO security & release governance:** `MAPPED_INTERNAL` — internal mappings point to explicit repository evidence.

Missing mappings are visible evidence and are never inferred from semantic similarity, tags or free metadata.

## Security and governance model

DTMO preserves RBAC, least privilege, code-controlled roles, strict service-account/human-role separation, administrator safety controls, separate human review and external share approval, provenance, privacy/data minimization, tamper-evident auditability and request correlation. Connectors, CI, dashboards, Administration, Governance or staging access do not grant publication authority.

See [`SECURITY.md`](SECURITY.md) and [`docs/security/SECURITY_OVERVIEW.md`](docs/security/SECURITY_OVERVIEW.md).

## Project status

| Phase | Scope | Status |
|---|---|---|
| 1–7 | Repository-controlled engineering | ✅ `PASS` |
| RC13 | Functional unified-console acceptance | ✅ `PASS` |
| 8 | Real staging acceptance | ▶ `READY_FOR_EXTERNAL_VALIDATION / PENDING_EXTERNAL_DEPLOYMENT_IDENTITY` |
| 9 | Independent external assurance | ⏳ `NOT COMPLETE` |
| 10 | Production go/no-go | ⏳ `NOT STARTED` |

The only current priority is **Phase 8.1 — establish and record the approved production-equivalent staging environment and immutable deployment identity**.

## Documentation

Start with [`docs/README.md`](docs/README.md). Key records include [`docs/project/CURRENT_STATE.md`](docs/project/CURRENT_STATE.md), [`docs/roadmap/PRODUCTION_ROADMAP.md`](docs/roadmap/PRODUCTION_ROADMAP.md), [`docs/qa/RC13_FUNCTIONAL_CONSOLE_ACCEPTANCE_GATE.md`](docs/qa/RC13_FUNCTIONAL_CONSOLE_ACCEPTANCE_GATE.md), [`docs/qa/PHASE8_STAGING_DEPLOYMENT_PARITY_GATE.md`](docs/qa/PHASE8_STAGING_DEPLOYMENT_PARITY_GATE.md), [`docs/staging/PHASE8_DEPLOYMENT_IDENTITY_RECORD.md`](docs/staging/PHASE8_DEPLOYMENT_IDENTITY_RECORD.md), [`docs/governance/GOVERNANCE_MAPPING_REGISTRY.md`](docs/governance/GOVERNANCE_MAPPING_REGISTRY.md) and [`docs/architecture/SYSTEM_ARCHITECTURE.md`](docs/architecture/SYSTEM_ARCHITECTURE.md).

## Open source and responsible use

DTMO is licensed under the **Apache License, Version 2.0** (`Apache-2.0`). Repository governance entry points are `LICENSE`, `NOTICE`, `SECURITY.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SUPPORTED_VERSIONS.md`, `docs/legal/LICENSING.md` and `docs/legal/THIRD_PARTY.md`.

Use DTMO only with lawful access to intelligence sources and infrastructure. A technically successful connector does not itself establish legal permission to collect, process or redistribute third-party material.
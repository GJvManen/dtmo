# DTMO

## Dutch Threat Monitoring for Education

**DTMO** is an open Cyber Threat Intelligence platform for the education sector. It combines vulnerability intelligence, vendor advisories, provenance, operational health, investigation and governance in one controlled platform.

**Release candidate:** `16.0.0rc12`  
**Engineering status:** Phases 1–7 and repository-controlled RC13.1–RC13.5 accepted  
**RC13 product status:** `AWAITING_OWNER_RETEST`  
**External staging:** `PAUSED_PENDING_RC13_OWNER_RETEST`  
**License:** Apache-2.0

> **Current release decision:** DTMO is not production ready and is not yet ready for external staging/pentest acceptance. The repository-controlled full canonical-console journey passed exact-head CI and was merged in PR #155. The only remaining RC13 acceptance action is an accountable project-owner functional retest of the repaired local product.

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

Project-owner testing on 2026-08-11 showed that earlier component-level CI did not prove a usable product journey. RC13 therefore repaired and re-proved the canonical console before Phase 8.

1. **RC13.1 — source-to-intelligence — PASS.** PR #151 merged as `95c4a5b072d141f50a02d23f8bf9abb862d6f8e2`.
2. **RC13.2 — single-session visual analytics — PASS.** PR #152 merged as `b8c254c5d099cde5dca624aa85b17c320594847e`.
3. **RC13.3 — Administration/RBAC — PASS.** PR #153 merged as `2e1029a43f7b44d8525fb89197d0a10458a3e992`.
4. **RC13.4 — Governance knowledge — PASS.** PR #154 merged as `21672aaf1cf097228699810660eaac167da842d6`.
5. **RC13.5 — full integrated canonical-console browser acceptance — PASS within the repository-controlled evidence boundary.** PR #155 merged as `d6f83557ab18d26f82ad6289b1b95f728346631d` after exact head `56805ec4ead5a14e9a2f776f84df42eb772302a4` completed the full returned workflow matrix successfully, including RC4 Quality Gate #815 and RC13 Full Functional Console Acceptance Gate #1.

The RC13.5 Chromium journey covered:

**Overview → Intelligence → Sources & Catalog → register/enable/run → Intelligence update → Visual analytics → Administration → Governance → Overview state confirmation.**

RC13.5 CI is synthetic repository-controlled evidence. It does **not** manufacture project-owner acceptance. The owner must still functionally retest the repaired local product and explicitly accept or report remaining blockers.

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
| RC13 | Functional unified-console acceptance | ⏳ `AWAITING_OWNER_RETEST` — RC13.1–RC13.5 repository evidence complete |
| 8 | Real staging acceptance | ⏸ `PAUSED_PENDING_RC13_OWNER_RETEST` |
| 9 | Independent external assurance | ⏳ `NOT COMPLETE` |
| 10 | Production go/no-go | ⏳ `NOT STARTED` |

The only current priority is **accountable project-owner functional retest of the repaired canonical console**. If accepted, RC13 may close and Phase 8 can return to external-validation readiness. If a blocker remains, that finding becomes the next repair priority.

## Documentation

Start with [`docs/README.md`](docs/README.md). Key records include [`docs/project/CURRENT_STATE.md`](docs/project/CURRENT_STATE.md), [`docs/roadmap/PRODUCTION_ROADMAP.md`](docs/roadmap/PRODUCTION_ROADMAP.md), [`docs/qa/RC13_FUNCTIONAL_CONSOLE_ACCEPTANCE_GATE.md`](docs/qa/RC13_FUNCTIONAL_CONSOLE_ACCEPTANCE_GATE.md), [`docs/qa/PHASE8_STAGING_DEPLOYMENT_PARITY_GATE.md`](docs/qa/PHASE8_STAGING_DEPLOYMENT_PARITY_GATE.md), [`docs/governance/GOVERNANCE_MAPPING_REGISTRY.md`](docs/governance/GOVERNANCE_MAPPING_REGISTRY.md) and [`docs/architecture/SYSTEM_ARCHITECTURE.md`](docs/architecture/SYSTEM_ARCHITECTURE.md).

## Open source and responsible use

DTMO is licensed under the **Apache License, Version 2.0** (`Apache-2.0`). Repository governance entry points are `LICENSE`, `NOTICE`, `SECURITY.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SUPPORTED_VERSIONS.md`, `docs/legal/LICENSING.md` and `docs/legal/THIRD_PARTY.md`.

Use DTMO only with lawful access to intelligence sources and infrastructure. A technically successful connector does not itself establish legal permission to collect, process or redistribute third-party material.

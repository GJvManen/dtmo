# DTMO

## Dutch Threat Monitoring for Education

**DTMO** is an open Cyber Threat Intelligence platform for the education sector. It combines vulnerability intelligence, vendor advisories, provenance, operational health, investigation and governance in one controlled platform.

**Release candidate:** `16.0.0rc12`  
**Engineering status:** Phases 1–7 accepted  
**RC13 product status:** `AWAITING_OWNER_RETEST_AFTER_REPAIR`  
**External staging:** `PAUSED_PENDING_RC13_OWNER_RETEST`  
**License:** Apache-2.0

> **Current release decision:** DTMO is not production ready. Repository-controlled RC13 repairs through PR #165 are complete and exact-head green. The next gate is accountable owner functional retesting on current merged `main`; repository CI does not manufacture that acceptance.

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

The current bounded repair sequence is repository-green:

1. **PR #159 — console usability repair** — merged as `b4fffecc47f87b1edab8258514eaa130d949c195`;
2. **PR #160 — Compose runtime packaging repair** — merged as `dc6f8c6a2d3ea3e7efc8c45460caea607aa63d9c`;
3. **PR #161 — Grafana datasource provisioning repair** — merged as `79037f82d0e6f42fa1cf57457b02f3aeaaa92bd5`;
4. **PR #163 — source catalog secret-reference/bootstrap repair** — exact head `4198f06e360929d3937065b8528237741cbe189a`, complete returned workflow matrix `completed/success`, merged as `adc027143f1274c604a16446fe1ad2bdc7bc835f`, later owner-observed bootstrap `200 OK`;
5. **PR #165 — local object-store credential contract repair** — exact head `48688977836cf3305b9d90c064e945de00eefb49`, complete returned workflow matrix `completed/success`, merged with expected-head protection as `65440afea6cfa3c3300b25d577d746432cc95700`.

PR #165 aligns only the local-development API object-store identity with local AIStor startup credentials. The staging/production-equivalent model continues to require a distinct least-privilege `AISTOR_APP_ACCESS_KEY/AISTOR_APP_SECRET_KEY` application identity.

## Owner-retest boundary

The accountable owner must now retest current merged `main` and verify the real source-to-intelligence and console path, including:

- local Compose startup and Grafana health;
- supported source-catalog bootstrap remains successful and idempotent;
- bootstrapped sources remain disabled by default until explicitly enabled;
- a supported source can fetch and persist raw evidence without object-store authentication failure;
- successful ingestion appears truthfully in Intelligence, Overview and analytics;
- `Alles vernieuwen`, empty-data states, Chrome controls and Administration behave truthfully;
- authorization/publication boundaries remain unchanged.

Only explicit accountable owner acceptance closes RC13.

## Historical RC13 evidence

RC13.1–RC13.5 and earlier owner acceptance remain historical evidence. Subsequent owner testing controls the current decision; historical records are not rewritten.

## Phase 8 — paused

PR #157 and the fail-closed external deployment identity record remain preparatory evidence. Issue #158 remains paused until RC13 is explicitly accepted.

After owner acceptance, Phase 8 may return to `READY_FOR_EXTERNAL_VALIDATION / PENDING_EXTERNAL_DEPLOYMENT_IDENTITY`. Repository CI, Docker Compose and staging emulators cannot substitute for real staging evidence.

## Governance mapping model

[`docs/governance/GOVERNANCE_MAPPING_REGISTRY.md`](docs/governance/GOVERNANCE_MAPPING_REGISTRY.md) remains authoritative:

- **Normenkader IBP:** `UNMAPPED`;
- **MITRE ATT&CK:** `UNMAPPED`;
- **CVSS:** `CONTEXT_ONLY`;
- **DTMO security & release governance:** `MAPPED_INTERNAL`.

Missing mappings are visible evidence and are never inferred.

## Security and governance model

DTMO preserves RBAC, least privilege, code-controlled roles, strict service-account/human-role separation, administrator safety controls, separate human review and external share approval, provenance, privacy/data minimization, tamper-evident auditability and request correlation. Credentialed integrations store logical secret references only; raw secret values remain forbidden. Local-development object-store credential reuse does not alter staging/production least-privilege requirements. Connectors, CI, dashboards, Administration, Governance or staging access do not grant publication authority.

## Project status

| Phase | Scope | Status |
|---|---|---|
| 1–7 | Repository-controlled engineering | ✅ `PASS` |
| RC13 | Functional unified-console acceptance | ⏳ `AWAITING_OWNER_RETEST_AFTER_REPAIR` |
| 8 | Real staging acceptance | ⏸ `PAUSED_PENDING_RC13_OWNER_RETEST` |
| 9 | Independent external assurance | ⏳ `NOT COMPLETE` |
| 10 | Production go/no-go | ⏳ `NOT STARTED` |

The only current product priority is **issue #150 — accountable owner RC13 functional retesting on current merged `main` containing PR #165**.

## Documentation

Start with [`docs/README.md`](docs/README.md). Current authoritative records include [`docs/project/CURRENT_STATE.md`](docs/project/CURRENT_STATE.md), [`docs/roadmap/PRODUCTION_ROADMAP.md`](docs/roadmap/PRODUCTION_ROADMAP.md), [`docs/qa/RC13_FUNCTIONAL_CONSOLE_ACCEPTANCE_GATE.md`](docs/qa/RC13_FUNCTIONAL_CONSOLE_ACCEPTANCE_GATE.md) and [`docs/qa/PHASE8_STAGING_DEPLOYMENT_PARITY_GATE.md`](docs/qa/PHASE8_STAGING_DEPLOYMENT_PARITY_GATE.md).

## Open source and responsible use

DTMO is licensed under the **Apache License, Version 2.0** (`Apache-2.0`). The repository governance entry points are `SECURITY.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SUPPORTED_VERSIONS.md`, `docs/legal/LICENSING.md` and `docs/legal/THIRD_PARTY.md`; canonical licence/notice files are `LICENSE` and `NOTICE`.

Use DTMO only with lawful access to intelligence sources and infrastructure. A technically successful connector does not itself establish legal permission to collect, process or redistribute third-party material.

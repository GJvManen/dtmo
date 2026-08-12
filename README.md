# DTMO

## Dutch Threat Monitoring for Education

**DTMO** is an open Cyber Threat Intelligence platform for the education sector. It combines vulnerability intelligence, vendor advisories, provenance, operational health, investigation and governance in one controlled platform.

**Release candidate:** `16.0.0rc12`  
**Engineering status:** Phases 1–7 accepted  
**RC13 product status:** `REOPENED / BLOCKED_INTERNAL`  
**External staging:** `PAUSED_PENDING_RC13_REPAIR_AND_OWNER_RETEST`  
**License:** Apache-2.0

> **Current release decision:** DTMO is not production ready. PR #163 is repository-green and its catalog-bootstrap repair is now owner-observed functional, but the same fresh-clone owner run exposed a new local source-to-intelligence object-store credential mismatch. RC13 remains open and Phase 8 remains paused until that bounded repository defect is repaired, exact-head green, merged and retested.

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

RC13.1–RC13.5 and the earlier owner acceptance remain historical evidence. Subsequent owner retesting has driven the current bounded repair sequence:

1. **PR #159 — console usability repair** — merged as `b4fffecc47f87b1edab8258514eaa130d949c195`;
2. **PR #160 — Compose runtime packaging repair** — merged as `dc6f8c6a2d3ea3e7efc8c45460caea607aa63d9c`;
3. **PR #161 — Grafana datasource provisioning repair** — merged as `79037f82d0e6f42fa1cf57457b02f3aeaaa92bd5`;
4. **PR #163 — source catalog secret-reference/bootstrap repair** — final exact head `4198f06e360929d3937065b8528237741cbe189a`, every returned workflow `completed/success`, merged with expected-head protection as `adc027143f1274c604a16446fe1ad2bdc7bc835f`.

The latest accountable owner run confirms the repaired startup and catalog path:

- `grafana-db-provision` exits 0;
- Grafana starts without the former duplicate-default datasource restart loop;
- API health is available;
- `POST /api/v1/admin/sources/catalog/bootstrap` returns `200 OK`.

That same fresh-clone run successfully fetched CISA KEV upstream data, then failed while writing raw evidence to the local object store with `InvalidAccessKeyId`. Repository inspection confirms the local development configuration was internally inconsistent: `.env.example` supplied API defaults `dtmo/change-me-now`, while `docker-compose.yml` started AIStor from separate `MINIO_ROOT_USER/MINIO_ROOT_PASSWORD` inputs and provisioned no matching `dtmo` identity.

## Current bounded repair

Branch `rc13/local-objectstore-credential-contract`:

- makes local-development Compose use the same supplied AIStor identity for the API and local AIStor service;
- removes misleading runnable `dtmo/change-me-now` object-store defaults from `.env.example`;
- keeps this credential reuse strictly local-development-only;
- preserves distinct least-privilege `AISTOR_APP_ACCESS_KEY/AISTOR_APP_SECRET_KEY` credentials for the staging-emulator/production-equivalent model;
- adds contract tests and an exact-head rendered-Compose credential gate.

No repository `PASS` is claimed for this new repair until the complete final exact-head workflow matrix is `completed/success`.

## Owner-retest boundary

Owner evidence now confirms the specific PR #163 catalog fix, but complete RC13 acceptance still requires a successful source-to-intelligence flow plus the remaining functional console checks. After the object-store repair merges, the owner retest resumes across source execution, Intelligence, Overview, analytics, Chrome controls and Administration.

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

DTMO preserves RBAC, least privilege, code-controlled roles, strict service-account/human-role separation, administrator safety controls, separate human review and external share approval, provenance, privacy/data minimization, tamper-evident auditability and request correlation. Credentialed integrations store logical secret references only; raw secret values remain forbidden. Local-development credential reuse does not alter staging/production least-privilege requirements. Connectors, CI, dashboards, Administration, Governance or staging access do not grant publication authority.

## Project status

| Phase | Scope | Status |
|---|---|---|
| 1–7 | Repository-controlled engineering | ✅ `PASS` |
| RC13 | Functional unified-console acceptance | ⛔ `REOPENED / BLOCKED_INTERNAL` |
| 8 | Real staging acceptance | ⏸ `PAUSED_PENDING_RC13_REPAIR_AND_OWNER_RETEST` |
| 9 | Independent external assurance | ⏳ `NOT COMPLETE` |
| 10 | Production go/no-go | ⏳ `NOT STARTED` |

The only current priority is **issue #150 — complete the local object-store credential contract repair, require exact-head CI, merge and resume accountable owner RC13 retesting**.

## Documentation

Start with [`docs/README.md`](docs/README.md). Current authoritative records include [`docs/project/CURRENT_STATE.md`](docs/project/CURRENT_STATE.md), [`docs/roadmap/PRODUCTION_ROADMAP.md`](docs/roadmap/PRODUCTION_ROADMAP.md), [`docs/qa/RC13_FUNCTIONAL_CONSOLE_ACCEPTANCE_GATE.md`](docs/qa/RC13_FUNCTIONAL_CONSOLE_ACCEPTANCE_GATE.md) and [`docs/qa/PHASE8_STAGING_DEPLOYMENT_PARITY_GATE.md`](docs/qa/PHASE8_STAGING_DEPLOYMENT_PARITY_GATE.md).

## Open source and responsible use

DTMO is licensed under the **Apache License, Version 2.0** (`Apache-2.0`). The repository governance entry points are `SECURITY.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SUPPORTED_VERSIONS.md`, `docs/legal/LICENSING.md` and `docs/legal/THIRD_PARTY.md`; canonical licence/notice files are `LICENSE` and `NOTICE`.

Use DTMO only with lawful access to intelligence sources and infrastructure. A technically successful connector does not itself establish legal permission to collect, process or redistribute third-party material.

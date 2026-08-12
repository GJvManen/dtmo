# DTMO

## Dutch Threat Monitoring for Education

**DTMO** is an open Cyber Threat Intelligence platform for the education sector. It combines vulnerability intelligence, vendor advisories, provenance, operational health, investigation and governance in one controlled platform.

**Release candidate:** `16.0.0rc12`  
**Engineering status:** Phases 1–7 accepted  
**RC13 product status:** `AWAITING_OWNER_RETEST_AFTER_REPAIR`  
**External staging:** `PAUSED_PENDING_RC13_OWNER_RETEST`  
**License:** Apache-2.0

> **Current release decision:** DTMO is not production ready. Repository-controlled repairs through PR #163 are green and merged. RC13 still requires accountable project-owner functional retesting of current `main`; Phase 8 remains paused until that explicit acceptance.

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

RC13.1–RC13.5 and the earlier owner acceptance remain historical evidence. Later owner retesting drove the bounded repair sequence below:

1. **PR #159 — console usability repair** — merged as `b4fffecc47f87b1edab8258514eaa130d949c195`;
2. **PR #160 — Compose runtime packaging repair** — merged as `dc6f8c6a2d3ea3e7efc8c45460caea607aa63d9c`;
3. **PR #161 — Grafana datasource provisioning repair** — merged as `79037f82d0e6f42fa1cf57457b02f3aeaaa92bd5`;
4. **PR #163 — source catalog secret-reference/bootstrap repair** — final exact head `4198f06e360929d3937065b8528237741cbe189a`; every returned workflow completed successfully; merged with expected-head protection as `adc027143f1274c604a16446fe1ad2bdc7bc835f`.

The latest owner run already progressed beyond the former #160/#161 startup defects. PR #163 now repairs the later catalog-bootstrap HTTP 500 by centralizing logical secret-reference validation, using executable `env:VARIABLE` references, normalizing legacy `env://VARIABLE`, preserving external secret-manager references, rejecting raw secrets and regression-testing complete supported catalog bootstrap for idempotency and disabled-by-default registration.

## Required owner retest

Current merged `main` must still demonstrate that:

- supported source catalog bootstrap succeeds without HTTP 500 and remains idempotent;
- bootstrapped sources remain disabled until explicitly enabled;
- source validation/run controls behave truthfully;
- `Alles vernieuwen` refreshes and returns to an enabled state;
- empty intelligence reports `Geen intelligence data · bronstatus geladen`, not false success;
- Chrome navigation and operator controls work;
- the navigation version number remains absent;
- Administration clearly presents `Gebruikers & rollen` without duplicated source operations;
- empty graphs explicitly report no data;
- after a successful source run with valid local configuration, Intelligence, Overview and analytics update truthfully.

The earlier MinIO credential symptom is not classified as a repository defect because the owner explicitly identified the local `.env` as incorrect and asked to skip that point.

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

DTMO preserves RBAC, least privilege, code-controlled roles, strict service-account/human-role separation, administrator safety controls, separate human review and external share approval, provenance, privacy/data minimization, tamper-evident auditability and request correlation. Credentialed integrations store logical secret references only; raw secret values remain forbidden. Connectors, CI, dashboards, Administration, Governance or staging access do not grant publication authority.

## Project status

| Phase | Scope | Status |
|---|---|---|
| 1–7 | Repository-controlled engineering | ✅ `PASS` |
| RC13 | Functional unified-console acceptance | ⏳ `AWAITING_OWNER_RETEST_AFTER_REPAIR` |
| 8 | Real staging acceptance | ⏸ `PAUSED_PENDING_RC13_OWNER_RETEST` |
| 9 | Independent external assurance | ⏳ `NOT COMPLETE` |
| 10 | Production go/no-go | ⏳ `NOT STARTED` |

The only current priority is **issue #150 — accountable project-owner local Compose and functional console retest of current merged `main`**.

## Documentation

Start with [`docs/README.md`](docs/README.md). Current authoritative records include [`docs/project/CURRENT_STATE.md`](docs/project/CURRENT_STATE.md), [`docs/roadmap/PRODUCTION_ROADMAP.md`](docs/roadmap/PRODUCTION_ROADMAP.md), [`docs/qa/RC13_FUNCTIONAL_CONSOLE_ACCEPTANCE_GATE.md`](docs/qa/RC13_FUNCTIONAL_CONSOLE_ACCEPTANCE_GATE.md) and [`docs/qa/PHASE8_STAGING_DEPLOYMENT_PARITY_GATE.md`](docs/qa/PHASE8_STAGING_DEPLOYMENT_PARITY_GATE.md).

## Open source and responsible use

DTMO is licensed under the **Apache License, Version 2.0** (`Apache-2.0`). The repository governance entry points are `SECURITY.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SUPPORTED_VERSIONS.md`, `docs/legal/LICENSING.md` and `docs/legal/THIRD_PARTY.md`; canonical licence/notice files are `LICENSE` and `NOTICE`.

Use DTMO only with lawful access to intelligence sources and infrastructure. A technically successful connector does not itself establish legal permission to collect, process or redistribute third-party material.

# DTMO

## Dutch Threat Monitoring for Education

**DTMO** is an open Cyber Threat Intelligence platform for the education sector. It combines vulnerability intelligence, vendor advisories, provenance, operational health, investigation and governance in one controlled platform.

**Release candidate:** `16.0.0rc12`  
**Engineering status:** Phases 1–7 accepted  
**RC13 product status:** `REOPENED / BLOCKED_INTERNAL`  
**External staging:** `PAUSED_PENDING_RC13_REPAIR_AND_OWNER_RETEST`  
**License:** Apache-2.0

> **Current release decision:** DTMO is not production ready. PR #165 is repository-green and repaired the local object-store credential contract. The subsequent accountable owner retest shows that source loading can appear successful while ingested intelligence remains invisible in the canonical console, leaving Intelligence, metrics and graphics empty. Repository inspection identified a connector transaction-boundary defect that can skip the canonical PostgreSQL commit.

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

RC13.1–RC13.5 and earlier owner acceptance remain historical evidence. Subsequent owner retesting controls the current decision.

Completed bounded repairs:

1. **PR #159 — console usability repair** — merged as `b4fffecc47f87b1edab8258514eaa130d949c195`;
2. **PR #160 — Compose runtime packaging repair** — merged as `dc6f8c6a2d3ea3e7efc8c45460caea607aa63d9c`;
3. **PR #161 — Grafana datasource provisioning repair** — merged as `79037f82d0e6f42fa1cf57457b02f3aeaaa92bd5`;
4. **PR #163 — source catalog secret-reference/bootstrap repair** — exact-head green, merged as `adc027143f1274c604a16446fe1ad2bdc7bc835f`, later owner-observed bootstrap `200 OK`;
5. **PR #165 — local object-store credential contract repair** — exact head `48688977836cf3305b9d90c064e945de00eefb49`, complete returned workflow matrix `completed/success`, merged with expected-head protection as `65440afea6cfa3c3300b25d577d746432cc95700`.

## Current blocker — canonical connector commit visibility

The latest owner retest reports that loading sources appears to work, but the ingested intelligence does not become visible in the interface. As a consequence the Intelligence view, Overview KPIs, metrics and native graphics remain empty.

Repository inspection confirms the canonical console and dashboards read `IntelligenceItem` from PostgreSQL. The built-in connector path calls `ingest_connector_record()`, which previously returned from inside:

```python
async for session in database.session():
    return await _persist_intelligence(...)
```

`Database.session()` performs `commit()` only after its `yield`. Returning from the loop body prevents the async generator from resuming through that post-yield commit path. The connector can therefore finish raw landing/indexing and report inserted/indexed work without a durable canonical PostgreSQL row becoming visible to the console/dashboard read model.

The bounded repair branch `rc13/canonical-connector-commit-visibility` now:

- retains the persistence receipt while the session generator runs to completion;
- returns connector success only after the canonical session commit has completed;
- propagates commit failure instead of reporting success;
- adds regression tests that fail on the former early-return behavior;
- adds an exact-head `RC13 Canonical Connector Commit Visibility Gate` covering the commit boundary, connector ingestion contract, canonical console read contract and graphical dashboard contract.

The repair is `PENDING_CI`. No repository PASS is claimed until every returned workflow on its final exact head is `completed/success`.

## Owner-retest boundary

After the repair is exact-head green and merged, the accountable owner must verify on current `main` that a real supported source run:

1. fetches the upstream source;
2. persists raw evidence without object-store authentication failure;
3. commits canonical intelligence to PostgreSQL;
4. becomes visible in **Intelligence** and **Recent intelligence**;
5. updates Overview KPIs and source/severity/trend metrics;
6. updates native Visual Analytics truthfully;
7. preserves truthful refresh/error/empty states and the existing authorization/publication boundaries.

Only explicit accountable owner acceptance closes RC13.

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

The only current priority is **issue #150 — complete the canonical connector commit/console-visibility repair, require full exact-head CI, merge, then resume accountable owner RC13 retesting**.

## Documentation

Start with [`docs/README.md`](docs/README.md). Current authoritative records include [`docs/project/CURRENT_STATE.md`](docs/project/CURRENT_STATE.md), [`docs/roadmap/PRODUCTION_ROADMAP.md`](docs/roadmap/PRODUCTION_ROADMAP.md), [`docs/qa/RC13_FUNCTIONAL_CONSOLE_ACCEPTANCE_GATE.md`](docs/qa/RC13_FUNCTIONAL_CONSOLE_ACCEPTANCE_GATE.md) and [`docs/qa/PHASE8_STAGING_DEPLOYMENT_PARITY_GATE.md`](docs/qa/PHASE8_STAGING_DEPLOYMENT_PARITY_GATE.md).

## Open source and responsible use

DTMO is licensed under the **Apache License, Version 2.0** (`Apache-2.0`). The repository governance entry points are `SECURITY.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SUPPORTED_VERSIONS.md`, `docs/legal/LICENSING.md` and `docs/legal/THIRD_PARTY.md`; canonical licence/notice files are `LICENSE` and `NOTICE`.

Use DTMO only with lawful access to intelligence sources and infrastructure. A technically successful connector does not itself establish legal permission to collect, process or redistribute third-party material.

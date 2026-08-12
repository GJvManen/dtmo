# DTMO

## Dutch Threat Monitoring for Education

**DTMO** is an open Cyber Threat Intelligence platform for the education sector. It combines vulnerability intelligence, vendor advisories, provenance, operational health, investigation and governance in one controlled platform.

**Release candidate:** `16.0.0rc12`  
**Engineering status:** Phases 1–7 accepted  
**RC13 product status:** `REOPENED / BLOCKED_INTERNAL`  
**External staging:** `PAUSED_PENDING_RC13_REPAIR_AND_OWNER_RETEST`  
**License:** Apache-2.0

> **Current release decision:** DTMO is not production ready. PR #167 is repository-controlled PASS and repaired the canonical connector commit boundary. The subsequent accountable owner retest shows the ingestion path now progresses further, including successful OpenSearch document writes, but supported-source records can still fail canonical validation before durable PostgreSQL visibility.

## Product scope

DTMO provides unified threat intelligence, governed source operations, threat investigation, native visual analytics, governed Administration/RBAC, governance knowledge and auditable separation between ingestion, review and external share approval.

## RC13 current state

Completed bounded repairs include:

1. PR #159 — console usability;
2. PR #160 — Compose runtime packaging;
3. PR #161 — Grafana datasource provisioning;
4. PR #163 — source catalog secret-reference/bootstrap contract;
5. PR #165 — local object-store credential contract;
6. PR #167 — canonical connector commit/console visibility, exact head `bf18ef2c499edcf8399d1f91b80190937538fdce`, complete returned workflow matrix `completed/success`, merged as `e9a0926f9e13b603be759a7d7036058685ebc3cc`.

The latest owner retest confirms healthy local startup, source/admin/read endpoints returning 200 and multiple OpenSearch `201 Created` document writes. It also exposes two new normalization blockers:

- **NVD canonical URL:** an NVD CVE can contain a first upstream reference using `ftp://`. The canonical ingest schema intentionally accepts only HTTP(S), so using that external reference as `canonical_url`/provenance causes validation failure. The repair keeps the stable NVD HTTPS CVE detail URL as canonical/provenance URL while preserving all upstream references in raw evidence.
- **Advisory item type:** supported source adapters can emit `security-advisory`, while canonical `IntelligenceType` uses `advisory`. The repair normalizes this explicit supported alias at the canonical connector boundary and rejects unknown types fail-closed.

PR #168 was closed without merge because this newer owner evidence superseded its post-#167 documentation reconciliation. Branch-only RUN-205 is not authoritative.

## Owner-retest boundary

After the normalization repair is exact-head green and merged, the accountable owner must verify on current `main` that:

1. NVD executes without failing on non-HTTP upstream references;
2. supported advisory sources execute without enum/statement errors;
3. raw evidence persists;
4. canonical PostgreSQL intelligence is durably committed;
5. Intelligence/Recent intelligence shows the ingested records;
6. Overview KPIs and dashboard metrics update;
7. severity/source/trend/review graphics render from those records;
8. refresh, Chrome controls, Administration and truthful empty states remain correct;
9. authorization, review and separate external-share approval boundaries remain unchanged.

Only explicit accountable owner acceptance closes RC13.

## Phase 8 — paused

Issue #158 remains paused. After explicit owner acceptance, Phase 8 may return to `READY_FOR_EXTERNAL_VALIDATION / PENDING_EXTERNAL_DEPLOYMENT_IDENTITY`. Repository CI, Docker Compose and staging emulators cannot substitute for real staging evidence.

## Governance mapping model

[`docs/governance/GOVERNANCE_MAPPING_REGISTRY.md`](docs/governance/GOVERNANCE_MAPPING_REGISTRY.md) remains authoritative. Missing mappings remain visible evidence and are never inferred.

## Security and governance model

DTMO preserves RBAC, least privilege, code-controlled roles, strict service-account/human-role separation, administrator safety controls, separate human review and external share approval, provenance, privacy/data minimization, tamper-evident auditability and request correlation. Credentialed integrations store logical secret references only; raw secret values remain forbidden. Local-development exceptions do not alter staging/production least-privilege requirements. Connectors, CI, dashboards, Administration, Governance or staging access do not grant publication authority.

## Project status

| Phase | Scope | Status |
|---|---|---|
| 1–7 | Repository-controlled engineering | ✅ `PASS` |
| RC13 | Functional unified-console acceptance | ⛔ `REOPENED / BLOCKED_INTERNAL` |
| 8 | Real staging acceptance | ⏸ `PAUSED_PENDING_RC13_REPAIR_AND_OWNER_RETEST` |
| 9 | Independent external assurance | ⏳ `NOT COMPLETE` |
| 10 | Production go/no-go | ⏳ `NOT STARTED` |

The only current priority is **complete the supported-source normalization repair with complete exact-head CI, merge, then resume accountable owner RC13 retesting**.

## Documentation

Start with [`docs/README.md`](docs/README.md). Current authoritative status records are [`docs/project/CURRENT_STATE.md`](docs/project/CURRENT_STATE.md), [`docs/roadmap/PRODUCTION_ROADMAP.md`](docs/roadmap/PRODUCTION_ROADMAP.md) and [`docs/development/RUN_LOG.md`](docs/development/RUN_LOG.md).

## Open source and responsible use

DTMO is licensed under Apache-2.0. Use DTMO only with lawful access to intelligence sources and infrastructure. A technically successful connector does not itself establish legal permission to collect, process or redistribute third-party material.

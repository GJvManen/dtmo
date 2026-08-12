# DTMO

## Dutch Threat Monitoring for Education

**DTMO** is an open Cyber Threat Intelligence platform for the education sector. It combines vulnerability intelligence, vendor advisories, provenance, operational health, investigation and governance in one controlled platform.

**Release candidate:** `16.0.0rc12`  
**Engineering status:** Phases 1–7 accepted  
**RC13 product status:** `PASS / OWNER_ACCEPTED`  
**External staging:** `READY_FOR_EXTERNAL_VALIDATION / PENDING_EXTERNAL_DEPLOYMENT_IDENTITY`  
**License:** Apache-2.0

> **Current release decision:** the accountable owner explicitly accepted the repaired unified console on 2026-08-12 with “Het project werkt! Gefelciteerd!”. RC13 is complete. DTMO is still **not production ready** because real Phase 8 staging acceptance, Phase 9 independent assurance and Phase 10 formal production go/no-go remain incomplete.

## Product scope

DTMO provides unified threat intelligence, governed source operations, threat investigation, native visual analytics, governed Administration/RBAC, governance knowledge and auditable separation between ingestion, review and external share approval.

## RC13 accepted repair sequence

1. PR #159 — console usability;
2. PR #160 — Compose runtime packaging;
3. PR #161 — Grafana datasource provisioning;
4. PR #163 — source catalog secret-reference/bootstrap contract;
5. PR #165 — local object-store credential contract;
6. PR #167 — canonical connector commit/console visibility;
7. PR #169 — supported-source normalization, final exact head `53aaa670c75a2f404337620bcf1a8df172efe583`, every returned workflow `completed/success`, merged as `4d182879d851cd22d22ff4f0bab795ed49ee0c1b`;
8. accountable owner functional retest — accepted on 2026-08-12.

Issue #150 is closed `completed`.

## Phase 8 — ready for real external validation

Issue #158 is now the single active production-readiness priority. Phase 8 requires a real approved production-equivalent staging environment, immutable deployment identity, approved least-privilege application credentials, environment/configuration evidence and accountable external validation. Repository CI, Docker Compose, staging emulators and synthetic browser fixtures cannot substitute for real staging evidence.

The staging application identity must remain distinct from AIStor root/admin credentials. The local-development credential compatibility exception must not be propagated into staging.

## Post-RC13 product enhancement backlog

Issue #171 tracks the accountable owner's follow-up recommendations without reopening RC13:

- richer accessible severity colour semantics and informational/low/medium/high filtering in Overview, Intelligence and Visual Analytics;
- governed manual source onboarding in Sources & Catalog;
- trend analysis and later framework-backed analytical aggregation;
- first-class, provenance-backed framework mappings;
- deeper Administration role/permission management;
- deeper framework-oriented Governance coverage and evidence views.

Framework mappings remain truthful: missing mappings stay visibly `UNMAPPED`/`CONTEXT_ONLY` until explicit evidence-backed mappings exist.

## Governance mapping model

[`docs/governance/GOVERNANCE_MAPPING_REGISTRY.md`](docs/governance/GOVERNANCE_MAPPING_REGISTRY.md) remains authoritative until first-class mapping data is implemented. Missing mappings remain visible evidence and are never inferred.

## Security and governance model

DTMO preserves RBAC, least privilege, code-controlled roles, strict service-account/human-role separation, administrator safety controls, separate human review and external share approval, provenance, privacy/data minimization, tamper-evident auditability and request correlation. Credentialed integrations store logical secret references only; raw secret values remain forbidden. Connectors, CI, dashboards, Administration, Governance or staging access do not grant publication authority.

## Project status

| Phase | Scope | Status |
|---|---|---|
| 1–7 | Repository-controlled engineering | ✅ `PASS` |
| RC13 | Functional unified-console acceptance | ✅ `PASS / OWNER_ACCEPTED` |
| 8 | Real staging acceptance | ▶ `READY_FOR_EXTERNAL_VALIDATION / PENDING_EXTERNAL_DEPLOYMENT_IDENTITY` |
| 9 | Independent external assurance | ⏳ `NOT COMPLETE` |
| 10 | Production go/no-go | ⏳ `NOT STARTED` |

The current production-readiness priority is **Phase 8.1 real staging and immutable deployment identity under issue #158**. Product enhancements are tracked separately in issue #171.

## Documentation

Start with [`docs/README.md`](docs/README.md). Current authoritative status records are [`docs/project/CURRENT_STATE.md`](docs/project/CURRENT_STATE.md), [`docs/roadmap/PRODUCTION_ROADMAP.md`](docs/roadmap/PRODUCTION_ROADMAP.md) and [`docs/development/RUN_LOG.md`](docs/development/RUN_LOG.md).

## Open source and responsible use

DTMO is licensed under the **Apache License, Version 2.0**. The canonical licence text is in `LICENSE`; applicable notices are maintained in `NOTICE`.

Open-source governance and security entry points are:

- `SECURITY.md` — security policy and vulnerability reporting;
- `CONTRIBUTING.md` — contribution requirements;
- `CODE_OF_CONDUCT.md` — contributor conduct;
- `SUPPORTED_VERSIONS.md` — supported release policy;
- `docs/legal/LICENSING.md` — DTMO licensing policy;
- `docs/legal/THIRD_PARTY.md` — third-party material, source terms and redistribution boundaries.

Use DTMO only with lawful access to intelligence sources and infrastructure. A technically successful connector does not itself establish legal permission to collect, process or redistribute third-party material.

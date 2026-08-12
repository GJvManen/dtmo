# DTMO

## Dutch Threat Monitoring for Education

**DTMO** is an open Cyber Threat Intelligence platform for the education sector. It combines vulnerability intelligence, vendor advisories, provenance, operational health, investigation and governance in one controlled platform.

**Release candidate:** `16.0.0rc12`  
**Engineering status:** Phases 1–7 accepted  
**RC13 product status:** `AWAITING_OWNER_RETEST_AFTER_REPAIR`  
**External staging:** `PAUSED_PENDING_RC13_OWNER_RETEST`  
**License:** Apache-2.0

> **Current release decision:** DTMO is not production ready. PR #169 is repository-controlled PASS and merged. Accountable owner retesting of the repaired source-to-interface path is now the only RC13 priority.

## Product scope

DTMO provides unified threat intelligence, governed source operations, threat investigation, native visual analytics, governed Administration/RBAC, governance knowledge and auditable separation between ingestion, review and external share approval.

## RC13 current state

Completed bounded repairs include:

1. PR #159 — console usability;
2. PR #160 — Compose runtime packaging;
3. PR #161 — Grafana datasource provisioning;
4. PR #163 — source catalog secret-reference/bootstrap contract;
5. PR #165 — local object-store credential contract; merged `65440afea6cfa3c3300b25d577d746432cc95700`;
6. PR #167 — canonical connector commit/console visibility; merged `e9a0926f9e13b603be759a7d7036058685ebc3cc`;
7. PR #169 — supported-source normalization; final exact head `53aaa670c75a2f404337620bcf1a8df172efe583`, every returned workflow `completed/success`, merged as `4d182879d851cd22d22ff4f0bab795ed49ee0c1b`.

PR #169 preserves the HTTP(S)-only canonical URL boundary, uses stable NVD HTTPS CVE detail URLs for canonical/provenance, retains upstream references in raw evidence, maps only `security-advisory` to canonical `advisory`, rejects unknown item types fail-closed and preserves PR #167 commit-before-success behavior.

The first #169 CI pass exposed a README-only governance regression. Commit `53aaa670c75a2f404337620bcf1a8df172efe583` restored the required Apache/governance entry points; the complete final exact-head workflow matrix then passed.

After merge, connector status handling created three extra commits on `main`, including an immediately restored README write. Compare `4d182879d851cd22d22ff4f0bab795ed49ee0c1b` -> `1fd006b8568a53c1171b9d127d50037ad0027568` returns `files: []`, so the current repository tree is identical to the #169 merge.

RUN-206 remains immutable. PR #168 stayed closed unmerged and branch-only RUN-205 is non-authoritative. RUN-207 records the post-#169 repository acceptance and owner-retest transition.

## Owner-retest boundary

The accountable owner must now verify on current `main` that:

1. NVD executes without failing on non-HTTP upstream references;
2. supported advisory sources execute without enum/statement errors;
3. raw evidence persists;
4. canonical PostgreSQL intelligence is durably committed;
5. Intelligence/Recent intelligence shows ingested records;
6. Overview KPIs and dashboard metrics update;
7. severity/source/trend/review graphics render from those records;
8. `Alles vernieuwen`, Chrome controls, Administration and truthful empty states remain correct;
9. authorization, human review and separate external-share approval boundaries remain unchanged.

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
| RC13 | Functional unified-console acceptance | ⏳ `AWAITING_OWNER_RETEST_AFTER_REPAIR` |
| 8 | Real staging acceptance | ⏸ `PAUSED_PENDING_RC13_OWNER_RETEST` |
| 9 | Independent external assurance | ⏳ `NOT COMPLETE` |
| 10 | Production go/no-go | ⏳ `NOT STARTED` |

The only current priority is **accountable owner retesting of the repaired source-to-interface flow on current `main`**.

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

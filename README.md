# DTMO — Dutch Threat Monitoring for Education

DTMO is an open Cyber Threat Intelligence (CTI) platform for education-sector security teams. It combines governed threat-source operations, canonical intelligence, provenance, vulnerability intelligence, investigation, visual analytics, role-based administration and governance evidence in one controlled application.

> **Software baseline:** `16.0.0rc12` with accepted post-RC13, E8 and Phase 11 repository enhancements  
> **Engineering baseline:** Phases 1–7 `PASS`  
> **Functional acceptance:** RC13 `PASS / OWNER_ACCEPTED`  
> **Product evolution:** E8.1–E8.10 `PASS / REPOSITORY_COMPLETE`  
> **Production-equivalent staging:** Phase 8 `PASS / OWNER_ACCEPTED`  
> **Independent assurance:** Phase 9 `PASS / EXTERNAL_ASSURANCE_ACCEPTED`  
> **Phase 10 production decision:** `NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`  
> **Phase 11.1 Taranis architecture/contract:** `PASS / REPOSITORY_COMPLETE`  
> **Phase 11.2 Taranis adapter:** `PASS / REPOSITORY_COMPLETE`  
> **Phase 11.3 IntelOwl integration:** `PASS / REPOSITORY_COMPLETE`  
> **Phase 11.4 OpenCTI contract:** `PASS / REPOSITORY_COMPLETE`  
> **Phase 11.4 OpenCTI read-only adapter:** `PASS / REPOSITORY_COMPLETE`  
> **Active bounded priority:** Phase 11.4 OpenCTI canonical mapping/persistence + operational integration `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`  
> **Next production authorization:** Phase 12 `NOT STARTED`  
> **Production status:** **not production authorized**

## Why DTMO

Education environments combine broad digital estates, sensitive information, cloud dependencies and a threat landscape ranging from opportunistic exploitation to targeted campaigns. DTMO turns heterogeneous governed intelligence into traceable, reviewable and operationally useful security intelligence while preserving authorization, privacy, provenance and publication controls.

DTMO is built around five principles: provenance first; fail closed; human authority remains human; least privilege by design; and evidence-based governance.

## Product capabilities

The canonical web application provides one operator experience for Overview, Intelligence, Sources & Catalog, Visual Analytics, Administration and Governance. The repository-complete baseline includes governed OpenCVE, CIRCL Vulnerability-Lookup, MISP and AIL semantics plus Phase 11 Taranis collection/canonicalization and IntelOwl enrichment integration.

Phase 11.4 integrates OpenCTI as a separate STIX knowledge-graph service while DTMO remains authoritative for education-sector relevance, local vulnerability/exposure semantics, Governance, review and publication/share authority.

## Phase 11 composed intelligence pipeline

```mermaid
flowchart LR
    S[Approved / governed sources] --> TAR[Taranis AI\ncollection + assessment]
    TAR --> D[(DTMO canonical intelligence)]
    D --> OWL[IntelOwl\nbounded enrichment]
    OWL --> D
    O[OpenCTI\nSTIX 2.1 graph] --> A[Read-only adapter]
    A --> M[(Canonical identity/provenance mapping)]
    M --> D
    M -. never grants .-> H[Human share/publication authority]
    D --> API[FastAPI application services]
    API --> UI[Unified DTMO console]
```

PostgreSQL remains canonical DTMO application truth. IntelOwl results and OpenCTI graph context remain attributable evidence/context; neither becomes proof of local compromise or external-share/publication authority.

## Phase 11.4 OpenCTI canonical persistence

The accepted OpenCTI read adapter performs bounded GraphQL `stixCoreObjects` reads and preserves stable OpenCTI/STIX identities, entity type, markings, confidence, timestamps, external references and provenance. The active slice adds durable PostgreSQL mapping and immutable reconciliation history.

`opencti_object_mappings` stores current DTMO-item ↔ OpenCTI/STIX identity context. `opencti_mapping_revisions` stores immutable SHA-256-keyed snapshots. Unchanged replay is idempotent; changed upstream state creates an attributable revision. Conflicting OpenCTI/STIX identity drift fails closed.

Migration `0012_opencti_mapping_persistence` adds identity uniqueness, confidence validation and database constraints enforcing `external_share_authorized=false` and `local_compromise_proven=false`.

The operational coordinator commits PostgreSQL before calling `commit_page(page)`. Database failure therefore cannot advance the cursor; checkpoint failure after a database commit is safely replayable.

OpenCTI remains a separate service/API boundary. Community Edition is Apache-2.0; Enterprise Edition is separately licensed. No OpenCTI source is vendored. Connector registration, MISP synchronization, external enrichment, TheHive case creation, report publication, security administration and arbitrary GraphQL mutation remain outside Phase 11.4.

See [OpenCTI → DTMO Integration Contract](docs/architecture/OPENCTI_DTMO_INTEGRATION_CONTRACT.md), [OpenCTI Integration](docs/integrations/OPENCTI_INTEGRATION.md) and [OpenCTI Integration Operations Runbook](docs/operations/OPENCTI_INTEGRATION_RUNBOOK.md).

## Architecture

The current DTMO reference platform consists of Python 3.12+, FastAPI/Uvicorn, SQLAlchemy/Alembic, PostgreSQL, Redis, OpenSearch, S3-compatible object storage, Prometheus/Grafana, Nginx and a Docker Compose reference topology. The Phase 11 target is a composed service architecture: Taranis AI for collection/assessment, IntelOwl for IOC enrichment, OpenCTI for STIX graph, MISP for governed exchange and TheHive for incident/case handoff.

## Current maturity and release position

| Stage | Scope | Status |
|---|---|---|
| Phases 1–7 | Repository-controlled engineering baseline | `PASS` |
| RC13 | Unified-console functional acceptance | `PASS / OWNER_ACCEPTED` |
| E8.1–E8.10 | Vulnerability & CTI product evolution | `PASS / REPOSITORY_COMPLETE` |
| Phase 8 | Production-equivalent staging validation | `PASS / OWNER_ACCEPTED` |
| Phase 9 | Independent assurance | `PASS / EXTERNAL_ASSURANCE_ACCEPTED` |
| Phase 10 | Formal production go/no-go | `NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED` |
| Phase 11.1 | Taranis architecture/API/data-model/identity/licensing | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.2 | Taranis→DTMO canonical adapter | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.3 | IntelOwl enrichment integration | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.4 contract | OpenCTI service/API/STIX/identity/security/licensing | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.4 adapter | Read-only GraphQL/STIX identity adapter | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.4 persistence | Canonical mapping/reconciliation/operational integration | `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED` |
| Phase 12 | New formal production go/no-go | `NOT STARTED` |

Historical Phase 8/9 evidence remains bound to the earlier candidate. Fresh Phase 11.10 production-equivalent validation and Phase 11.11 independent external assurance remain required before Phase 12.

## Product roadmap

The fixed sequence is OpenCTI → MISP consolidation → TheHive → conditional Cortex → Kubernetes/Helm/GitOps hardening → migration/compatibility → new validation → new independent assurance → Phase 12.

See the [Platform Industrialisation Roadmap](docs/roadmap/PLATFORM_INDUSTRIALISATION_ROADMAP.md), [Current Project State](docs/project/CURRENT_STATE.md), [QA and Release Gates](docs/qa/QA_AND_RELEASE_GATES.md) and [Evidence Index](docs/evidence/EVIDENCE_INDEX.md).

## Documentation

The authoritative documentation portal is [docs/README.md](docs/README.md). Historical point-in-time records remain historical and are not rewritten to claim later Phase 11 evidence.

## Local reference environment

```bash
git clone https://github.com/GJvManen/dtmo.git
cd dtmo
python3 tools/bootstrap_local.py
docker compose up --build
```

The local Compose topology is a development/reference environment only.

## Open source and responsible use

DTMO is licensed under the **Apache License, Version 2.0**. Canonical governance and legal entry points remain:

- `LICENSE`
- `NOTICE`
- `SECURITY.md`
- `CONTRIBUTING.md`
- `CODE_OF_CONDUCT.md`
- `SUPPORTED_VERSIONS.md`
- `docs/legal/LICENSING.md`
- `docs/legal/THIRD_PARTY.md`

Taranis AI remains a separate service behind its own licensing boundary. IntelOwl and pyIntelOwl remain separate AGPL-3.0 services. OpenCTI Community Edition is Apache-2.0 and OpenCTI Enterprise Edition is separately licensed; Enterprise Edition-only dependencies require explicit entitlement/legal review before acceptance. Phase 11 integrations do not vendor upstream platform source into DTMO.

Use DTMO only with lawful access to intelligence sources and infrastructure. Technical connectivity does not itself establish legal authority to collect, process, enrich, synchronize, publish or redistribute third-party material.

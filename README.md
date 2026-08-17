# DTMO — Dutch Threat Monitoring for Education

DTMO is an open Cyber Threat Intelligence (CTI) platform for education-sector security teams. It combines governed threat-source operations, canonical intelligence, provenance, vulnerability intelligence, investigation, visual analytics, role-based administration and governance evidence in one controlled application.

> **Software baseline:** `16.0.0rc12` with accepted post-RC13, E8 and Phase 11 repository enhancements  
> **Engineering baseline:** Phases 1–7 `PASS`  
> **Functional acceptance:** RC13 `PASS / OWNER_ACCEPTED`  
> **Product evolution:** E8.1–E8.10 `PASS / REPOSITORY_COMPLETE`  
> **Production-equivalent staging:** Phase 8 `PASS / OWNER_ACCEPTED`  
> **Independent assurance:** Phase 9 `PASS / EXTERNAL_ASSURANCE_ACCEPTED`  
> **Phase 10 production decision:** `NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`  
> **Phase 11.3 IntelOwl integration:** `PASS / REPOSITORY_COMPLETE`  
> **Phase 11.4 OpenCTI integration:** `PASS / REPOSITORY_COMPLETE`  
> **Phase 11.5 MISP consolidation:** `PASS / REPOSITORY_COMPLETE`  
> **Phase 11.6 TheHive:** `PASS / REPOSITORY_COMPLETE`  
> **Phase 11.7 Cortex decision:** `PASS / REPOSITORY_COMPLETE — HISTORICAL DECISION BASELINE`  
> **Active bounded priority:** Phase 11.7b Cortex analyzer connector `IN PROGRESS / OWNER-REQUIRED EXACT-HEAD VALIDATION`  
> **Phase 11.8 runtime industrialisation:** `NOT STARTED / BLOCKED BY 11.7b`  
> **Next production authorization:** Phase 12 `NOT STARTED`  
> **Production status:** **not production authorized**

## Why DTMO

Education environments combine broad digital estates, sensitive information, cloud dependencies and a threat landscape ranging from opportunistic exploitation to targeted campaigns. DTMO turns heterogeneous governed intelligence into traceable, reviewable and operationally useful security intelligence while preserving authorization, privacy, provenance and publication controls.

DTMO is built around five principles: provenance first; fail closed; human authority remains human; least privilege by design; and evidence-based governance.

## Product capabilities

The canonical web application provides one operator experience for Overview, Intelligence, Sources & Catalog, Visual Analytics, Administration and Governance. The repository-complete baseline includes governed OpenCVE, CIRCL Vulnerability-Lookup, MISP and AIL semantics plus Phase 11 Taranis AI collection/canonicalization, IntelOwl enrichment, OpenCTI graph integration, governed MISP consolidation and human-authorized TheHive case handoff.

The original Phase 11.7 decision did not adopt Cortex because no validated IntelOwl capability gap existed at that time. On 2026-08-17 the accountable owner added Cortex connector integration as a new attributable requirement. Phase 11.7b now adds a bounded analyzer-only connector without rewriting that historical decision.

## Phase 11 composed intelligence pipeline

```mermaid
flowchart LR
    S[Approved governed sources] --> TAR[Taranis AI\ncollection + assessment]
    TAR --> D[(DTMO canonical intelligence)]
    D --> OWL[IntelOwl\nbounded enrichment]
    OWL --> D
    D --> CTX[Cortex\nowner-required analyzer connector]
    CTX --> D
    O[OpenCTI\nSTIX 2.1 graph] --> D
    M[MISP\ngoverned exchange] <--> D
    D --> H{Human handoff:case authority?}
    H -->|approved| R[(Durable handoff reservation)]
    H -->|not approved| N[No case mutation]
    R --> TH[TheHive API v1\nPOST /api/v1/case]
    D -. authority remains .-> P[Human share/publication approval]
```

PostgreSQL remains canonical DTMO application truth. Taranis AI, IntelOwl, Cortex, OpenCTI, MISP and TheHive are separate service boundaries. None independently establishes local compromise or grants DTMO external-share/publication authority.

## Phase 11.7b Cortex analyzer connector

The bounded connector lives in `backend/dtmo/integrations/cortex.py` and uses the official Cortex REST API. It accepts only explicit non-file observable datatypes and analyzer IDs from configured allowlists, requires an explicit TLP value and uses API-key bearer authentication.

Only `POST /api/analyzer/{ANALYZER_ID}/run` and `GET /api/job/{JOB_ID}/waitreport` are in scope. Stable job identity is mandatory, analyzer identity is checked when returned, result size is bounded and malformed output fails closed. Imported report metadata explicitly sets `external_share_authorized=false` and `local_compromise_proven=false`.

Responders, external side-effect actions, Cortex administration, file/attachment analysis, dynamic analyzer enablement, automatic fallback from IntelOwl and upstream source vendoring are excluded. The feature is disabled by default. Production configuration requires HTTPS, a runtime API key and an explicit analyzer allowlist.

See [Cortex → DTMO Integration Contract](docs/architecture/CORTEX_DTMO_INTEGRATION_CONTRACT.md), [Cortex Analyzer Connector](docs/integrations/CORTEX_ANALYZER_CONNECTOR.md), [Cortex Analyzer Runbook](docs/operations/CORTEX_ANALYZER_RUNBOOK.md) and [Phase 11.7b Cortex Connector Gate](docs/qa/PHASE11_7B_CORTEX_CONNECTOR_GATE.md).

## Architecture

The current DTMO reference platform consists of Python 3.12+, FastAPI/Uvicorn, SQLAlchemy/Alembic, PostgreSQL, Redis, OpenSearch, S3-compatible object storage, Prometheus/Grafana, Nginx and a Docker Compose reference topology. The Phase 11 target is a composed service architecture: Taranis AI for collection/assessment, IntelOwl and bounded Cortex analysis for enrichment, OpenCTI for STIX graph, MISP for governed exchange and TheHive for incident/case handoff.

## Current maturity and release position

| Stage | Scope | Status |
|---|---|---|
| Phases 1–7 | Repository-controlled engineering baseline | `PASS` |
| RC13 | Unified-console functional acceptance | `PASS / OWNER_ACCEPTED` |
| E8.1–E8.10 | Vulnerability & CTI product evolution | `PASS / REPOSITORY_COMPLETE` |
| Phase 8 | Production-equivalent staging validation | `PASS / OWNER_ACCEPTED` |
| Phase 9 | Independent assurance | `PASS / EXTERNAL_ASSURANCE_ACCEPTED` |
| Phase 10 | Formal production go/no-go | `NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED` |
| Phase 11.1–11.2 | Taranis architecture + canonical adapter | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.3 | IntelOwl enrichment integration | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.4 | OpenCTI STIX knowledge-graph integration | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.5 | MISP consolidation and authority state | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.6 | TheHive incident/case handoff | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.7 | Cortex conditional decision | `PASS / REPOSITORY_COMPLETE — HISTORICAL DECISION BASELINE` |
| Phase 11.7b | Owner-required Cortex analyzer connector | `IN PROGRESS / OWNER-REQUIRED EXACT-HEAD VALIDATION` |
| Phase 11.8 | Kubernetes/Helm/GitOps runtime industrialisation | `NOT STARTED / BLOCKED BY 11.7b` |
| Phase 12 | New formal production go/no-go | `NOT STARTED` |

Historical Phase 8/9 evidence remains bound to the earlier candidate. Fresh Phase 11.10 production-equivalent validation and Phase 11.11 independent external assurance remain required before Phase 12.

## Product roadmap

The controlled sequence is accepted TheHive → historical Cortex decision → owner-required bounded Cortex connector → Kubernetes/Helm/GitOps hardening → migration/compatibility → new production-equivalent validation → new independent external assurance → Phase 12.

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

Taranis AI, IntelOwl, Cortex, OpenCTI, MISP and TheHive remain separate services under their applicable licensing and provider boundaries. IntelOwl and MISP remain separate AGPL-3.0 services; OpenCTI Community Edition is Apache-2.0 while Enterprise Edition is separately licensed; TheHive license entitlement is deployment-specific. StrangeBee documents Cortex itself as fully open source and not requiring a Cortex product license, while individual analyzers and external providers can impose separate licensing, subscription or data-handling terms. Phase 11 integrations do not vendor upstream platform source without explicit licensing approval.

Use DTMO only with lawful access to intelligence sources and infrastructure. Technical connectivity does not itself establish legal authority to collect, process, enrich, synchronize, create cases, publish or redistribute third-party material.

# DTMO — Dutch Threat Monitoring for Education

DTMO is an open Cyber Threat Intelligence (CTI) platform for education-sector security teams. It combines governed threat-source operations, canonical intelligence, provenance, vulnerability intelligence, investigation, visual analytics, role-based administration and governance evidence in one controlled application.

> **Software baseline:** `16.0.0rc12` with accepted post-RC13, E8 and Phase 11 repository enhancements  
> **Engineering baseline:** Phases 1–7 `PASS`  
> **Functional acceptance:** RC13 `PASS / OWNER_ACCEPTED`  
> **Product evolution:** E8.1–E8.10 `PASS / REPOSITORY_COMPLETE`  
> **Historical staging evidence:** Phase 8 `PASS / OWNER_ACCEPTED — HISTORICAL CANDIDATE`  
> **Historical independent assurance:** Phase 9 `PASS / EXTERNAL_ASSURANCE_ACCEPTED — HISTORICAL CANDIDATE`  
> **Phase 10 production decision:** `NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`  
> **Phase 11.1–11.9:** `PASS / REPOSITORY_COMPLETE`  
> **Phase 11.10:** `IN PROGRESS / FRESH CANDIDATE-BOUND EVIDENCE REQUIRED`  
> **Phase 11.10a frontend architecture/design:** `PASS / REPOSITORY_COMPLETE`  
> **Phase 11.10b canonical application shell:** `PASS / REPOSITORY_COMPLETE`  
> **Phase 11.10c Command Center:** `PASS / REPOSITORY_COMPLETE`  
> **Phase 11.10d Unified Intelligence Workspace:** `PASS / REPOSITORY_COMPLETE`  
> **Active bounded slice:** Phase 11.10e IntelOwl/Cortex integrated analysis — `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`  
> **Phase 11.10f OpenCTI graph/entity workspace:** `NOT STARTED`  
> **Phase 11.10p fresh production-equivalent validation:** `NOT STARTED / CANDIDATE FREEZE REQUIRED`  
> **Phase 11.11 independent external assurance:** `NOT STARTED`  
> **Phase 12 production decision:** `NOT STARTED`  
> **Production status:** **not production authorized**

## Why DTMO

Education environments combine broad digital estates, sensitive information, cloud dependencies and a threat landscape ranging from opportunistic exploitation to targeted campaigns. DTMO turns heterogeneous governed intelligence into traceable, reviewable and operationally useful security intelligence while preserving authorization, privacy, provenance and publication controls.

DTMO is built around five principles: provenance first; fail closed; human authority remains human; least privilege by design; and evidence-based governance.

## Product capabilities

The accepted DTMO baseline provides **Sources & Catalog**, canonical Intelligence, **Visual Analytics**, vulnerability intelligence, governed case handoff, **Administration** and **Governance**. The accepted Phase 11 integration baseline adds Taranis AI collection/canonicalization, IntelOwl enrichment, OpenCTI STIX knowledge-graph integration, governed MISP exchange, human-authorized TheHive case handoff and a bounded Cortex analyzer connector.

The next-generation interface is the **DTMO Unified Operations Workbench**. Phase 11.10a established the frontend architecture/design contract; Phase 11.10b accepted the React/TypeScript/Vite canonical application shell; Phase 11.10c delivered the functional **Command Center**; Phase 11.10d delivered the functional **Unified Intelligence Workspace** and **IOC Explorer**; Phase 11.10e is now integrating governed **IntelOwl enrichment and Cortex analyzer evidence** in the same shell.

The Command Center exposes accountable canonical intelligence counts, high/critical activity, 24-hour intake, review/share-decision workload, education relevance, recent intelligence, integration capability and role-aware navigation. It does not invent operational state: an unavailable canonical datastore renders unavailable values, and a configured integration is not automatically labelled healthy.

The Unified Intelligence Workspace reuses the governed DTMO search and canonical-detail APIs rather than introducing a parallel intelligence backend. Search is explicit, supports severity and education-relevance filtering, and returns discovery projections. Selecting a result retrieves canonical DTMO object detail and provenance. Failed search/detail dependencies remain unavailable and are not converted into synthetic empty or complete records.

The active Analysis & Enrichment slice preserves the existing IntelOwl execution/history contract and adds a DTMO-governed analyzer-only Cortex execution/history path. Capability state and configured allowlists are visible without being promoted to runtime-health claims. Reads require `read:intelligence`; execution requires server-side `review:intelligence`. Cortex responders, automatic analyzer discovery and automatic IntelOwl fallback remain excluded. Analyzer evidence does **not prove** local compromise and never grants external-share or publication authority.

PostgreSQL remains canonical application truth. Redis, OpenSearch and S3-compatible object storage provide coordination, search and object persistence. Taranis AI, IntelOwl, Cortex, OpenCTI, MISP and TheHive remain separate service/licensing boundaries.

### Accepted Phase 11 service integration baseline

| Integration | Status | Authority boundary |
|---|---|---|
| Phase 11.3 IntelOwl | `PASS / REPOSITORY_COMPLETE` | Enrichment evidence only; no publication/share authority and no local-compromise inference |
| Phase 11.4 OpenCTI | `PASS / REPOSITORY_COMPLETE` | STIX knowledge graph remains a separate service/API/licensing boundary |
| Phase 11.5 MISP | `PASS / REPOSITORY_COMPLETE` | Governed exchange remains subject to DTMO human sharing approval and handling restrictions |
| Phase 11.6 TheHive | `PASS / REPOSITORY_COMPLETE` | Human case-handoff authority remains separate from publication/share authority |
| Phase 11.7 Cortex decision | `PASS / REPOSITORY_COMPLETE — HISTORICAL DECISION BASELINE` | Historical conditional decision remains immutable |
| Phase 11.7b Cortex analyzer connector | `PASS / REPOSITORY_COMPLETE` | Analyzer-only enrichment; responders and autonomous side effects remain excluded |

## Architecture

The canonical product trust path is:

```mermaid
flowchart LR
    B[Browser] --> W[DTMO Unified Operations Workbench]
    W --> A[DTMO API]
    A --> R[Server-side RBAC + audit]
    R --> D[(PostgreSQL canonical intelligence)]
    R --> G[Governed integration adapters]
    G --> S[Taranis / IntelOwl / OpenCTI / MISP / TheHive / Cortex]
    D --> O[OpenSearch / object storage / analytics]
```

Normal frontend operations follow **browser → DTMO API → governed integration adapter → upstream service**. The browser does not receive privileged upstream service credentials. Role-aware rendering is a usability function; **server-side RBAC** remains authoritative.

The Phase 11.8 platform baseline includes Kubernetes/Helm/GitOps, workload identity, **external secret** delivery, **ingress/TLS**, network segmentation, HA/disruption controls, observability, backup/recovery, supply-chain hardening, capacity planning and upgrade/rollback controls. Phase 11.9 adds the accepted connected migration graph and forward-first compatibility contract.

## Current maturity and release position

Phase 10 remains **`NO-GO / BLOCKED`**. Phase 11 is `IN PROGRESS` and DTMO is **not production authorized**.

Phase 11.10 candidate completion is sequenced before fresh external validation because the Unified Operations Workbench materially changes the candidate. The fixed sequence is:

**11.10a architecture/design → 11.10b shell → 11.10c Command Center → 11.10d Intelligence → 11.10e IntelOwl/Cortex → 11.10f OpenCTI → 11.10g MISP → 11.10h TheHive → 11.10i Vulnerability/Exposure → 11.10j Sources/Collection → 11.10k Automation → 11.10l Governance/Evidence → 11.10m Operations/Admin → 11.10n role-aware UX/accessibility → 11.10o consolidation/full functional acceptance → candidate freeze → 11.10p fresh production-equivalent validation**.

Phase 11.10e is the sole active bounded slice. The only permitted next slice after a fully green merge is **11.10f OpenCTI graph/entity workspace**.

### Phase 11.10e evidence boundary

`/workbench/analysis` uses DTMO server APIs for capability visibility, persisted IntelOwl/Cortex history and explicit reviewer-authorized execution. The browser is not a privileged upstream client and never receives IntelOwl/Cortex credentials.

Capability configuration is not runtime-health evidence. IntelOwl and Cortex outputs are enrichment evidence, not verdicts: they do not prove local compromise, approve external sharing, publish intelligence, mutate TheHive cases or authorize production. Cortex remains analyzer-only and responders are outside scope.

Failures **fail closed**. Repository/browser CI validates this implementation contract only. It does **not prove** live upstream availability or analyzer/provider authorization, production-equivalent deployment/continuity, independent assurance or production authorization.

## Product roadmap

Phase 11.10f–11.10o continue the Unified Operations Workbench one bounded PR at a time. After 11.10o, one immutable integrated candidate is frozen for 11.10p.

11.10p requires fresh evidence for candidate identity, migration/compatibility, upgrade, exact prior-digest rollback plus post-rollback health, health/readiness, representative saturation/capacity and recovery/continuity. All evidence must bind to the **same immutable** candidate and one production-equivalent environment. Historical Phase 8 and Phase 9 evidence remains audit history only and cannot satisfy the materially changed candidate.

Missing, inaccessible, historical-only, placeholder or mixed-candidate evidence must **fail closed**. Phase 11.11 remains `NOT STARTED` until 11.10 is explicitly `PASS / OWNER_ACCEPTED`. Phase 12 remains `NOT STARTED` until fresh external assurance has also been accepted.

## Documentation

Start with:

- [Documentation Portal](docs/README.md)
- [Current State](docs/project/CURRENT_STATE.md)
- [Executive Status](docs/project/EXECUTIVE_STATUS.md)
- [Production Readiness Report](docs/project/PRODUCTION_READINESS_REPORT.md)
- [Unified Operations Workbench](docs/ux/UNIFIED_OPERATIONS_WORKBENCH.md)
- [Unified Intelligence Workspace](docs/user/UNIFIED_INTELLIGENCE_WORKSPACE.md)
- [Integrated Analysis Workspace](docs/user/INTEGRATED_ANALYSIS_WORKSPACE.md)
- [Frontend Architecture](docs/architecture/FRONTEND_ARCHITECTURE.md)
- [Phase 11.10d Unified Intelligence Workspace](docs/architecture/PHASE11_10D_UNIFIED_INTELLIGENCE_WORKSPACE.md)
- [Phase 11.10e Integrated Analysis Workspace](docs/architecture/PHASE11_10E_INTEGRATED_ANALYSIS_WORKSPACE.md)
- [Phase 11.10e Integrated Analysis Gate](docs/qa/PHASE11_10E_INTEGRATED_ANALYSIS_GATE.md)
- [Evidence Index](docs/evidence/EVIDENCE_INDEX.md)
- [Platform Industrialisation Roadmap](docs/roadmap/PLATFORM_INDUSTRIALISATION_ROADMAP.md)

The governed screenshot catalogue contains UI-01 through UI-10. These are documentation illustrations, not evidence of live-source connectivity, staging acceptance or production readiness. No synthetic screenshot is promoted as operational, staging, assurance or production evidence.

## Open source and responsible use

DTMO is released under the **Apache License, Version 2.0**. Upstream products retain their own licenses, trademarks, service terms and operational boundaries. DTMO integrations must use authorized credentials and documented APIs and must not be used to bypass provider, organizational, privacy or legal controls.

Governance and contribution entry points are preserved as explicit repository contracts:

- `LICENSE` and `NOTICE` — project licensing and notices;
- `SECURITY.md` — vulnerability reporting and security policy;
- `CONTRIBUTING.md` — contribution requirements;
- `CODE_OF_CONDUCT.md` — community conduct expectations;
- `SUPPORTED_VERSIONS.md` — supported release/security-maintenance scope;
- `docs/legal/LICENSING.md` — DTMO licensing model and boundaries;
- `docs/legal/THIRD_PARTY.md` — third-party licensing and integration boundaries.

DTMO is defensive security software. Publication/share authority remains human-governed, TheHive case authority remains distinct, and enrichment/correlation/graph presence does not prove local compromise.

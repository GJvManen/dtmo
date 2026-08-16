# DTMO Platform Industrialisation Roadmap

Last updated: **2026-08-17**  
Programme state: **`ACTIVE / HIGHEST PRIORITY`**

## Purpose

Phase 10 concluded with `NO-GO / BLOCKED` for production authorization. Phase 11 is the successor industrialisation programme and is executed one bounded pull request at a time. Historical Phase 8/9 evidence remains candidate-bound and is not reused for the materially changed integrated platform.

DTMO prefers mature service integrations over rebuilding generic collection, enrichment, graph, exchange and case-management platforms inside DTMO.

## Strategic target

```mermaid
flowchart LR
    EXT[External OSINT / CERT / vendor sources] --> TAR[Taranis AI\ncollection + assessment]
    TAR --> DTMO[DTMO\neducation CTI + vulnerability context + governance]
    DTMO --> OWL[IntelOwl\nIOC enrichment]
    OWL --> DTMO
    DTMO <--> OCTI[OpenCTI\nSTIX 2.1 knowledge graph]
    DTMO --> MISP[MISP\ngoverned exchange]
    DTMO --> HIVE[TheHive\nincident/case workflow]
```

The target is a composed service architecture, not a source-code merger. Provenance, RBAC, human publication/share authority and fail-closed evidence rules remain explicit across every boundary.

## Fixed priority order

1. 11.1 Taranis AI architecture/API/data-model/identity/licensing assessment.
2. 11.2 Taranis → DTMO canonical adapter.
3. 11.3 IntelOwl enrichment integration.
4. 11.4 OpenCTI STIX knowledge-graph integration.
5. 11.5 MISP consolidation and authoritative governed sharing model.
6. 11.6 TheHive incident/case handoff.
7. 11.7 Cortex only if a validated IntelOwl capability gap exists.
8. 11.8 Kubernetes/Helm/GitOps plus HA/secrets/network/observability/recovery/supply-chain hardening.
9. 11.9 migration/compatibility.
10. 11.10 new production-equivalent validation.
11. 11.11 new independent external assurance.
12. Phase 12 formal production GO/NO-GO.

## Phase 11 — Platform industrialisation

### 11.1 Taranis AI architecture and gap assessment

**Status:** `PASS / REPOSITORY_COMPLETE`

### 11.2 Taranis → DTMO canonical adapter

**Status:** `PASS / REPOSITORY_COMPLETE`

### 11.3 IntelOwl enrichment integration

**Status:** `PASS / REPOSITORY_COMPLETE`

### 11.4 OpenCTI knowledge-graph integration

**Status:** `PASS / REPOSITORY_COMPLETE`

The accepted Phase 11.4 boundary includes the OpenCTI service/API/STIX/licensing contract, bounded read-only GraphQL/STIX adapter, explicit OpenCTI/STIX↔DTMO identity mapping, immutable reconciliation history, database-enforced no-share/no-local-compromise invariants and PostgreSQL-before-checkpoint ordering. Repository acceptance remains engineering evidence only and does not prove live OpenCTI deployment or production authorization.

### 11.5 MISP consolidation

**Status:** `IN PROGRESS / SYNCHRONIZATION STATE IN EXACT-HEAD VALIDATION`

The MISP v2.5.44 service/API/licensing and authority contract is `PASS / REPOSITORY_COMPLETE`. MISP remains a separate AGPL-3.0 service/API boundary.

The active bounded implementation reconciles the existing governed inbound `POST /events/restSearch` and human-approved unpublished `POST /events/add` paths through one durable authority state:

- `misp_synchronization_state` binds one DTMO canonical item to one stable MISP event UUID;
- event UUID, not title or instance-local numeric ID, remains authoritative upstream identity;
- distribution, sharing-group and TLP restrictions are persisted as a source authority envelope;
- the accepted envelope is projected to canonical `metadata_json.misp_restrictions`, reusing the existing governed-export enforcement path;
- conflicting identity mappings, unknown distribution, incomplete sharing-group restrictions or attempts to import share authority fail closed;
- database constraints enforce known distribution semantics, sharing-group requirements and `external_share_authorized=false`;
- migration `0013_misp_synchronization_state` follows the accepted OpenCTI migration;
- human DTMO review/share approval remains the only outbound trigger;
- uncertain outbound delivery continues to block blind replay;
- automatic MISP federation, automatic OpenCTI↔MISP synchronization and event publication remain excluded.

```mermaid
flowchart LR
    M[MISP\nseparate AGPL-3.0 service] -->|events/restSearch| R[Existing governed inbound]
    R --> V{UUID + restrictions valid?}
    V -->|no| X[Fail closed]
    V -->|yes| S[(MISP synchronization state)]
    S --> D[(DTMO canonical item\nauthoritative restrictions)]
    D --> H{Human review + share approval?}
    H -->|no| N[No outbound side effect]
    H -->|yes| P[Existing durable replay reservation]
    P -->|events/add unpublished| M
    M -->|uncertain| U[Block replay; operator reconcile]
```

Repository CI remains engineering evidence only. It does not establish live MISP connectivity, deployed credentials/RBAC, lawful data sharing, remote-server trust, federation behavior, independent assurance or production authorization.

After protected acceptance of this implementation and lifecycle reconciliation, Phase 11.5 may become `PASS / REPOSITORY_COMPLETE`. Phase 11.6 remains blocked until then.

### 11.6 TheHive incident/case handoff

**Status:** `PLANNED / BLOCKED BY 11.5`

### 11.7 Cortex decision gate

**Status:** `PLANNED / CONDITIONAL`

Adopt Cortex only when an accepted IntelOwl capability-gap analysis proves it is needed.

### 11.8 Integrated runtime industrialisation

**Status:** `PLANNED`

Kubernetes, Helm, GitOps, immutable images, workload identities/external secrets, TLS/network policy, HA/recovery, centralized observability, SBOM/scanning/signing/attestation, capacity and upgrade/rollback procedures are required across the composed platform.

### 11.9 Migration and compatibility

**Status:** `PLANNED`

### 11.10 Integrated production-equivalent validation

**Status:** `PLANNED`

Run new production-equivalent validation against one immutable integrated deployment identity. Prior Phase 8 evidence is historical only.

### 11.11 Independent external assurance

**Status:** `PLANNED`

Run fresh independent assurance against the same integrated candidate after 11.10 acceptance.

## Phase 12 — Production GO/NO-GO

**Status:** `NOT STARTED`

A `GO` requires accepted 11.10 and 11.11 evidence for the same immutable integrated release identity plus accountable production ownership, residual-risk, change/support and rollback authority. Missing evidence remains fail-closed.

## Delivery discipline

Every bounded PR requires one primary objective, exact-head CI, expected-head merge protection, professional documentation synchronization, explicit security/licensing/evidence boundaries and one declared next priority. A code/integration PR does not merge when required documentation is missing or stale.

## Immediate sequence

1. Accept the **Phase 11.5 MISP synchronization-state/persistence and authority-enforcement** implementation on fully green exact-head CI.
2. Reconcile Phase 11.5 to `PASS / REPOSITORY_COMPLETE` only after protected merge.
3. Start exactly **11.6 TheHive**.
4. Continue 11.7–11.11 in fixed order and enter Phase 12 only after every required Phase 11 gate is accepted.

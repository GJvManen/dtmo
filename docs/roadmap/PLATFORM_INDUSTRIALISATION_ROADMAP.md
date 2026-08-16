# DTMO Platform Industrialisation Roadmap

Last updated: **2026-08-16**  
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
    MISP <--> OCTI
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

The accepted assessment establishes a service-to-service Taranis boundary. DTMO retains education-sector CTI, vulnerability context, governance, provenance and governed publication/share authority. Taranis source is not vendored into DTMO.

### 11.2 Taranis → DTMO canonical adapter

**Status:** `PASS / REPOSITORY_COMPLETE`

Repository-complete implementation includes read-only collection, stable namespaced identity, fail-closed TLP handling, durable checkpointing/reconciliation, bounded detail/CTI retrieval, governed execution, canonical persistence/indexing and observability.

### 11.3 IntelOwl enrichment integration

**Status:** `PASS / REPOSITORY_COMPLETE`

The contract, bounded adapter and governed execution/persistence boundary are accepted. IntelOwl remains a separate AGPL-3.0 service/API boundary with explicit analyzer allowlists, human review authority, durable enrichment history and no-share/no-local-compromise invariants.

### 11.4 OpenCTI knowledge-graph integration

**Status:** `IN PROGRESS / CANONICAL PERSISTENCE IN EXACT-HEAD VALIDATION`

The OpenCTI service/API/STIX/licensing contract and bounded read-only GraphQL/STIX adapter are `PASS / REPOSITORY_COMPLETE`. The active final Phase 11.4 slice adds canonical mapping persistence, immutable reconciliation history and operational persistence-before-checkpoint ordering.

Active repository scope:

- `opencti_object_mappings` for explicit DTMO-item ↔ OpenCTI internal ID ↔ STIX ID mapping;
- `opencti_mapping_revisions` for immutable SHA-256-keyed reconciliation snapshots;
- preservation of entity type, parent types, markings, confidence, timestamps, external references and provenance;
- unique identity constraints plus fail-closed OpenCTI/STIX identity drift detection;
- database-enforced `external_share_authorized=false` and `local_compromise_proven=false`;
- idempotent unchanged replay and attributable revision creation for changed upstream state;
- migration `0012_opencti_mapping_persistence` after `0011_intelowl_enrichment_history`;
- persistence coordinator that commits PostgreSQL before `commit_page(page)` advances the durable cursor;
- replay safety when checkpoint replacement fails after database commit;
- no connector registration, MISP synchronization, enrichment, case creation, publication, security administration or GraphQL mutation.

```mermaid
flowchart LR
    O[OpenCTI GraphQL] --> A[Accepted read-only adapter]
    A --> V{Identity / markings / provenance valid?}
    V -->|no| X[Fail closed]
    V -->|yes| M[(Canonical OpenCTI mapping)]
    M --> R[(Immutable mapping revisions)]
    M --> D{PostgreSQL commit?}
    D -->|no| X
    D -->|yes| C[(Durable cursor commit)]
    M -. never grants .-> S[Human publication/share authority]
```

Repository CI remains engineering evidence only. It does not prove live OpenCTI connectivity, deployed credentials/RBAC/markings, production-scale graph correctness/performance, privacy approval, HA/recovery, independent assurance or production authorization.

After protected acceptance of this slice and lifecycle reconciliation, **Phase 11.4 may become `PASS / REPOSITORY_COMPLETE`** and the next bounded priority is 11.5 MISP consolidation.

### 11.5 MISP consolidation

**Status:** `PLANNED / BLOCKED BY 11.4`

Consolidate inbound/synchronization and governed outbound exchange into one documented authority model. DTMO human/governed outbound approval remains authoritative.

### 11.6 TheHive incident/case handoff

**Status:** `PLANNED`

Introduce controlled intelligence-to-case handoff with explicit case-creation permission, provenance back to DTMO intelligence and separation between case state and canonical CTI truth.

### 11.7 Cortex decision gate

**Status:** `PLANNED / CONDITIONAL`

Adopt Cortex only when an accepted IntelOwl capability-gap analysis proves it is needed.

### 11.8 Integrated runtime industrialisation

**Status:** `PLANNED`

Kubernetes, Helm, GitOps, immutable images, workload identities/external secrets, TLS/network policy, HA/recovery, centralized observability, SBOM/scanning/signing/attestation, capacity and upgrade/rollback procedures are required across the composed platform.

### 11.9 Migration and compatibility

**Status:** `PLANNED`

Preserve canonical intelligence, provenance, classification, governance and accepted E8 semantics while retiring duplication with explicit rollback paths.

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

1. Accept the **OpenCTI canonical mapping/persistence + operational integration** slice on fully green exact-head CI.
2. Reconcile Phase 11.4 to `PASS / REPOSITORY_COMPLETE` only after protected merge.
3. Start exactly **11.5 MISP consolidation**.
4. Continue 11.6–11.11 in fixed order.
5. Enter Phase 12 only after every required Phase 11 gate is accepted.

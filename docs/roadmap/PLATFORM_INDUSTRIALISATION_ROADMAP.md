# DTMO Platform Industrialisation Roadmap

Last updated: **2026-08-17**  
Programme state: **`ACTIVE / HIGHEST PRIORITY`**

## Purpose

Phase 10 concluded with `NO-GO / BLOCKED` for production authorization. Phase 11 is the successor industrialisation programme and is executed one bounded pull request at a time. Historical Phase 8/9 evidence remains candidate-bound and is not reused for the materially changed integrated platform.

DTMO prefers mature service integrations over rebuilding generic collection, enrichment, graph, exchange and case-management platforms inside DTMO.

## Strategic target

```mermaid
flowchart LR
    EXT[External governed sources] --> TAR[Taranis AI\ncollection + assessment]
    TAR --> DTMO[DTMO\ncanonical education CTI + governance]
    DTMO --> OWL[IntelOwl\nenrichment]
    OWL --> DTMO
    DTMO <--> OCTI[OpenCTI\nSTIX graph]
    DTMO <--> MISP[MISP\ngoverned exchange]
    DTMO --> HIVE[TheHive\nincident/case workflow]
```

Provenance, RBAC, human publication/share authority and fail-closed evidence rules remain explicit across every boundary.

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

### 11.5 MISP consolidation

**Status:** `PASS / REPOSITORY_COMPLETE`

The accepted Phase 11.5 boundary keeps MISP v2.5.44 as a separate AGPL-3.0 service/API, unifies governed `events/restSearch` inbound and human-approved unpublished `events/add` outbound behavior through durable `misp_synchronization_state`, preserves authoritative distribution/sharing-group/TLP restrictions and fails closed on identity/restriction ambiguity or uncertain outbound delivery. Automatic federation, automatic publication and automatic OpenCTI↔MISP synchronization remain excluded.

### 11.6 TheHive incident/case handoff

**Status:** `IN PROGRESS / CONTRACT IN EXACT-HEAD VALIDATION`

The first bounded Phase 11.6 slice is contract-only. It assesses TheHive 5.5.16, API v1, case identity, licensing/entitlement, TLP/PAP/access semantics, least-privilege service identity, human case-handoff authorization and mutation replay safety before any runtime adapter is added.

Contract rules:

- TheHive remains a separate StrangeBee service; no upstream source is vendored;
- API v1 (`/api/v1`) is the supported integration surface and public API v0 is not used;
- TheHive 5.3+ requires an activated Community/Gold/Platinum license for continued write functionality, so deployment entitlement is an explicit prerequisite;
- a DTMO intelligence item, MISP event, OpenCTI object, IntelOwl result or Taranis assessment never creates a case by itself;
- `POST /api/v1/case` is a mutation candidate only after explicit human-authorized DTMO handoff under dedicated server-side RBAC;
- case-handoff authority is distinct from DTMO publication/share authority;
- DTMO canonical UUID, handoff request/idempotency key, TheHive case identity and organization context must be durably mapped;
- mutable title/tag/assignee values are never identity;
- TLP/PAP/access mappings cannot broaden authoritative source restrictions; unknown or ambiguous mappings fail closed;
- ambiguous mutation delivery blocks blind replay and requires reconciliation;
- attachments, raw source bodies, credentials, private enrichment and unrelated personal data are excluded by default;
- TheHive case lifecycle does not become canonical CTI truth, local-compromise proof or DTMO external-share authority;
- responders, Cortex execution, automatic MISP→TheHive automation, external sharing and platform/organization administration are outside this slice.

```mermaid
flowchart LR
    D[(DTMO canonical intelligence)] --> A{Human case-handoff approval?}
    A -->|no| N[No TheHive mutation]
    A -->|yes| V{Identity + provenance + TLP/PAP valid?}
    V -->|no| X[Fail closed]
    V -->|yes| R[(Durable handoff reservation)]
    R --> C[TheHive API v1\nPOST /api/v1/case]
    C -->|201 + case identity| M[(DTMO↔TheHive mapping)]
    C -->|timeout/ambiguous| U[Block blind replay\noperator reconcile]
    M --> H[TheHive case lifecycle]
    H -. never grants .-> S[DTMO publication/share authority]
```

Repository CI for this contract is engineering evidence only. It does not establish live connectivity, license entitlement, deployed service-account permissions, organization/access configuration, privacy approval, real-data TLP/PAP correctness, HA/recovery, independent assurance or production authorization.

After protected acceptance of the contract baseline, the next bounded 11.6 slice may implement the minimal human-authorized case-handoff adapter and durable identity/replay state.

### 11.7 Cortex decision gate

**Status:** `PLANNED / CONDITIONAL`

Adopt Cortex only when an accepted capability-gap analysis proves IntelOwl cannot satisfy a validated requirement. TheHive integration does not itself justify Cortex adoption.

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

1. Accept the **Phase 11.6 TheHive handoff contract** on fully green exact-head CI.
2. Implement the minimal human-authorized TheHive case-handoff adapter and durable identity/replay state in a separate bounded PR.
3. Complete Phase 11.6 before considering the conditional 11.7 Cortex decision gate.
4. Continue 11.8–11.11 in fixed order and enter Phase 12 only after every required Phase 11 gate is accepted.

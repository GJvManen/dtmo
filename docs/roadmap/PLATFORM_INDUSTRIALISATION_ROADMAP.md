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

Cortex is intentionally absent from the target unless Phase 11.7 demonstrates a validated IntelOwl capability gap. Provenance, RBAC, human publication/share authority and fail-closed evidence rules remain explicit across every boundary.

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

### 11.1–11.2 Taranis AI

**Status:** `PASS / REPOSITORY_COMPLETE`

### 11.3 IntelOwl enrichment integration

**Status:** `PASS / REPOSITORY_COMPLETE`

The accepted boundary provides bounded human-authorized generic enrichment, explicit analyzer allowlisting, TLP/handling checks, stable job/analyzer identity, partial-result semantics, durable enrichment history and database-enforced no-share/no-local-compromise invariants.

### 11.4 OpenCTI knowledge-graph integration

**Status:** `PASS / REPOSITORY_COMPLETE`

### 11.5 MISP consolidation

**Status:** `PASS / REPOSITORY_COMPLETE`

MISP remains a separate AGPL-3.0 service/API with governed inbound/outbound exchange, durable synchronization state, authoritative distribution/sharing-group/TLP restrictions and human-approved unpublished export.

### 11.6 TheHive incident/case handoff

**Status:** `PASS / REPOSITORY_COMPLETE`

The accepted Phase 11.6 boundary provides only the minimal human-authorized `POST /api/v1/case` path, dedicated `handoff:case` permission, durable reservation before mutation, stable request/item/case/organization identity, `reserved`/`delivered`/`ambiguous`/`failed` reconciliation, blocked blind replay after ambiguity, minimized payloads and hard no-share/no-local-compromise invariants. Responders, Cortex, automatic MISP→TheHive automation, external sharing and administration remain excluded.

Live TheHive use still requires actual entitlement, credentials, effective permissions, organization scope, privacy/handling approval and later deployment-bound validation; repository acceptance does not invent that evidence.

### 11.7 Cortex decision gate

**Status:** `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`

The conditional decision record is `docs/architecture/CORTEX_DECISION_GATE.md`. The current review finds **no validated IntelOwl capability gap for the approved DTMO enrichment requirement set** and therefore proposes **no Cortex adoption** in the current Phase 11 candidate.

The decision is based on the accepted IntelOwl capabilities for observable enrichment, analyzer/playbook governance, human authorization, TLP/handling control, stable job identity, partial-result handling, provenance and bounded outage behavior. IntelOwl Connectors remain deliberately excluded because they create external side effects; that exclusion is an authority boundary, not a validated enrichment defect.

Cortex analyzers/responders would add a new service, secret, identity, licensing/maintenance and mutation/response authority boundary. Responders are outside the accepted enrichment requirement and TheHive case handoff does not itself justify Cortex.

```mermaid
flowchart LR
    R[Validated enrichment requirements] --> I[IntelOwl accepted boundary]
    I --> G{Validated material gap?}
    G -->|no| N[Do not adopt Cortex]
    G -->|future evidence| A[New bounded gap assessment]
    A --> C{Cortex uniquely justified?}
    C -->|yes| P[Separate architecture/security/licensing PR]
    C -->|no| N
```

Phase 11.7 is complete only after the decision record, QA contract, current-state documentation and exact-head CI are protected-merged. A future Cortex proposal requires a new attributable requirement and cannot reopen this decision by preference alone.

### 11.8 Integrated runtime industrialisation

**Status:** `PLANNED / NEXT AFTER 11.7 ACCEPTANCE`

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

1. Accept the **Phase 11.7 Cortex decision gate** on fully green exact-head CI.
2. If accepted, record Cortex as not adopted for the current candidate because no validated IntelOwl gap exists.
3. Start exactly Phase 11.8 integrated runtime industrialisation.
4. Continue 11.9–11.11 in fixed order and enter Phase 12 only after every required Phase 11 gate is accepted.

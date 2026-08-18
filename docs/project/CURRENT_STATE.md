# DTMO Current Project State

Last reconciled: **2026-08-18**  
Software baseline: **16.0.0rc12 plus accepted post-RC13, E8 and Phase 11 repository enhancements**

## Executive summary

DTMO has completed Phases 1–7, RC13 functional acceptance and E8.1–E8.10 product evolution. Phase 8 and Phase 9 evidence remain historical and candidate-bound. Phase 10 concluded **`NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`**. DTMO is **not production authorized**.

The active programme is **Phase 11 — Platform Industrialisation**. Phase 11.1–11.8c are `PASS / REPOSITORY_COMPLETE`. The sole active bounded objective is **Phase 11.8d HA and disruption hardening**, currently `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`.

## Lifecycle position

| Stage | Status |
|---|---|
| Phases 1–7 | `PASS` |
| RC13 + owner retest | `PASS / OWNER_ACCEPTED` |
| E8.1–E8.10 | `PASS / REPOSITORY_COMPLETE` |
| Phase 8 | `PASS / OWNER_ACCEPTED — HISTORICAL CANDIDATE` |
| Phase 9 | `PASS / EXTERNAL_ASSURANCE_ACCEPTED — HISTORICAL CANDIDATE` |
| Phase 10 | `NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED` |
| Phase 11 | `IN PROGRESS / ACTIVE` |
| Phase 11.1–11.2 Taranis | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.3 IntelOwl | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.4 OpenCTI | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.5 MISP | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.6 TheHive | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.7 Cortex decision gate | `PASS / REPOSITORY_COMPLETE — HISTORICAL DECISION BASELINE` |
| Phase 11.7b Cortex analyzer connector | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.8a runtime foundation | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.8b workload identity / external secrets | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.8c ingress/TLS + network segmentation | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.8d HA / disruption hardening | `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED` |
| Phase 11.9 migration/compatibility | `NOT STARTED` |
| Phase 11.10 production-equivalent validation | `NOT STARTED` |
| Phase 11.11 independent external assurance | `NOT STARTED` |
| Phase 12 | `NOT STARTED` |

## Accepted Phase 11 service boundaries

Taranis provides governed collection/canonicalization; IntelOwl provides bounded human-authorized enrichment with immutable history; Cortex provides bounded analyzer-only enrichment; OpenCTI provides bounded graph integration and durable identity reconciliation; MISP provides governed inbound/outbound exchange with authoritative restriction state; TheHive provides minimal explicit human-authorized case handoff with durable mutation reservation/reconciliation and no blind replay after ambiguity.

All remain separate service and licensing boundaries. None gains DTMO human publication/share authority or establishes local compromise by itself. TheHive case-handoff authority remains distinct from publication/share authority.

## Accepted Phase 11.8a–11.8c runtime boundaries

The accepted 11.8a slice establishes the governed Helm/GitOps Kubernetes foundation. The accepted 11.8b slice adds provider-neutral workload identity and opt-in external secret delivery. The accepted 11.8c slice adds TLS-only ingress and explicit ingress-controller namespace/pod network segmentation. These remain repository engineering evidence and do not establish production authorization.

## Active Phase 11.8d HA and disruption boundary

The active slice raises the DTMO application replica default to three, requires at least two replicas, distributes replicas across zone and hostname topology with `DoNotSchedule`, requires host anti-affinity, retains a non-zero PodDisruptionBudget and adds graceful termination. Stateful PostgreSQL, Redis, OpenSearch and object-storage HA remain deployment-specific requirements rather than inferred repository claims.

```mermaid
flowchart LR
    U[Ingress / service traffic] --> A[DTMO replica zone A]
    U --> B[DTMO replica zone B]
    U --> C[DTMO replica zone C]
    A --> S[(Stateful service boundary)]
    B --> S
    C --> S
    PDB[PodDisruptionBudget] -. voluntary disruption guard .-> A
    PDB -. voluntary disruption guard .-> B
    PDB -. voluntary disruption guard .-> C
```

Availability controls do not grant publication/share authority, case-handoff authority, responder authority or proof of local compromise. Missing required HA configuration fails closed.

## Governance and evidence boundary

Repository CI can prove chart, scheduling-policy and documentation contracts only. It cannot prove real multi-zone placement, zone-failure survival, stateful quorum/failover, provider durability, recovery objectives, production-equivalent behavior, independent assurance or production authorization.

Historical Phase 8/9 evidence remains valid only for the earlier candidate and is not reused for the materially changed Phase 11 platform. Fresh Phase 11.10 production-equivalent validation and Phase 11.11 independent assurance remain required before Phase 12.

## Phase 11 fixed order

1. Taranis AI — `PASS / REPOSITORY_COMPLETE`;
2. IntelOwl — `PASS / REPOSITORY_COMPLETE`;
3. OpenCTI — `PASS / REPOSITORY_COMPLETE`;
4. MISP — `PASS / REPOSITORY_COMPLETE`;
5. TheHive — `PASS / REPOSITORY_COMPLETE`;
6. original Cortex conditional decision — historical `PASS / REPOSITORY_COMPLETE`;
7. owner-required Cortex analyzer connector — `PASS / REPOSITORY_COMPLETE`;
8. Kubernetes/Helm/GitOps and integrated runtime hardening — active Phase 11.8, with 11.8a–11.8c accepted and 11.8d active;
9. migration/compatibility;
10. new production-equivalent validation;
11. new independent external assurance;
12. Phase 12 formal production GO/NO-GO.

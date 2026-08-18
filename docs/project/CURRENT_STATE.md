# DTMO Current Project State

Last reconciled: **2026-08-18**  
Software baseline: **16.0.0rc12 plus accepted post-RC13, E8 and Phase 11 repository enhancements**

## Executive summary

DTMO has completed Phases 1–7, RC13 functional acceptance and E8.1–E8.10 product evolution. Phase 8 and Phase 9 evidence remain historical and candidate-bound. Phase 10 concluded **`NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`**. DTMO is **not production authorized**.

The active programme is **Phase 11 — Platform Industrialisation**. Phase 11.1–11.7b are `PASS / REPOSITORY_COMPLETE`. Phase 11.8a runtime foundation is now `PASS / REPOSITORY_COMPLETE` after protected exact-head merge of PR #287. The sole active bounded objective is **Phase 11.8b workload identity and external secret delivery**, currently `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`.

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
| Phase 11.8b workload identity / external secrets | `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED` |
| Phase 11.9 migration/compatibility | `NOT STARTED` |
| Phase 11.10 production-equivalent validation | `NOT STARTED` |
| Phase 11.11 independent external assurance | `NOT STARTED` |
| Phase 12 | `NOT STARTED` |

## Accepted Phase 11 service boundaries

Taranis provides governed collection/canonicalization; IntelOwl provides bounded human-authorized enrichment with immutable history; Cortex provides bounded analyzer-only enrichment; OpenCTI provides bounded graph integration and durable identity reconciliation; MISP provides governed inbound/outbound exchange with authoritative restriction state; TheHive provides minimal explicit human-authorized case handoff with durable mutation reservation/reconciliation and no blind replay after ambiguity.

All remain separate service and licensing boundaries. None gains DTMO human publication/share authority or establishes local compromise by itself. TheHive case-handoff authority remains distinct from publication/share authority.

## Accepted Phase 11.8a runtime foundation

The accepted 11.8a slice establishes the governed Helm/GitOps Kubernetes foundation for the DTMO application workload: immutable image digest, existing-secret consumption, non-root/read-only workload hardening, disabled service-account token automounting, probes/resources, PodDisruptionBudget and fail-closed NetworkPolicy. Repository acceptance does not claim live-cluster availability, HA, recovery or production readiness.

## Active Phase 11.8b identity and secret-delivery boundary

The active slice adds an explicit workload-identity attachment point through ServiceAccount annotations while keeping Kubernetes service-account token automount disabled. It optionally renders an ExternalSecret that references an explicitly named external SecretStore/ClusterSecretStore and explicit per-variable remote mappings. No identity credential or secret value is stored in Git, and DTMO consumes only the resulting Kubernetes Secret rather than directly calling the provider API.

```mermaid
flowchart LR
    G[Reviewed GitOps revision] --> H[Helm render]
    H --> SA[DTMO ServiceAccount\nno token automount]
    A[Deployment-owned identity annotation] --> SA
    SA -. workload identity .-> IAM[External identity authority]
    IAM --> STORE[Approved secret provider]
    ES[External Secrets controller] --> STORE
    H --> ES
    ES --> KS[Kubernetes Secret]
    KS --> P[DTMO pod]
```

Workload identity and secret delivery do not grant publication/share authority, case-handoff authority, responder authority or proof of local compromise. Missing or ambiguous identity/store/secret evidence fails closed.

## Governance and evidence boundary

Repository CI can prove chart, policy and documentation contracts only. It cannot prove Kubernetes admission behavior, cloud IAM, provider ACLs, live secret rotation/revocation, controller installation, CNI enforcement, runtime availability, recovery objectives, service entitlement or lawful disclosure authorization.

Historical Phase 8/9 evidence remains valid only for the earlier candidate and is not reused for the materially changed Phase 11 platform. Fresh Phase 11.10 production-equivalent validation and Phase 11.11 independent assurance remain required before Phase 12.

## Phase 11 fixed order

1. Taranis AI — `PASS / REPOSITORY_COMPLETE`;
2. IntelOwl — `PASS / REPOSITORY_COMPLETE`;
3. OpenCTI — `PASS / REPOSITORY_COMPLETE`;
4. MISP — `PASS / REPOSITORY_COMPLETE`;
5. TheHive — `PASS / REPOSITORY_COMPLETE`;
6. original Cortex conditional decision — historical `PASS / REPOSITORY_COMPLETE`;
7. owner-required Cortex analyzer connector — `PASS / REPOSITORY_COMPLETE`;
8. Kubernetes/Helm/GitOps and integrated runtime hardening — active Phase 11.8, with 11.8a accepted and 11.8b active;
9. migration/compatibility;
10. new production-equivalent validation;
11. new independent external assurance;
12. Phase 12 formal production GO/NO-GO.

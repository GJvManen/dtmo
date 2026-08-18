# DTMO Executive Decision View

## Purpose

This document gives accountable decision makers the concise current decision position for DTMO production readiness and the active Phase 11 successor programme.

## Current position

| Decision area | Current state | Decision consequence |
|---|---|---|
| Repository-controlled engineering | `PASS` for Phases 1–7 | Engineering foundation accepted |
| Functional product | `RC13 PASS / OWNER_ACCEPTED` | Canonical product journey accepted |
| E8 vulnerability/CTI product line | `PASS / REPOSITORY_COMPLETE` | Repository product baseline accepted |
| Phase 8 production-equivalent staging | `PASS / OWNER_ACCEPTED` | Historical evidence for prior candidate only |
| Phase 9 independent assurance | `PASS / EXTERNAL_ASSURANCE_ACCEPTED` | Historical evidence for prior candidate only |
| Phase 10 production authorization | `NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED` | Production authorization not granted |
| Phase 11.1–11.8b | `PASS / REPOSITORY_COMPLETE` | Accepted integration/runtime boundaries |
| Phase 11.8c ingress/TLS + network segmentation | `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED` | Current bounded north-south network gate |
| Phase 11 platform industrialisation | `IN PROGRESS / ACTIVE` | Highest-priority programme |
| Phase 12 production authorization | `NOT STARTED` | New decision only after fresh validation and assurance |

## Decision interpretation

DTMO has not received a production `GO`. Historical Phase 8 and Phase 9 evidence remains valid only for the candidate it originally covered and cannot be treated as production acceptance of the materially changed Phase 11 platform.

The active engineering decision is whether Phase 11.8c establishes a fail-closed TLS ingress and explicit ingress-controller network boundary without inventing live deployment evidence or weakening accepted service boundaries.

## Phase 11 progression

1. Taranis architecture/licensing and canonical adapter — completed.
2. IntelOwl bounded enrichment integration — completed.
3. OpenCTI graph integration — completed.
4. MISP governed exchange/consolidation — completed.
5. TheHive human-authorized case handoff — completed.
6. Original Cortex conditional decision — historical accepted baseline.
7. Owner-required Cortex analyzer connector — completed separately as Phase 11.7b.
8. Phase 11.8a runtime foundation — accepted.
9. Phase 11.8b workload identity/external secret delivery — accepted.
10. **Active:** Phase 11.8c ingress/TLS and network segmentation.
11. Migration/compatibility — not started.
12. New production-equivalent validation — not started.
13. New independent external assurance — not started.
14. Phase 12 formal production GO/NO-GO — not started.

## Phase 11.8c decision boundary

The active slice requires ingress disabled by default, explicit ingress class and hostname, mandatory TLS and TLS Secret reference, a `ClusterIP` application Service, enabled NetworkPolicy, and ingress-controller reachability constrained by both namespace and pod selectors.

```mermaid
flowchart LR
    C[External client] -->|TLS| I[Approved ingress controller]
    T[Kubernetes TLS Secret] --> I
    I -->|namespace + pod selectors| N[DTMO NetworkPolicy]
    N --> S[ClusterIP Service]
    S --> P[DTMO workload]
```

Taranis AI, IntelOwl, Cortex, OpenCTI, MISP and TheHive remain separate service/licensing/identity boundaries. Kubernetes scheduling or network reachability cannot grant human publication/share authority, TheHive case-handoff authority, or prove local compromise.

## Decision rules

- Green CI is repository engineering evidence, not production authorization.
- Historical Phase 8/9 evidence remains deployment/candidate-bound.
- Service integrations preserve provenance, least privilege, RBAC and applicable licensing boundaries.
- Secret values and TLS private keys are not committed to Git; live certificate/provider evidence is deployment-bound.
- Missing or conflicting mandatory evidence fails closed.
- Phase 11.8c acceptance does not imply HA/recovery/observability/supply-chain completion.

## Current decision

**Phase 10 remains `NO-GO / BLOCKED`. Phase 11.1–11.8b are `PASS / REPOSITORY_COMPLETE`. Phase 11.8c is `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`. DTMO remains not production authorized; Phase 12 is `NOT STARTED` and requires accepted Phase 11.10/11.11 evidence for one immutable integrated candidate.**
# DTMO Executive Status

Date: **2026-08-18**  
Software baseline: **16.0.0rc12 plus accepted post-RC13/E8/Phase-11 repository enhancements**

## Management summary

DTMO has an accepted repository-controlled engineering baseline, RC13 `PASS / OWNER_ACCEPTED` functional acceptance and E8.1–E8.10 `PASS / REPOSITORY_COMPLETE` product evolution. Phase 8 remains `PASS / OWNER_ACCEPTED` and Phase 9 remains `PASS / EXTERNAL_ASSURANCE_ACCEPTED` for the earlier candidate they actually covered. Those historical evidence classes are not transferred to the materially changed Phase 11 platform.

Phase 10 remains **`NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`**. DTMO is **not production authorized**.

The highest-priority programme is **Phase 11 Platform Industrialisation**, `IN PROGRESS / ACTIVE`. Phase 11.1–11.8b are `PASS / REPOSITORY_COMPLETE`; the original Phase 11.7 Cortex no-adoption decision remains preserved as a historical decision baseline, while the later owner-required 11.7b analyzer connector is accepted separately. The sole active bounded objective is **Phase 11.8c ingress/TLS and network segmentation**, currently `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`.

Phase 12 remains `NOT STARTED` and can only begin after fresh Phase 11.10 production-equivalent validation and Phase 11.11 independent external assurance against the same immutable integrated candidate.

## Current decision position

| Decision area | Status | Consequence |
|---|---|---|
| Engineering baseline | `PASS` | Repository foundation accepted |
| Functional product | `PASS / OWNER_ACCEPTED` | Canonical console journey accepted |
| E8 product evolution | `PASS / REPOSITORY_COMPLETE` | Repository product baseline accepted |
| Phase 8 | `PASS / OWNER_ACCEPTED` | Historical candidate-bound staging evidence |
| Phase 9 | `PASS / EXTERNAL_ASSURANCE_ACCEPTED` | Historical candidate-bound assurance evidence |
| Phase 10 | `NO-GO / BLOCKED` | Production authorization not granted |
| Phase 11.1–11.8b | `PASS / REPOSITORY_COMPLETE` | Accepted integration/runtime boundaries |
| Phase 11.8c ingress/TLS + network segmentation | `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED` | Active north-south network-boundary gate |
| Phase 11.9–11.11 | `NOT STARTED` | Follow only after bounded 11.8 completion |
| Phase 12 | `NOT STARTED` | New formal production decision |

## Active Phase 11.8c control objective

Phase 11.8c establishes a governed north-south DTMO application boundary only: ingress disabled by default, mandatory TLS when enabled, explicit ingress class/hostname/TLS Secret reference, `ClusterIP` application Service, mandatory NetworkPolicy and ingress-controller reachability constrained by both namespace and pod selectors.

```mermaid
flowchart LR
    C[External client] -->|TLS| I[Approved ingress controller]
    T[Kubernetes TLS Secret] --> I
    I -->|namespace + pod selectors| N[DTMO NetworkPolicy]
    N --> S[ClusterIP Service]
    S --> P[DTMO pods]
```

This slice does not establish DNS ownership, certificate validity, live ingress-controller admission, cloud load-balancer/WAF policy, CNI enforcement, multi-zone/stateful HA, centralized observability, recovery objectives, SBOM/scanning/signing/attestation, capacity or exercised upgrade/rollback. Those remain later bounded Phase 11.8 objectives.

## Security, authority and licensing boundaries

Taranis AI, IntelOwl, Cortex, OpenCTI, MISP and TheHive remain separate services under their applicable licensing/provider boundaries. Kubernetes placement and network reachability do not transfer service ownership, grant DTMO publication/share authority, grant case-handoff authority, or prove local compromise. Provenance, RBAC, human/service identity separation and fail-closed handling remain mandatory.

## Evidence boundaries

Repository CI for Phase 11.8c is repository engineering evidence only. It cannot prove live DNS, certificate, ingress-controller, load-balancer/WAF or CNI behavior, availability, recovery, production-equivalent characteristics, independent assurance or production authorization. Historical Phase 8/9 evidence remains candidate-bound.

## Executive recommendation

Continue only the active Phase 11.8c bounded slice. Merge only after the dedicated ingress/TLS/network gate, RC4, Professional Documentation and all required exact-head checks are green on the same final head with expected-head protection. Do not start the next 11.8 slice before protected acceptance.
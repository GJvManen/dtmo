# DTMO Executive Status

Date: **2026-08-17**  
Software baseline: **16.0.0rc12 plus accepted post-RC13/E8/Phase-11 repository enhancements**

## Management summary

DTMO has an accepted repository-controlled engineering baseline, RC13 `PASS / OWNER_ACCEPTED` functional product and E8.1–E8.10 `PASS / REPOSITORY_COMPLETE` product baseline. Phase 8 is `PASS / OWNER_ACCEPTED` and Phase 9 is `PASS / EXTERNAL_ASSURANCE_ACCEPTED` for the earlier candidate they covered.

Phase 10 remains **`NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`**. DTMO is **not production authorized**.

The highest-priority programme is **Phase 11 Platform Industrialisation**. Phase 11.1–11.5 and the Phase 11.6 TheHive contract are `PASS / REPOSITORY_COMPLETE`. The sole active bounded objective is the **minimal human-authorized TheHive case-handoff implementation with durable reservation/reconciliation state**, currently `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`.

A new Phase 12 production GO/NO-GO occurs only after the materially changed integrated platform completes fresh Phase 11.10 production-equivalent validation and Phase 11.11 independent external assurance.

## Current decision position

| Decision area | Status | Consequence |
|---|---|---|
| Engineering baseline | `PASS` | Repository foundation accepted |
| Functional product | `PASS / OWNER_ACCEPTED` | Canonical console journey accepted |
| E8 product evolution | `PASS / REPOSITORY_COMPLETE` | Vulnerability/CTI scope accepted in repository |
| Phase 8 | `PASS / OWNER_ACCEPTED` | Historical staging acceptance for prior candidate |
| Phase 9 | `PASS / EXTERNAL_ASSURANCE_ACCEPTED` | Historical independent assurance for prior candidate |
| Phase 10 | `NO-GO / BLOCKED` | Production authorization not granted |
| Phase 11.1–11.5 | `PASS / REPOSITORY_COMPLETE` | Taranis, IntelOwl, OpenCTI and MISP boundaries accepted |
| Phase 11.6 TheHive contract | `PASS / REPOSITORY_COMPLETE` | Service/API/identity/licensing/authority baseline accepted |
| Phase 11.6 TheHive implementation | `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED` | Active human-authorized case-handoff/state gate |
| Phase 12 | `NOT STARTED` | New production decision only after integrated validation/assurance |

## Active Phase 11.6 control objective

TheHive remains a separate StrangeBee service. The reviewed baseline is TheHive 5.5.16 using public API v1. The accepted contract now permits one bounded runtime mutation path: explicit human-authorized `POST /api/v1/case`.

The implementation introduces a dedicated `handoff:case` permission, distinct from publication/share approval, and keeps service accounts outside the human authorization boundary. Before mutation DTMO requires canonical identity, provenance and explicit severity/TLP/PAP handling, then commits a durable reservation. A stable returned TheHive case identity is required for `delivered`; uncertain delivery becomes `ambiguous` and blocks blind replay.

The persisted handoff outcome is minimized and database constraints prevent handoff state from granting external-share authority or becoming local-compromise proof. Known authoritative MISP distribution/sharing-group restrictions currently block TheHive handoff because no deployment-approved cross-service access mapping exists; DTMO does not infer one.

The feature remains disabled by default. Live use requires actual TheHive entitlement, HTTPS endpoint, runtime token, target organization, least-privilege service permissions and privacy/handling approval. Repository CI cannot prove those deployment facts.

Responders, Cortex execution, task/observable creation, automatic MISP→TheHive automation, case deletion, external sharing and platform/organization administration remain outside this bounded slice.

## Strategic architecture and licensing

The fixed order remains Taranis → IntelOwl → OpenCTI → MISP consolidation → TheHive → conditional Cortex → Kubernetes/Helm/GitOps hardening → migration/compatibility → new production-equivalent validation → new independent assurance → Phase 12.

Taranis, IntelOwl, OpenCTI, MISP and TheHive remain separate services under their applicable licensing boundaries. No upstream source vendoring is implied by repository integration work.

## Evidence boundaries

Repository CI for this slice can establish synthetic adapter, RBAC, persistence, migration, state-machine and documentation behavior only. It does not prove live TheHive connectivity, activated license entitlement, deployed permissions, target-organization/access configuration, lawful real-data transfer, production-equivalent validation, independent assurance or production authorization. Historical Phase 8/9 evidence remains candidate-bound and cannot be reused for the materially changed Phase 11 platform.

## Executive recommendation

Continue only the active Phase 11.6 implementation slice. Merge only when its dedicated implementation gate, RC4, Professional Documentation and all required exact-head checks are green with expected-head protection. After protected acceptance, mark Phase 11.6 repository-complete and evaluate Phase 11.7 Cortex only if a validated IntelOwl capability gap exists.

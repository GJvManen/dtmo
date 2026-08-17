# DTMO Executive Status

Date: **2026-08-17**  
Software baseline: **16.0.0rc12 plus accepted post-RC13/E8/Phase-11 repository enhancements**

## Management summary

DTMO has an accepted repository-controlled engineering baseline, RC13 `PASS / OWNER_ACCEPTED` functional product and E8.1–E8.10 `PASS / REPOSITORY_COMPLETE` product baseline. Phase 8 is `PASS / OWNER_ACCEPTED` and Phase 9 is `PASS / EXTERNAL_ASSURANCE_ACCEPTED` for the earlier candidate they covered.

Phase 10 remains **`NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`**. DTMO is **not production authorized**.

The highest-priority programme is **Phase 11 Platform Industrialisation**. Phase 11.1–11.5 are `PASS / REPOSITORY_COMPLETE`. The sole active bounded objective is **Phase 11.6 TheHive incident/case handoff contract**, currently `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`.

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
| Phase 11.6 TheHive contract | `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED` | Active service/API/identity/licensing/authority gate |
| Phase 12 | `NOT STARTED` | New production decision only after integrated validation/assurance |

## Active Phase 11.6 control objective

TheHive remains a separate StrangeBee service. The reviewed baseline is TheHive 5.5.16 using public API v1. The current slice defines the boundary before any runtime case mutation is implemented.

The initial case-creation candidate is `POST /api/v1/case`, but no DTMO intelligence item may create a case automatically. A later implementation must require explicit human case-handoff approval under dedicated server-side RBAC, a least-privilege non-human TheHive identity, stable DTMO↔TheHive identity mapping, durable idempotency/reconciliation state and fail-closed TLP/PAP/access mapping.

Case-handoff authority and publication/share authority remain separate. TheHive case state does not become canonical CTI truth, prove local compromise or grant DTMO external-share authority. Ambiguous mutation delivery must block blind replay.

TheHive 5.3+ requires an activated Community, Gold or Platinum license for continued write functionality. Repository CI cannot prove deployed entitlement, organization scope, service-account permissions, privacy approval or operational readiness.

Responders, Cortex execution, automatic MISP→TheHive automation, external sharing and platform/organization administration remain outside this bounded slice.

## Strategic architecture and licensing

The fixed order remains Taranis → IntelOwl → OpenCTI → MISP consolidation → TheHive → conditional Cortex → Kubernetes/Helm/GitOps hardening → migration/compatibility → new production-equivalent validation → new independent assurance → Phase 12.

Taranis, IntelOwl, OpenCTI, MISP and TheHive remain separate services under their applicable licensing boundaries. No upstream source vendoring is implied by repository integration work.

## Evidence boundaries

Repository CI for this slice can establish documentation and policy-contract consistency only. It does not prove live TheHive connectivity, activated license entitlement, deployed permissions, target-organization/access configuration, lawful data transfer, staging acceptance, independent assurance or production authorization. Historical Phase 8/9 evidence remains candidate-bound and cannot be reused for the materially changed Phase 11 platform.

## Executive recommendation

Continue only the active Phase 11.6 contract slice. Merge only when the full exact-head CI matrix, dedicated TheHive contract gate and Professional Documentation Gate are green with expected-head protection. After protected acceptance, proceed to a separate bounded implementation PR for the minimal human-authorized case-handoff adapter and durable mutation reconciliation state.

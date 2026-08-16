# DTMO Executive Status

Date: **2026-08-17**  
Software baseline: **16.0.0rc12 plus accepted post-RC13/E8/Phase-11 repository enhancements**

## Management summary

DTMO has an accepted repository-controlled engineering baseline, RC13 `PASS / OWNER_ACCEPTED` functional product and E8.1–E8.10 `PASS / REPOSITORY_COMPLETE` product baseline. Phase 8 is `PASS / OWNER_ACCEPTED` and Phase 9 is `PASS / EXTERNAL_ASSURANCE_ACCEPTED` for the earlier candidate they covered.

Phase 10 remains **`NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`**. DTMO is **not production authorized**.

The highest-priority programme is **Phase 11 Platform Industrialisation**. Phase 11.1–11.2 Taranis, Phase 11.3 IntelOwl and Phase 11.4 OpenCTI are `PASS / REPOSITORY_COMPLETE`. The Phase 11.5 MISP consolidation contract is also `PASS / REPOSITORY_COMPLETE`. The sole active bounded objective is **Phase 11.5 MISP synchronization-state/persistence and authority enforcement**, currently `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`.

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
| Phase 11.1–11.2 | `PASS / REPOSITORY_COMPLETE` | Taranis boundary and adapter accepted |
| Phase 11.3 | `PASS / REPOSITORY_COMPLETE` | IntelOwl integration accepted |
| Phase 11.4 | `PASS / REPOSITORY_COMPLETE` | OpenCTI contract, read adapter and persistence accepted |
| Phase 11.5 MISP contract | `PASS / REPOSITORY_COMPLETE` | Service/API/licensing/authority model accepted |
| Phase 11.5 MISP state | `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED` | Active persistence/authority implementation gate |
| Phase 12 | `NOT STARTED` | New production decision only after integrated validation/assurance |

## Active Phase 11.5 control objective

MISP remains a separate AGPL-3.0 service/API component. DTMO reuses the existing governed `events/restSearch` inbound path and human-approved unpublished `events/add` outbound path rather than creating a parallel client.

The active implementation introduces durable `misp_synchronization_state`, binding one DTMO canonical item to one stable MISP event UUID and its source distribution/sharing-group/TLP authority envelope. Accepted restrictions are projected to canonical `metadata_json.misp_restrictions`, which is already enforced by governed export.

Canonical MISP candidate persistence and authority-state reconciliation occur in the same database transaction. Event identity collisions, identity drift, unknown/incomplete source restrictions and inbound attempts to grant external-share authority fail closed. Database constraints preserve known distribution semantics, required sharing-group context and `external_share_authorized=false`.

Human review/share approval remains the only outbound authority. Automatic MISP server federation, automatic OpenCTI↔MISP synchronization, event publication, TheHive case creation and Cortex work are outside this bounded slice.

## Strategic architecture and licensing

The fixed order remains Taranis → IntelOwl → OpenCTI → MISP consolidation → TheHive → conditional Cortex → Kubernetes/Helm/GitOps hardening → migration/compatibility → new production-equivalent validation → new independent assurance → Phase 12.

Taranis, IntelOwl, OpenCTI and MISP remain separate services under their applicable licensing boundaries. No upstream source vendoring is implied by repository integration work.

## Evidence boundaries

Repository CI for this slice can establish schema/migration correctness, same-transaction MISP restriction reconciliation, synthetic conflict handling and documentation synchronization. It does not prove live MISP credentials, deployed permissions, remote-server trust, lawful production data sharing, staging acceptance, independent assurance or production authorization. Historical Phase 8/9 evidence remains candidate-bound and cannot be reused for the materially changed Phase 11 platform.

## Executive recommendation

Continue only the active Phase 11.5 synchronization-state/persistence implementation. Merge only when the full exact-head CI matrix, dedicated MISP state gate and Professional Documentation Gate are green with expected-head protection. After protected acceptance and lifecycle reconciliation, Phase 11.5 may become `PASS / REPOSITORY_COMPLETE`; only then start Phase 11.6 TheHive.

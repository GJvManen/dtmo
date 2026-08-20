# DTMO Current Project State

Last reconciled: **2026-08-20**  
Software baseline: **16.0.0rc12 plus accepted post-RC13, E8 and Phase 11 repository enhancements**

## Executive summary

DTMO has completed Phases 1–7, RC13 functional acceptance and E8.1–E8.10 product evolution. Phase 8 and Phase 9 evidence remain historical and candidate-bound. Phase 10 concluded **`NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`**. DTMO is **not production authorized**.

The active programme is **Phase 11 — Platform Industrialisation**. Phase 11.1–11.9 and Phase 11.10a–11.10f are `PASS / REPOSITORY_COMPLETE`. Phase 11.10 remains `IN PROGRESS / FRESH CANDIDATE-BOUND EVIDENCE REQUIRED`.

The sole active bounded objective is **Phase 11.10g MISP Sharing & Exchange**, status `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`. Phase 11.10f delivered the accepted OpenCTI graph/entity workspace. Phase 11.10g makes the canonical `/workbench/sharing` route functional by composing DTMO's existing human review, independent share approval and replay-protected MISP export controls without creating publication or synchronization authority.

Fresh production-equivalent execution remains deferred until 11.10a–11.10o are complete and one immutable integrated candidate is frozen for 11.10p.

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
| Phase 11.8 integrated runtime industrialisation | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.8a runtime foundation | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.8b workload identity / external secrets | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.8c ingress/TLS + network segmentation | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.8d HA / disruption hardening | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.8e observability hardening | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.8f backup / restore / recovery hardening | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.8g software supply-chain hardening | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.8h capacity / resource planning | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.8i exercised upgrade / rollback | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.9 migration/compatibility | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.10 production-equivalent validation | `IN PROGRESS / FRESH CANDIDATE-BOUND EVIDENCE REQUIRED` |
| Phase 11.10a frontend architecture/design contract | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.10b canonical application shell | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.10c Command Center | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.10d Unified Intelligence Workspace | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.10e IntelOwl/Cortex integrated analysis | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.10f OpenCTI graph/entity workspace | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.10g MISP Sharing & Exchange | `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED` |
| Phase 11.10h TheHive Investigations & Cases | `NOT STARTED` |
| Phase 11.10i Vulnerability & Exposure Center | `NOT STARTED` |
| Phase 11.10j Sources & Collection Control Center | `NOT STARTED` |
| Phase 11.10k Automation & Playbooks | `NOT STARTED` |
| Phase 11.10l Governance & Evidence Center | `NOT STARTED` |
| Phase 11.10m Operations & Administration | `NOT STARTED` |
| Phase 11.10n role-aware UX/accessibility | `NOT STARTED` |
| Phase 11.10o consolidation/full functional acceptance | `NOT STARTED` |
| Phase 11.10p fresh production-equivalent validation | `NOT STARTED / CANDIDATE FREEZE REQUIRED` |
| Phase 11.11 independent external assurance | `NOT STARTED` |
| Phase 12 | `NOT STARTED` |

## Accepted service and runtime boundaries

Taranis, IntelOwl, Cortex, OpenCTI, MISP and TheHive remain separate governed service/licensing boundaries. None gains DTMO human publication/share authority or establishes local compromise by itself. TheHive case-handoff authority remains distinct from publication/share authority.

Phase 11.8 is repository-complete across Kubernetes/Helm/GitOps runtime foundation, workload identity/external-secret delivery, ingress/TLS and network segmentation, HA/disruption, observability, backup/recovery, supply-chain, capacity and exercised upgrade/rollback. Phase 11.9 adds the accepted forward-first migration/application compatibility contract. Application rollback does not authorize automatic database down migration.

These are engineering controls. Repository CI does not by itself establish production-equivalent behavior or production authorization.

## Accepted Unified Operations Workbench baseline

The canonical trust path remains:

**browser → DTMO API → governed integration adapter → upstream service**

The browser is not a privileged integration broker. Role-aware presentation is usability only; **server-side RBAC** remains authoritative.

Accepted workbench slices are:

- 11.10a frontend architecture/design;
- 11.10b React/TypeScript/Vite canonical `/workbench/` shell and migration compatibility paths;
- 11.10c read-only Command Center with fail-closed canonical operational state;
- 11.10d Unified Intelligence Workspace with governed search, canonical detail and provenance;
- 11.10e Integrated Analysis with human-triggered IntelOwl enrichment, analyzer-only Cortex execution and durable evidence history;
- 11.10f OpenCTI graph/entity workspace over persisted OpenCTI/STIX mapping and revision evidence without inferred upstream topology.

IntelOwl/Cortex and OpenCTI-derived context are evidence, not verdicts. They grant no external-share/publication authority and do not prove local compromise.

## Accepted Phase 11.10f OpenCTI graph/entity boundary

Phase 11.10f made `/workbench/intelligence/graph` functional through DTMO-owned read APIs over already persisted OpenCTI evidence.

Frontend-facing contracts are:

- `GET /api/v1/opencti/capabilities`;
- `GET /api/v1/opencti/items/{item_id}/graph`;
- `GET /api/v1/opencti/entities/{mapping_id}`.

Every endpoint requires server-side `read:intelligence`. No OpenCTI write, connector invocation, MISP synchronization, case creation or publication/share action was added.

The Phase 11.4 persistence baseline contains stable OpenCTI/STIX object mappings and immutable revisions. It does **not** durably contain generic OpenCTI entity-to-entity relationship topology. The accepted graph therefore renders only attributable `canonical-mapping` edges between the selected canonical DTMO intelligence object and its persisted OpenCTI mappings. Missing upstream relationship evidence must **fail closed** and must not be visually inferred.

Authoritative Phase 11.10f material remains:

- `backend/dtmo/opencti_workspace.py`;
- `frontend/src/OpenCTIGraphWorkspace.tsx`;
- `frontend/src/opencti-graph.css`;
- `docs/architecture/PHASE11_10F_OPENCTI_GRAPH_ENTITY_WORKSPACE.md`;
- `docs/user/OPENCTI_GRAPH_ENTITY_WORKSPACE.md`;
- `docs/qa/PHASE11_10F_OPENCTI_GRAPH_ENTITY_GATE.md`;
- `backend/tests/test_phase11_10f_opencti_graph_contract.py`;
- `backend/tests/test_phase11_10f_opencti_graph_browser.py`;
- `.github/workflows/phase11-opencti-graph-workspace.yml`.

Repository/browser evidence for that accepted slice does not prove live OpenCTI health, completeness of OpenCTI knowledge, local exposure or compromise, production-equivalent operation, independent assurance or production authorization.

## Active Phase 11.10g MISP Sharing & Exchange boundary

Phase 11.10g replaces the `/workbench/sharing` placeholder with a canonical human-governed MISP workflow. It reuses accepted controls rather than inventing a parallel authority path.

The decision sequence is:

1. inspect canonical sharing state with `read:intelligence`;
2. record human review with `review:intelligence`;
3. record independent human share approval with `approve:share`, performed by a principal different from the reviewer;
4. export an already reviewed and share-approved canonical revision to MISP through the existing governed export API;
5. leave MISP publication and synchronization outside this slice.

The export adapter creates `published=false` events only. For MISP-origin intelligence, authoritative distribution, sharing-group and TLP restrictions remain binding and cannot be weakened on re-export. A persisted `pending`, `success` or `uncertain` export for the current deterministic event UUID blocks automatic replay. An uncertain external result requires operator inspection.

Frontend/browser paths never receive a MISP API key or call MISP directly. Configuration is not live-service health. Successful event creation does not establish MISP publication, synchronization, downstream consumption, local compromise or production readiness.

Authoritative Phase 11.10g material:

- `backend/dtmo/misp_sharing_workspace.py`;
- `backend/dtmo/misp_export_api.py`;
- `backend/dtmo/governance/misp_export.py`;
- `frontend/src/MispSharingWorkspace.tsx`;
- `frontend/src/misp-sharing.css`;
- `docs/architecture/PHASE11_10G_MISP_SHARING_EXCHANGE.md`;
- `docs/user/MISP_SHARING_EXCHANGE_WORKSPACE.md`;
- `docs/qa/PHASE11_10G_MISP_SHARING_EXCHANGE_GATE.md`;
- `backend/tests/test_phase11_10g_misp_sharing_contract.py`;
- `backend/tests/test_phase11_10g_misp_sharing_browser.py`;
- `.github/workflows/phase11-misp-sharing-exchange.yml`.

Repository/browser evidence for this active slice does **not prove** live MISP health, publication/synchronization, production-equivalent operation, independent assurance or production authorization.

After Phase 11.10g exact-head acceptance and merge, the only next bounded priority is **Phase 11.10h — TheHive Investigations & Cases**.

## Phase 11.10p external validation boundary

Fresh production-equivalent validation remains mandatory, but is the final 11.10 candidate step **11.10p** after 11.10a–11.10o candidate completion and functional acceptance.

11.10p requires fresh production-equivalent evidence for the **same immutable** integrated deployment identity and one production-equivalent environment. Required evidence remains candidate identity, migration/compatibility, upgrade, exact-prior-digest rollback with post-rollback health, health/readiness, representative saturation/capacity and recovery/continuity.

Historical Phase 8/9 evidence remains audit history only and is not reusable. Missing, placeholder, inaccessible, mixed-candidate or historical-only evidence must **fail closed**.

The external execution package remains authoritative:

- `docs/qa/PHASE11_10_PRODUCTION_EQUIVALENT_VALIDATION_GATE.md`;
- `docs/operations/PHASE11_10_PRODUCTION_EQUIVALENT_VALIDATION_RUNBOOK.md`;
- `docs/evidence/PHASE11_10_PRODUCTION_EQUIVALENT_EVIDENCE.template.json`;
- `tools/phase11_production_equivalent_validation.py`;
- `backend/tests/test_phase11_10_production_equivalent_validation.py`;
- `.github/workflows/phase11-production-equivalent-validation.yml`.

Phase 11.10 may become `PASS / OWNER_ACCEPTED` only after 11.10a–11.10o are complete, one candidate is frozen, the 11.10p evidence package for the same immutable candidate is complete and the accountable owner accepts it. Phase 11.11 must then run against that same candidate before Phase 12 can make the formal production decision.

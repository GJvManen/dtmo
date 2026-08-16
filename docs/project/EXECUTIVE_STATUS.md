# DTMO Executive Status

Date: **2026-08-16**  
Software baseline: **16.0.0rc12 plus accepted post-RC13/E8/Phase-11 repository enhancements**

## Management summary

DTMO has an accepted repository-controlled engineering baseline, owner-accepted functional product and E8.1–E8.10 `PASS / REPOSITORY_COMPLETE` vulnerability/CTI baseline. Phase 8 is `PASS / OWNER_ACCEPTED` and Phase 9 is `PASS / EXTERNAL_ASSURANCE_ACCEPTED` for the earlier candidate they covered.

The Phase 10 production decision remains **`NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`**. DTMO is **not production authorized**.

The highest-priority programme is **Phase 11 Platform Industrialisation**. Phase 11.1–11.2 Taranis and Phase 11.3 IntelOwl are `PASS / REPOSITORY_COMPLETE`. Within Phase 11.4, the OpenCTI contract and bounded read-only GraphQL/STIX adapter are `PASS / REPOSITORY_COMPLETE`. The sole active bounded objective is **OpenCTI canonical mapping/persistence + operational integration**, currently `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`.

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
| Phase 11.1–11.2 | `PASS / REPOSITORY_COMPLETE` | Taranis service boundary and canonical adapter accepted |
| Phase 11.3 | `PASS / REPOSITORY_COMPLETE` | IntelOwl enrichment integration accepted |
| Phase 11.4 contract | `PASS / REPOSITORY_COMPLETE` | OpenCTI service/API/STIX/licensing boundary accepted |
| Phase 11.4 adapter | `PASS / REPOSITORY_COMPLETE` | Read-only GraphQL/STIX adapter accepted |
| Phase 11.4 persistence | `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED` | Final repository gate before 11.4 completion |
| Phase 12 | `NOT STARTED` | New production decision only after integrated validation/assurance |

## Active Phase 11.4 control objective

The active slice adds durable DTMO-item ↔ OpenCTI internal ID ↔ STIX ID mappings, immutable SHA-256-keyed reconciliation history, fail-closed identity-drift detection, and database constraints that prevent graph context from granting external-share authority or local-compromise proof.

PostgreSQL commit must complete before the durable OpenCTI cursor advances. A failed database transaction leaves the checkpoint unchanged; a checkpoint-write interruption after database commit is replay-safe through stable identity and snapshot-hash idempotency.

OpenCTI remains a separate service boundary. Connector registration, MISP synchronization, external enrichment, TheHive case creation, report publication, security/marking administration and arbitrary GraphQL mutation remain excluded.

## Phase 11 strategic architecture

The fixed order remains Taranis → IntelOwl → OpenCTI → MISP consolidation → TheHive → conditional Cortex → Kubernetes/Helm/GitOps hardening → migration/compatibility → new production-equivalent validation → new independent assurance → Phase 12.

## Key control boundaries

Server-side RBAC, least privilege, human/service separation, provenance/confidence preservation, data minimization, audit/correlation and separate human external-share authority remain mandatory. OpenCTI graph context cannot establish DTMO-local exposure, compromise, severity or publication authority.

OpenCTI routine integration must not require administrator or `Bypass all capabilities` authority. Community Edition is Apache-2.0; Enterprise Edition is separately licensed and Enterprise-only dependencies require explicit entitlement/legal approval.

Repository CI remains engineering evidence. Prior Phase 8/9 acceptance is not transferable to the materially changed Phase 11 platform.

## Executive recommendation

Continue the active Phase 11.4 persistence slice only. Merge only after full exact-head CI and the Professional Documentation Gate are green with expected-head protection. After protected acceptance, reconcile Phase 11.4 to `PASS / REPOSITORY_COMPLETE` and start exactly Phase 11.5 MISP consolidation. Do not enter Phase 12 early.

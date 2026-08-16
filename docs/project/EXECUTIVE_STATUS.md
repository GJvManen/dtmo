# DTMO Executive Status

Date: **2026-08-16**  
Software baseline: **16.0.0rc12 plus accepted post-RC13/E8/Phase-11 repository enhancements**

## Management summary

DTMO has an accepted repository-controlled engineering baseline, owner-accepted functional product and E8.1–E8.10 `PASS / REPOSITORY_COMPLETE` vulnerability/CTI baseline. Phase 8 is `PASS / OWNER_ACCEPTED` and Phase 9 is `PASS / EXTERNAL_ASSURANCE_ACCEPTED` for the earlier candidate they covered.

The Phase 10 production decision remains **`NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`**. DTMO is **not production authorized**.

The highest-priority programme is **Phase 11 Platform Industrialisation**. Phase 11.1–11.2 Taranis and Phase 11.3 IntelOwl are `PASS / REPOSITORY_COMPLETE`. The sole active bounded objective is **Phase 11.4 OpenCTI service/API/STIX/data-model/identity/security/licensing contract validation**, currently `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`.

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
| Phase 11.4 contract | `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED` | OpenCTI contract is the active release gate |
| Phase 12 | `NOT STARTED` | New production decision only after integrated validation/assurance |

## Phase 11 strategic architecture

The fixed order remains:

1. Taranis AI — repository-complete;
2. IntelOwl — repository-complete;
3. OpenCTI — active STIX knowledge-graph contract and subsequent adapter work;
4. MISP — consolidated governed exchange;
5. TheHive — incident/case handoff;
6. Cortex only if IntelOwl cannot satisfy a validated need;
7. Kubernetes/Helm/GitOps, HA, secrets, network, observability, recovery and supply-chain hardening;
8. migration/compatibility;
9. new production-equivalent validation and independent external assurance;
10. Phase 12.

The active OpenCTI contract keeps DTMO and OpenCTI identity domains explicit, requires least-privilege non-human access and marking restrictions, preserves STIX identity/provenance/confidence, and excludes automatic connector/MISP/case/publication side effects.

## Key control boundaries

Server-side RBAC, least privilege, human/service separation, privileged-action safeguards, validated trust, provenance/confidence preservation, data minimization, audit/correlation and separate human external-share authority remain mandatory.

IntelOwl enrichment remains attributed context rather than local-compromise proof. OpenCTI graph context follows the same rule: entities, relationships, confidence or graph presence do not establish DTMO-local exposure, compromise, severity or publication authority.

OpenCTI routine integration must not require administrator or `Bypass all capabilities` authority. Unknown markings, malformed STIX and authorization failures fail closed. OpenCTI Community Edition is Apache-2.0; Enterprise Edition is separately licensed and Enterprise-only dependencies require explicit entitlement/legal approval.

Repository CI remains engineering evidence. Prior Phase 8/9 acceptance is not transferable to the materially changed Phase 11 platform.

## Executive recommendation

Continue Phase 11 in the fixed order, one bounded green pull request at a time. Merge the Phase 11.4 OpenCTI contract only after full exact-head CI and Professional Documentation Gate are green. Then begin exactly the read-only OpenCTI STIX/identity adapter with pagination/reconciliation and provenance preservation. Do not enter Phase 11.5 or Phase 12 early.

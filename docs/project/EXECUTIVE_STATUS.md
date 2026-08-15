# DTMO Executive Status

Date: **2026-08-15**  
Software baseline: **16.0.0rc12 plus accepted post-RC13/E8 repository enhancements**

## Management summary

DTMO has an accepted repository-controlled engineering baseline, an owner-accepted functional product and an E8.1–E8.10 `PASS / REPOSITORY_COMPLETE` vulnerability/CTI baseline. Phase 8 is `PASS / OWNER_ACCEPTED` and Phase 9 is `PASS / EXTERNAL_ASSURANCE_ACCEPTED`.

The Phase 10 production decision is **`NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`**. DTMO is not production authorized.

The active and highest-priority programme is **Phase 11 Platform Industrialisation**. It moves generic OSINT collection, enrichment, CTI graph and case-management responsibilities to mature open-source subsystems while retaining DTMO as the education-sector CTI, vulnerability-context, governance and governed-sharing layer. A new Phase 12 production GO/NO-GO will occur only after the integrated platform has new production-equivalent validation and independent external assurance.

## Current decision position

| Decision area | Status | Consequence |
|---|---|---|
| Engineering baseline | `PASS` | Repository foundation accepted |
| Functional product | `PASS / OWNER_ACCEPTED` | Canonical console journey accepted |
| E8 product evolution | `PASS / REPOSITORY_COMPLETE` | Vulnerability/CTI scope accepted in repository |
| Phase 8 | `PASS / OWNER_ACCEPTED` | Historical staging acceptance remains valid for prior candidate |
| Phase 9 | `PASS / EXTERNAL_ASSURANCE_ACCEPTED` | Historical independent assurance remains valid for prior candidate |
| Phase 10 | `NO-GO / BLOCKED` | Production authorization not granted |
| Phase 11 | `IN PROGRESS / ACTIVE` | Platform industrialisation is the only active development priority |
| Phase 12 | `NOT STARTED` | New production decision after integrated validation/assurance |

## Phase 11 strategic architecture

Priority order:

1. Taranis AI — generic OSINT collection, analyst assessment and structured reporting;
2. IntelOwl — IOC enrichment;
3. OpenCTI — STIX knowledge graph;
4. MISP — consolidated governed exchange;
5. TheHive — incident/case handoff;
6. Cortex only if IntelOwl cannot satisfy a validated need;
7. Kubernetes/Helm/GitOps, HA, secrets, observability, recovery and supply-chain hardening;
8. migration/compatibility;
9. new production-equivalent validation and external assurance.

The current bounded objective is Phase 11.1 Taranis architecture and gap assessment.

## Key control boundaries

The platform retains server-side RBAC, least privilege, human/service-account separation, privileged-action safeguards, validated trust, provenance/confidence preservation, data minimization, audit/correlation and separate human review/external-share authority.

Repository CI remains engineering evidence. Prior Phase 8/9 acceptance is not automatically transferable to the materially changed Phase 11 platform. Technical integration does not grant publication authority. Framework mappings do not imply blanket compliance, maturity or certification.

## Executive recommendation

Proceed with Phase 11 in the fixed priority order, one bounded green pull request at a time. Do not expand unrelated UI or generic collector/enrichment features while Phase 11 is active. Do not enter Phase 12 until the integrated platform has completed new production-equivalent validation and independent external assurance.
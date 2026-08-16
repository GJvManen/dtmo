# DTMO Documentation Status and Authority

Last reconciled: **2026-08-16**

## Purpose

This document defines which DTMO documents are authoritative for the current product/lifecycle state, which records are historical/immutable, and how conflicts are resolved.

## Authority order

For current project decisions, use this order:

1. `docs/project/CURRENT_STATE.md` — current controlled product and lifecycle state;
2. `docs/roadmap/PLATFORM_INDUSTRIALISATION_ROADMAP.md` — active Phase 11 programme and fixed priority order;
3. `docs/architecture/OPENCTI_DTMO_INTEGRATION_CONTRACT.md` — accepted Phase 11.4 service/API/STIX/identity/security/licensing contract;
4. `docs/integrations/OPENCTI_INTEGRATION.md` — active OpenCTI adapter/mapping/persistence boundary;
5. `docs/operations/OPENCTI_INTEGRATION_RUNBOOK.md` — active operational ordering, restart and recovery boundary;
6. `docs/qa/PHASE11_4_OPENCTI_PERSISTENCE_GATE.md` — active exact-head acceptance definition;
7. IntelOwl integration documentation — accepted Phase 11.3 boundary;
8. Taranis assessment/contract/adapter documentation — accepted Phase 11.1–11.2 boundary;
9. `docs/roadmap/PRODUCTION_ROADMAP.md` — production-readiness sequence from Phase 10 NO-GO to Phase 12;
10. `docs/project/PRODUCTION_READINESS_REPORT.md` and `PRODUCTION_CHECKLIST.md` — consolidated readiness/evidence completion state;
11. `docs/production/PHASE10_PRODUCTION_GO_NO_GO.md` — completed accountable no-go decision;
12. architecture, security, governance, QA and `docs/evidence/EVIDENCE_INDEX.md` — domain-specific boundaries and evidence classes.

Historical point-in-time records remain valid for what they originally described and are never rewritten to manufacture later acceptance.

## Current documentation baseline

| Document class | Status | Maintenance expectation |
|---|---|---|
| Root README / docs portal | `CURRENT` | Update on material product/lifecycle change |
| Current state / executive views | `CURRENT` | Reconcile together on lifecycle change |
| Platform Industrialisation Roadmap | `CURRENT / ACTIVE` | Maintain through Phase 11 |
| Taranis assessment/contract/adapter docs | `CURRENT / ACCEPTED` | Preserve accepted boundary |
| IntelOwl contract/integration/runbook/user docs | `CURRENT / ACCEPTED` | Preserve repository-complete Phase 11.3 boundary |
| OpenCTI contract | `CURRENT / ACCEPTED` | Preserve accepted Phase 11.4 contract boundary |
| OpenCTI read adapter | `CURRENT / ACCEPTED` | Preserve accepted bounded read-only semantics |
| OpenCTI integration/runbook/persistence gate | `CURRENT / IN EXACT-HEAD VALIDATION` | Active canonical mapping/persistence and operational boundary |
| Production roadmap/readiness/checklist | `CURRENT` | Reconcile together on readiness-gate change |
| Phase 10 decision record | `CURRENT / DECIDED` | Preserve NO-GO decision and successor rationale |
| System architecture | `CURRENT — STABLE DESIGN` | Update for accepted component/trust/data-flow changes |
| Security model | `CURRENT — STABLE CONTROL MODEL` | Update when identity/authorization/security boundaries change |
| Governance mapping registry | `CURRENT — CONTROLLED CLAIM MODEL` | Update when mappings/framework semantics change |
| QA/release gates | `CURRENT — CONTROL MODEL` | Update when gate/evidence rules change |
| Historical phase runbooks/evidence | `HISTORICAL / SUPPORTING` | Never rewrite original evidence claims |
| `docs/development/runs/` | `HISTORICAL / IMMUTABLE` | Never rewrite to simulate current state |

## Current release truth

The professional documentation must consistently distinguish:

- Phases 1–7: `PASS`;
- RC13: `PASS / OWNER_ACCEPTED`;
- E8.1–E8.10: `PASS / REPOSITORY_COMPLETE`;
- Phase 8: `PASS / OWNER_ACCEPTED` for the earlier candidate;
- Phase 9: `PASS / EXTERNAL_ASSURANCE_ACCEPTED` for the earlier candidate;
- Phase 10: `NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`;
- Phase 11: `IN PROGRESS / ACTIVE`;
- Phase 11.1–11.2 Taranis: `PASS / REPOSITORY_COMPLETE`;
- Phase 11.3 IntelOwl: `PASS / REPOSITORY_COMPLETE`;
- Phase 11.4 OpenCTI contract: `PASS / REPOSITORY_COMPLETE`;
- Phase 11.4 OpenCTI read-only adapter: `PASS / REPOSITORY_COMPLETE`;
- Phase 11.4 OpenCTI canonical mapping/persistence: `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`;
- Phase 12: `NOT STARTED`;
- DTMO: **not production authorized**.

## Active Phase 11.4 documentation rule

Documentation may describe repository-implemented OpenCTI read and persistence behavior but must not imply live OpenCTI connectivity, deployed credentials/RBAC/markings, production-scale STIX synchronization, production graph correctness, production-equivalent behavior or an accepted OpenCTI operator UI.

The active documentation preserves these boundaries:

- OpenCTI remains a separate service/API component; no source is vendored;
- Community Edition Apache-2.0 and separate Enterprise Edition licensing are distinguished;
- dedicated non-human least-privilege identity and runtime secrets remain required;
- OpenCTI/STIX and DTMO identity domains stay separate and explicitly mapped;
- mappings and immutable reconciliation revisions preserve markings, confidence, timestamps, external references and provenance;
- conflicting identity drift, malformed data and ambiguous mapping fail closed;
- database constraints keep `external_share_authorized=false` and `local_compromise_proven=false`;
- PostgreSQL commit precedes durable checkpoint advance;
- unchanged replay is idempotent through stable identity and snapshot hashes;
- connector registration, MISP synchronization, enrichment, TheHive case creation, publication, security administration and arbitrary mutation remain excluded;
- graph context does not establish local compromise/exposure or DTMO share/publication authority;
- repository CI is engineering evidence, not live integration or production evidence.

No synthetic screenshot is promoted because this persistence slice introduces no accepted OpenCTI operator GUI surface.

## Evidence and claim rules

Repository CI cannot manufacture staging acceptance; owner acceptance cannot manufacture independent assurance; independent assurance cannot manufacture production authorization. Prior Phase 8/9 evidence remains valid only for the prior candidate. Fresh Phase 11.10 validation and Phase 11.11 independent assurance are required before Phase 12.

Framework mappings, IntelOwl enrichment and OpenCTI graph context remain bounded claims and do not imply blanket compliance, local exposure or compromise without separate attributable evidence.

## Historical / immutable material

Historical documents may contain lifecycle terminology that is no longer current. This is acceptable only where the document is clearly an immutable point-in-time record. Historical text must not be used as the primary current-state source or rewritten to manufacture later acceptance.

## Reconciliation gate

Material documentation changes must satisfy `docs/qa/CURRENT_STATE_RECONCILIATION.md` and professional documentation contract tests before protected merge. Current lifecycle state is reconciled across the root README, documentation portal, current state, executive views, readiness report/checklist, documentation status, evidence index, QA/release gates, production roadmap and active Phase 11 roadmap/integration documents. Historical Phase 8/9 and Phase 10 evidence claims remain preserved in their original scope.

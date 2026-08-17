# DTMO Documentation Status and Authority

Last reconciled: **2026-08-17**

## Purpose

This document defines which DTMO documents are authoritative for the current product/lifecycle state, which records are historical/immutable, and how conflicts are resolved.

## Authority order

For current project decisions, use this order:

1. `docs/project/CURRENT_STATE.md` — current controlled product and lifecycle state;
2. `docs/roadmap/PLATFORM_INDUSTRIALISATION_ROADMAP.md` — active Phase 11 programme and fixed priority order;
3. `docs/architecture/PHASE11_8_RUNTIME_FOUNDATION.md` — active Phase 11.8a runtime architecture/trust boundary;
4. `docs/administration/KUBERNETES_RUNTIME_CONFIGURATION.md` and `docs/operations/PHASE11_8_RUNTIME_FOUNDATION_RUNBOOK.md` — active configuration and operations boundary;
5. `docs/qa/PHASE11_8_RUNTIME_FOUNDATION_GATE.md` — active exact-head acceptance gate;
6. Cortex, TheHive, MISP, OpenCTI, IntelOwl and Taranis architecture/integration/runbook documentation — accepted Phase 11.1–11.7b service boundaries;
7. `docs/roadmap/PRODUCTION_ROADMAP.md` — production-readiness sequence from Phase 10 NO-GO to Phase 12;
8. readiness, security, QA and `docs/evidence/EVIDENCE_INDEX.md` — domain-specific current-state/evidence boundaries;
9. `docs/production/PHASE10_PRODUCTION_GO_NO_GO.md` — completed accountable Phase 10 no-go decision.

Historical point-in-time records remain valid for what they originally described and are never rewritten to manufacture later acceptance.

## Current documentation baseline

| Document class | Status | Maintenance expectation |
|---|---|---|
| Root README / docs portal | `CURRENT` | Update on material product/lifecycle change |
| Current state / executive views | `CURRENT` | Reconcile together on lifecycle change |
| Platform Industrialisation Roadmap | `CURRENT / ACTIVE` | Maintain through Phase 11 |
| Taranis through Cortex accepted docs | `CURRENT / ACCEPTED` | Preserve accepted Phase 11.1–11.7b boundaries |
| Phase 11.8a architecture/configuration/runbook | `CURRENT / IN EXACT-HEAD VALIDATION` | Active bounded runtime foundation |
| Phase 11.8a QA gate | `CURRENT / IN EXACT-HEAD VALIDATION` | Active exact-head acceptance boundary |
| Production roadmap/readiness/checklist | `CURRENT` | Reconcile together on readiness-gate change |
| Phase 10 decision record | `CURRENT / DECIDED` | Preserve NO-GO decision and successor rationale |
| System architecture | `CURRENT — PHASE 11 COMPOSED DESIGN` | Update for accepted component/trust/data-flow changes |
| Security model | `CURRENT — ACTIVE PHASE 11.8 CONTROL BOUNDARY` | Update when identity/authorization/runtime boundaries change |
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
- Phase 11.1–11.7b: `PASS / REPOSITORY_COMPLETE`;
- Phase 11.8a runtime foundation: `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`;
- Phase 11.9 migration/compatibility: `NOT STARTED`;
- Phase 11.10 production-equivalent validation: `NOT STARTED`;
- Phase 11.11 independent external assurance: `NOT STARTED`;
- Phase 12: `NOT STARTED`;
- DTMO: **not production authorized**.

## Active Phase 11.8a documentation rule

Documentation may describe the repository-controlled Helm/GitOps runtime foundation because it exists in the active PR, but must not imply a live accepted cluster, cloud IAM/workload identity, effective secret-provider permissions, production ingress/TLS, CNI enforcement, stateful/multi-zone HA, recovery objectives, centralized observability, supply-chain attestation or production authorization.

The active documentation preserves these boundaries:

- immutable image digest is mandatory;
- Git stores non-secret desired state only;
- runtime secrets are referenced through an existing Secret and remain outside repository evidence;
- pods run non-root with read-only root filesystem, dropped capabilities and no automatic service-account token;
- readiness/liveness probes and resource defaults are explicit;
- application disruption budget is explicit;
- network policy fails closed and external egress requires explicit allowlisting;
- Taranis AI, IntelOwl, Cortex, OpenCTI, MISP and TheHive remain separate service/licensing/identity boundaries;
- Kubernetes placement does not grant publication/share authority or case-handoff authority;
- external platform state does not prove local compromise;
- repository CI remains engineering evidence, not live deployment or production evidence.

No synthetic live-cluster screenshot is promoted because Phase 11.8a has no accepted deployment evidence surface. Mermaid architecture/trust-boundary diagrams are documentation illustrations only.

## Evidence and claim rules

Repository CI cannot manufacture staging acceptance; owner acceptance cannot manufacture independent assurance; independent assurance cannot manufacture production authorization. Prior Phase 8/9 evidence remains valid only for the prior candidate. Fresh Phase 11.10 validation and Phase 11.11 independent assurance are required before Phase 12.

Framework mappings and integrated service state remain bounded claims and do not imply blanket compliance, local exposure, compromise, case necessity or dissemination authority without separate attributable evidence.

## Historical / immutable material

Historical documents may contain lifecycle terminology that is no longer current. This is acceptable only where the document is clearly an immutable point-in-time record. Historical text must not be used as the primary current-state source or rewritten to manufacture later acceptance.

## Reconciliation gate

Material documentation changes must satisfy `docs/qa/CURRENT_STATE_RECONCILIATION.md` and professional documentation contract tests before protected merge. Current lifecycle state is reconciled across the root README, documentation portal, current state, executive views, readiness report/checklist, documentation status, evidence index, QA/release gates, production roadmap and active Phase 11 documents. Historical Phase 8/9 and Phase 10 evidence claims remain preserved in their original scope.
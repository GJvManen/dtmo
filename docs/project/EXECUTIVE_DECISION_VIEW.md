# DTMO Executive Decision View

## Purpose

This document gives accountable decision makers the concise current decision position for DTMO production readiness and the active Phase 11 successor programme.

## Current position

| Decision area | Current state | Decision consequence |
|---|---|---|
| Repository-controlled engineering | `PASS` for Phases 1–7 | Engineering foundation accepted |
| Functional product | `RC13 PASS / OWNER_ACCEPTED` | Canonical product journey accepted |
| E8 vulnerability/CTI product line | `PASS / REPOSITORY_COMPLETE` | Product capabilities repository-complete |
| Phase 8 production-equivalent staging | `PASS / OWNER_ACCEPTED` | Historical staging evidence accepted for prior candidate |
| Phase 9 independent assurance | `PASS / EXTERNAL_ASSURANCE_ACCEPTED` | Historical assurance accepted for prior candidate |
| Phase 10 production authorization | `NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED` | Production authorization not granted |
| Phase 11.1–11.5 | `PASS / REPOSITORY_COMPLETE` | Taranis, IntelOwl, OpenCTI and MISP boundaries accepted |
| Phase 11.6 TheHive contract | `PASS / REPOSITORY_COMPLETE` | Service/API/licensing/authority baseline accepted |
| Phase 11.6 TheHive implementation | `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED` | Current bounded handoff/state gate |
| Phase 11 platform industrialisation | `IN PROGRESS / ACTIVE` | Highest-priority programme |
| Phase 12 production authorization | `NOT STARTED` | New decision only after integrated validation and assurance |

## Decision interpretation

The project has not received a production `GO`. Historical Phase 8 and Phase 9 evidence remains valid only for the candidate it originally covered and cannot be treated as production acceptance of the materially changed Phase 11 platform.

The active engineering decision is whether the bounded TheHive implementation safely realizes the already accepted contract without transferring human authority or inventing deployment evidence.

## Phase 11 required progression

1. **Completed:** Taranis architecture/licensing and canonical adapter.
2. **Completed:** IntelOwl bounded enrichment integration.
3. **Completed:** OpenCTI contract, read adapter and canonical mapping/persistence integration.
4. **Completed:** MISP consolidation contract and authoritative synchronization-state implementation.
5. **Completed:** TheHive service/API/identity/licensing/authority contract.
6. **Active:** minimal human-authorized TheHive case handoff plus durable reservation/reconciliation state.
7. Adopt Cortex only if a validated IntelOwl capability gap remains after Phase 11.6 acceptance.
8. Industrialise the composed runtime with Kubernetes/Helm/GitOps, HA, secrets, network policy, observability, backup/recovery and supply-chain controls.
9. Complete migration/compatibility.
10. Execute new production-equivalent validation.
11. Execute new independent external assurance.
12. Enter Phase 12 for the next formal production GO/NO-GO.

## TheHive decision boundary

TheHive 5.5.16 remains a separate StrangeBee service using public API v1. TheHive 5.3+ requires an activated Community, Gold or Platinum license for continued write functionality; live entitlement is deployment evidence, not a CI assumption.

The implementation permits only explicit human-authorized `POST /api/v1/case`. `handoff:case` is distinct from share/publication approval and service accounts cannot authorize it. DTMO commits durable request/item/principal/organization state before external mutation. Stable returned case identity is required for `delivered`; uncertain delivery becomes `ambiguous` and blocks blind replay.

TLP/PAP handling fails closed. A requested TLP cannot broaden a known authoritative TLP tag. Authoritative MISP distribution/sharing-group restrictions currently block handoff because no deployment-approved TheHive access-membership mapping exists. DTMO does not infer one.

TheHive case lifecycle is not canonical CTI truth, local-compromise proof or DTMO share authority. Responders, task/observable creation, Cortex execution, automatic MISP→TheHive automation, case deletion, external sharing and administration remain excluded.

## Decision rules

- Green CI is repository engineering evidence, not production authorization.
- Historical Phase 8/9 evidence remains deployment/candidate-bound.
- Service-to-service integrations preserve provenance, least privilege and applicable licensing boundaries.
- Technical connectivity or platform permissions do not grant DTMO publication/share or case-handoff authority.
- Source handling restrictions cannot be broadened by handoff or re-export.
- Missing, conflicting or inaccessible mandatory evidence fails closed.

## Current decision

**Phase 10 remains `NO-GO / BLOCKED`. Phase 11.1–11.5 and the Phase 11.6 TheHive contract are `PASS / REPOSITORY_COMPLETE`. The bounded Phase 11.6 TheHive handoff implementation is the active exact-head gate. DTMO remains not production authorized; Phase 12 starts only after Phase 11.10/11.11 evidence is accepted.**

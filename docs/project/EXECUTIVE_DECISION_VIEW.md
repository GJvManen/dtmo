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
| Phase 11.6 TheHive handoff contract | `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED` | Current bounded contract gate |
| Phase 11 platform industrialisation | `IN PROGRESS / ACTIVE` | Highest-priority programme |
| Phase 12 production authorization | `NOT STARTED` | New decision only after integrated validation and assurance |

## Decision interpretation

The project has not received a production `GO`. Historical Phase 8 and Phase 9 evidence remains valid only for the candidate it originally covered and cannot be treated as production acceptance of the materially changed Phase 11 platform.

The active engineering decision is whether the bounded Phase 11.6 TheHive contract safely defines service/API/licensing, case identity, TLP/PAP/access, human case-handoff authority and mutation replay behavior before any runtime case creation is introduced.

## Phase 11 required progression

1. **Completed:** Taranis architecture/licensing and canonical adapter.
2. **Completed:** IntelOwl bounded enrichment integration.
3. **Completed:** OpenCTI contract, read adapter and canonical mapping/persistence integration.
4. **Completed:** MISP consolidation contract and authoritative synchronization-state implementation.
5. **Active:** TheHive incident/case handoff contract; runtime mutation remains excluded.
6. Implement the minimal human-authorized TheHive handoff only after the contract is protected-merged.
7. Adopt Cortex only if a validated IntelOwl capability gap remains.
8. Industrialise the composed runtime with Kubernetes/Helm/GitOps, HA, secrets, network policy, observability, backup/recovery and supply-chain controls.
9. Complete migration/compatibility.
10. Execute new production-equivalent validation.
11. Execute new independent external assurance.
12. Enter Phase 12 for the next formal production GO/NO-GO.

## TheHive decision boundary

TheHive 5.5.16 remains a separate StrangeBee service using public API v1. TheHive 5.3+ requires an activated Community, Gold or Platinum license for continued write functionality; live entitlement is deployment evidence, not a CI assumption.

`POST /api/v1/case` is a mutation candidate only after explicit human-authorized DTMO case handoff. A later implementation must persist stable DTMO canonical identity, handoff/idempotency identity, TheHive case identity and organization context; ambiguous delivery must block blind replay. Mutable title/tag/assignee fields are not identity.

TLP/PAP/access mapping may not broaden authoritative source restrictions. TheHive case lifecycle is not canonical CTI truth, local-compromise proof or DTMO share authority. Responders, Cortex execution, automatic MISP→TheHive automation, external sharing and administration remain excluded.

## Decision rules

- Green CI is repository engineering evidence, not production authorization.
- Historical Phase 8/9 evidence remains deployment/candidate-bound.
- Service-to-service integrations preserve provenance, least privilege and applicable licensing boundaries.
- Technical connectivity or platform permissions do not grant DTMO publication/share or case-handoff authority.
- Source handling restrictions cannot be broadened by handoff or re-export.
- Missing, conflicting or inaccessible mandatory evidence fails closed.

## Current decision

**Phase 10 remains `NO-GO / BLOCKED`. Phase 11.1–11.5 are `PASS / REPOSITORY_COMPLETE`. Phase 11.6 TheHive handoff-contract exact-head validation is the active bounded gate. DTMO remains not production authorized; Phase 12 starts only after Phase 11.10/11.11 evidence is accepted.**

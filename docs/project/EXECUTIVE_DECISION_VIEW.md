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
| Phase 11.1–11.2 Taranis | `PASS / REPOSITORY_COMPLETE` | Service boundary and canonical adapter accepted |
| Phase 11.3 IntelOwl | `PASS / REPOSITORY_COMPLETE` | Enrichment integration accepted |
| Phase 11.4 OpenCTI | `PASS / REPOSITORY_COMPLETE` | Contract, read adapter and persistence accepted |
| Phase 11.5 MISP consolidation contract | `PASS / REPOSITORY_COMPLETE` | MISP service/API/licensing/authority model accepted |
| Phase 11.5 MISP synchronization state/persistence | `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED` | Current bounded implementation gate |
| Phase 11 platform industrialisation | `IN PROGRESS / ACTIVE` | Highest-priority programme |
| Phase 12 production authorization | `NOT STARTED` | New decision only after integrated validation and assurance |

## Decision interpretation

The project has not received a production `GO`. Phase 11 continues to industrialise the platform before a new authorization attempt.

Historical Phase 8 and Phase 9 evidence remains valid only for the candidate it originally covered and cannot be treated as production acceptance of the materially changed Phase 11 platform.

The active engineering decision is whether the bounded Phase 11.5 MISP persistence implementation correctly binds stable MISP event identity and authoritative source restrictions to canonical DTMO state without creating publication authority or a second MISP synchronization path.

## Phase 11 required progression

1. **Completed:** Taranis architecture/licensing and canonical adapter.
2. **Completed:** IntelOwl bounded enrichment integration.
3. **Completed:** OpenCTI contract, read adapter and canonical mapping/persistence integration.
4. **Contract completed; implementation active:** MISP synchronization-state/persistence and authority enforcement.
5. Add TheHive incident/case handoff only after Phase 11.5 repository completion.
6. Adopt Cortex only if a validated IntelOwl capability gap remains.
7. Industrialise the composed runtime with Kubernetes/Helm/GitOps, HA, secrets, network policy, observability, backup/recovery and supply-chain controls.
8. Complete migration/compatibility.
9. Execute new production-equivalent validation.
10. Execute new independent external assurance.
11. Enter Phase 12 for the next formal production GO/NO-GO.

## MISP decision boundary

MISP v2.5.44 remains a separate AGPL-3.0 service/API. The accepted contract preserves MISP UUID identity, distribution, sharing-group and TLP/tag restrictions; human DTMO review/share approval for outbound sharing; deterministic replay protection; unpublished `events/add` destination events; and fail-closed reconciliation after uncertain delivery.

The active implementation adds `misp_synchronization_state`, maps one stable MISP event UUID to one DTMO canonical item, persists the authoritative source restriction envelope and projects it to canonical `metadata_json.misp_restrictions` in the same database transaction as canonical ingestion. Identity collision/drift, malformed or incomplete restrictions and attempted inbound external-share authority fail closed.

Service accounts, connectors, schedulers, IntelOwl, OpenCTI and MISP itself cannot grant DTMO share approval. Automatic MISP federation, automatic publication and OpenCTI↔MISP synchronization remain outside the boundary.

## Decision rules

- Green CI is repository engineering evidence, not production authorization.
- Historical Phase 8/9 evidence remains deployment/candidate-bound.
- Service-to-service integrations preserve provenance, least privilege and applicable licensing boundaries.
- Technical connectivity or platform permissions do not grant DTMO publication/share authority.
- Source handling restrictions cannot be broadened by re-export.
- Missing, conflicting or inaccessible mandatory evidence fails closed.

## Current decision

**Phase 10 remains `NO-GO / BLOCKED`. Phase 11.1–11.4 and the Phase 11.5 MISP contract are `PASS / REPOSITORY_COMPLETE`. Phase 11.5 MISP synchronization-state/persistence exact-head validation is the active bounded gate. DTMO remains not production authorized; Phase 12 starts only after Phase 11.10/11.11 evidence is accepted.**

# DTMO Executive Decision View

## Purpose

This document gives accountable decision makers the concise current decision position for DTMO production readiness and the active successor programme.

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
| Phase 11.4 OpenCTI contract | `PASS / REPOSITORY_COMPLETE` | Service/API/STIX/licensing boundary accepted |
| Phase 11.4 OpenCTI read adapter | `PASS / REPOSITORY_COMPLETE` | Bounded GraphQL/STIX adapter accepted |
| Phase 11.4 OpenCTI persistence | `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED` | Current final repository gate for Phase 11.4 |
| Phase 11 platform industrialisation | `IN PROGRESS / ACTIVE` | Highest-priority programme |
| Phase 12 production authorization | `NOT STARTED` | New decision only after integrated validation and assurance |

## Decision interpretation

The project has not received a production `GO`. The accountable decision remains to industrialise the platform before a new authorization attempt.

Historical functional, Phase 8 and Phase 9 evidence remains valid only for the candidate it originally covered. Because Phase 11 materially changes the architecture, that evidence cannot be treated as production acceptance of the future integrated platform.

The active engineering decision is whether the final bounded Phase 11.4 canonical OpenCTI mapping/persistence and operational integration satisfy exact-head code, migration, security, evidence and documentation gates. No live OpenCTI or production claim follows from repository acceptance.

## Phase 11 required progression

1. **Completed:** Taranis AI architecture/API/data-model/identity/licensing and canonical adapter.
2. **Completed:** IntelOwl contract, bounded adapter and governed execution/persistence.
3. **Active:** finish OpenCTI canonical mapping/persistence and operational integration after the accepted contract and read adapter.
4. Consolidate MISP inbound/outbound authority and synchronization.
5. Add TheHive incident/case handoff.
6. Adopt Cortex only if a documented IntelOwl capability gap remains.
7. Industrialise the composed runtime with Kubernetes/Helm/GitOps, HA, secrets, network policy, observability, backup/recovery and supply-chain controls.
8. Complete migration/compatibility.
9. Execute new production-equivalent validation.
10. Execute new independent external assurance.
11. Enter Phase 12 for the next formal production GO/NO-GO.

## OpenCTI decision boundary

The active persistence slice preserves:

- separate OpenCTI service/API integration rather than source vendoring;
- dedicated least-privilege service identity and runtime-secret bearer token;
- stable DTMO item, OpenCTI internal and STIX identity domains;
- immutable SHA-256-keyed reconciliation snapshots;
- marking, confidence, timestamp, external-reference and provenance retention;
- fail-closed conflicting identity drift and ambiguous mapping;
- database-enforced no-share/no-local-compromise invariants;
- PostgreSQL commit before durable checkpoint advance;
- idempotent replay if checkpoint replacement fails after successful persistence;
- no OpenCTI connectors, MISP synchronization, enrichment, TheHive case creation, publication, security administration or arbitrary mutation;
- OpenCTI graph context treated as evidence/context, not local-compromise proof or dissemination authority;
- Community Edition Apache-2.0 versus separately licensed Enterprise Edition boundary.

## Decision rules

- Green CI is repository engineering evidence, not production authorization.
- Historical Phase 8/9 evidence remains deployment/candidate-bound.
- A material integrated-platform change requires fresh validation and assurance.
- Framework mappings do not imply blanket compliance or maturity.
- Technical administration, collectors, publishers, enrichment engines or graph integrations do not grant publication/share authority.
- Missing or inaccessible mandatory evidence is not implicit acceptance.
- Service-to-service integrations must preserve provenance, classification and least privilege.
- Taranis source remains outside the DTMO repository under the accepted service boundary.
- IntelOwl/pyIntelOwl and OpenCTI remain separate services under their applicable licensing boundaries.

## Principal decision inputs

Decision makers should use `CURRENT_STATE.md`, the Platform Industrialisation Roadmap, the OpenCTI integration contract/implementation/runbook, the OpenCTI persistence gate, Production Readiness Report, Production Checklist, Production Roadmap, Evidence Index and Security Overview. Immutable run/CI evidence remains separate from these stable decision documents.

## Current decision

**Phase 10 remains `NO-GO / BLOCKED`. Phase 11.1–11.3 are repository-complete. The Phase 11.4 OpenCTI contract and read adapter are repository-complete; canonical mapping/persistence + operational integration is the active exact-head gate. DTMO remains not production authorized; Phase 12 is the next production authorization gate only after Phase 11.10/11.11 evidence is accepted.**

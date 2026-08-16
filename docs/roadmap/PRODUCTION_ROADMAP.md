# DTMO Roadmap — Production Readiness and Product Evolution

Last updated: **2026-08-16**

## Purpose

This roadmap separates production authorization from product evolution and platform industrialisation. Repository engineering, accountable acceptance, external staging evidence, independent assurance and production authorization remain distinct evidence classes.

## Current position

| Stage | Scope | Status |
|---|---|---|
| Phases 1–7 | Repository-controlled engineering baseline | `PASS` |
| RC13 + owner retest | Unified-console functional acceptance | `PASS / OWNER_ACCEPTED` |
| E8.1–E8.10 | Vulnerability & CTI ecosystem integrations | `PASS / REPOSITORY_COMPLETE` |
| Phase 8 | Production-equivalent validation and accountable acceptance | `PASS / OWNER_ACCEPTED` |
| Phase 9 | Independent external assurance | `PASS / EXTERNAL_ASSURANCE_ACCEPTED` |
| Phase 10 | Formal production go/no-go | `NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED` |
| Phase 11.1 | Taranis architecture/API/licensing | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.2 | Taranis→DTMO canonical adapter | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.3 | IntelOwl enrichment integration | `IN PROGRESS / CONTRACT BASELINE IN EXACT-HEAD VALIDATION` |
| Phase 12 | New formal production go/no-go for integrated platform | `NOT STARTED` |

DTMO remains **not production authorized**. Phase 10 concluded with a no-go decision and Phase 11 is the highest-priority programme.

# Track A — Accepted historical readiness evidence

## Phase 8 — production-equivalent staging acceptance

**Status:** `PASS / OWNER_ACCEPTED`

The accepted Phase 8 evidence remains historical evidence for the candidate it covered. It is not reused as acceptance of a materially changed Phase 11 integrated platform.

## Phase 9 — independent external assurance

**Status:** `PASS / EXTERNAL_ASSURANCE_ACCEPTED`

The accepted Phase 9 assurance remains historical evidence for the candidate it covered. It is not reused as assurance of a materially changed Phase 11 integrated platform.

## Phase 10 — production go/no-go

**Status:** `NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`

The accountable decision is recorded in `docs/production/PHASE10_PRODUCTION_GO_NO_GO.md`. Production authorization was not granted.

# Track B — Phase 11 platform industrialisation

**Status:** `IN PROGRESS / ACTIVE`

The authoritative detailed programme is `docs/roadmap/PLATFORM_INDUSTRIALISATION_ROADMAP.md`.

The fixed priority order is:

1. Taranis AI architecture and gap assessment;
2. Taranis → DTMO canonical adapter;
3. IntelOwl enrichment integration;
4. OpenCTI knowledge-graph integration;
5. MISP consolidation;
6. TheHive incident/case handoff;
7. Cortex decision only if IntelOwl is insufficient for a validated requirement;
8. Kubernetes/Helm/GitOps and platform hardening;
9. migration and compatibility;
10. new production-equivalent validation;
11. new independent external assurance.

## Phase 11.1 — Taranis AI architecture and gap assessment

**Status:** `PASS / REPOSITORY_COMPLETE`

The accepted Phase 11.1 assessment and service-to-service contract define the read-only API surface, source/news/story/CTI mappings, stable identity, authentication/service-account boundary, provenance/TLP transformation, polling/reconciliation behavior, licensing boundary and abuse cases. Taranis source code is not vendored into DTMO.

See:

- `docs/architecture/TARANIS_PLATFORM_INTEGRATION_ASSESSMENT.md`;
- `docs/architecture/TARANIS_DTMO_INTEGRATION_CONTRACT.md`.

## Phase 11.2 — Taranis → DTMO canonical adapter

**Status:** `PASS / REPOSITORY_COMPLETE`

Repository implementation covers read-only collection, deterministic canonical IDs, fail-closed handling, durable checkpointing, bounded pagination/reconciliation, bounded detail/CTI retrieval, canonical persistence/indexing, connector alerting and governed scheduler/manual execution using the existing `MANAGE_CONNECTORS` permission. No Taranis publisher/share capability becomes DTMO external-sharing authority.

The authoritative implementation guide is `docs/integrations/TARANIS_ADAPTER.md`.

This repository status is not live composed-platform evidence. Production-equivalent validation remains a Phase 11.10 evidence class and historical Phase 8/9 evidence is not reused for the materially changed candidate.

## Phase 11.3 — IntelOwl enrichment integration

**Status:** `IN PROGRESS / CONTRACT BASELINE IN EXACT-HEAD VALIDATION`

The active bounded gate is acceptance of `docs/architecture/INTELOWL_DTMO_INTEGRATION_CONTRACT.md`. The contract establishes the IntelOwl v6.7-compatible service/API boundary, non-admin service identity, runtime-secret token, TLS verification, explicit observable/analyzer allowlists, TLP/privacy rules, bounded job/rate-limit behavior, analyzer/job/result provenance, partial-failure semantics, exclusion of external IntelOwl Connector side effects and the AGPL-3.0 service boundary.

The companion design guide is `docs/integrations/INTELOWL_INTEGRATION.md`. It is explicitly contract-only and does not claim a live adapter.

After the contract passes fully green exact-head CI and professional documentation gates, the next bounded PR is the IntelOwl enrichment adapter implementation. OpenCTI does not start before that adapter slice is accepted.

## Phase 11.4–11.11

Subsequent phases execute one bounded objective at a time in the priority order defined above. No later phase may silently bypass red exact-head CI, unresolved licensing/security blockers or a required external evidence gate.

# Track C — Phase 12 production authorization

## Phase 12 — formal production go/no-go

**Status:** `NOT STARTED`

Phase 12 begins only after the integrated Phase 11 candidate has:

- passed production-equivalent validation against one immutable deployment identity;
- completed independent external assurance against that same integrated candidate;
- closed or formally dispositioned release blockers;
- obtained production environment/owner/support, IAM/secrets/network, backup/recovery/rollback, monitoring/on-call/IR, privacy/legal/governance and change authorization.

Phase 12 is fail-closed. A `GO` applies only to the explicitly approved immutable integrated release identity.

# Product and platform boundary

DTMO's differentiating scope remains:

- education-sector CTI and decision support;
- vulnerability prioritization and context;
- provenance and canonical evidence semantics;
- explicit governance/framework relationships;
- governed Administration/RBAC;
- human-controlled external-sharing authority.

Generic collection, IOC enrichment, CTI graph, case management and report-publishing capabilities should be integrated from mature open-source projects where practical rather than rebuilt inside DTMO.

# Delivery and documentation discipline

Each material change requires one bounded pull request with a primary objective, explicit acceptance criteria, exact-head CI where applicable, architecture/security/evidence boundaries and professional documentation updates. A code/integration PR is not mergeable if its affected current-state, architecture, integration, security, QA/evidence, roadmap or user/admin documentation is stale.
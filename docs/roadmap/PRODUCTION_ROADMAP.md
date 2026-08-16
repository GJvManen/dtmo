# DTMO Roadmap — Production Readiness and Product Evolution

Last updated: **2026-08-16**

## Purpose

This roadmap separates production authorization from product evolution and platform industrialisation. Repository engineering, accountable acceptance, deployment-bound validation, independent assurance and production authorization remain distinct evidence classes.

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
| Phase 11.3 | IntelOwl enrichment integration | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.4 contract | OpenCTI service/API/STIX/identity/security/licensing | `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED` |
| Phase 12 | New formal production go/no-go for integrated platform | `NOT STARTED` |

DTMO remains **not production authorized**. Phase 10 concluded with a no-go decision and Phase 11 is the highest-priority programme.

## Historical readiness evidence

Phase 8 remains `PASS / OWNER_ACCEPTED` and Phase 9 remains `PASS / EXTERNAL_ASSURANCE_ACCEPTED` for the earlier candidate they actually covered. Those claims are preserved as historical evidence and are not transferred to the materially changed Phase 11 platform.

Phase 10 remains `NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`; production authorization was not granted.

## Phase 11 platform industrialisation

The authoritative detailed programme is `docs/roadmap/PLATFORM_INDUSTRIALISATION_ROADMAP.md` and the fixed order remains Taranis → IntelOwl → OpenCTI → MISP → TheHive → conditional Cortex → integrated runtime → migration/compatibility → new validation → new assurance.

### Phase 11.1–11.2 — Taranis

**Status:** `PASS / REPOSITORY_COMPLETE`

Accepted scope includes the Taranis service-to-service architecture/licensing contract plus read-only canonical collection, durable checkpointing/reconciliation, bounded detail/CTI retrieval, governed execution, canonical persistence/indexing and observability. Taranis source is not vendored into DTMO.

### Phase 11.3 — IntelOwl

**Status:** `PASS / REPOSITORY_COMPLETE`

Accepted scope includes the service/API/security/licensing contract, bounded policy-enforced enrichment adapter, human `REVIEW_INTELLIGENCE` execution boundary, durable immutable enrichment history and read-only history access. IntelOwl remains a separate AGPL-3.0 service. Analyzer results never grant DTMO publication/share authority and never constitute local-compromise proof by themselves.

### Phase 11.4 — OpenCTI

**Status:** `IN PROGRESS / CONTRACT IN EXACT-HEAD VALIDATION`

The active bounded contract establishes:

- OpenCTI `7.260811.0` as the reviewed compatibility baseline;
- Community Edition Apache-2.0 and separately licensed Enterprise Edition boundaries;
- separate service/API consumption with no OpenCTI source vendoring;
- bounded GraphQL, STIX 2.1, TAXII 2.1 and access-controlled stream interfaces;
- dedicated non-human least-privilege identity and runtime-secret handling;
- explicit OpenCTI/STIX ↔ DTMO canonical identity mapping;
- marking/TLP/PAP, confidence and provenance preservation;
- fail-closed behavior for authorization failures, unknown markings and malformed/unsupported STIX;
- durable restart-safe pagination/stream reconciliation requirements;
- exclusion of connector registration, MISP synchronization, enrichment, case creation and report-publication side effects;
- preservation of DTMO human publication/share authority and no-local-compromise semantics.

After this contract is fully green and protected-merged, the next bounded Phase 11.4 PR is a **read-only OpenCTI STIX/identity adapter with pagination/reconciliation and provenance preservation**.

### Phase 11.5–11.11

Subsequent phases remain blocked by the fixed order. They cover MISP consolidation, TheHive handoff, the conditional Cortex decision, Kubernetes/Helm/GitOps and platform hardening, migration/compatibility, new production-equivalent validation and new independent external assurance.

## Phase 12 — formal production GO/NO-GO

**Status:** `NOT STARTED`

Phase 12 starts only after one immutable integrated Phase 11 candidate has accepted Phase 11.10 production-equivalent validation and Phase 11.11 independent external assurance, plus the required production ownership/IAM/secrets/network/recovery/monitoring/privacy/legal/change approvals.

Phase 12 is fail-closed. A `GO` applies only to the explicitly approved immutable integrated release identity.

## Product and platform boundary

DTMO remains the education-sector CTI and decision-support layer with vulnerability context, provenance, canonical evidence semantics, explicit governance/framework relationships, governed Administration/RBAC and human-controlled external-sharing authority. Generic collection, IOC enrichment, CTI graph and case-management functions are integrated from mature projects instead of duplicated inside DTMO.

## Delivery and documentation discipline

Each material change requires one bounded pull request with explicit acceptance criteria, exact-head CI, expected-head protection, architecture/security/licensing/evidence boundaries and synchronized professional documentation. A code/integration PR is not mergeable if affected current-state, architecture, integration, security, QA/evidence, roadmap or user/admin documentation is stale.

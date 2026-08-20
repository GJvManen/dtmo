# DTMO Platform Industrialisation Roadmap

Last updated: **2026-08-20**  
Programme state: **`ACTIVE / HIGHEST PRIORITY`**

## Purpose

Phase 10 concluded with `NO-GO / BLOCKED` for production authorization. Phase 11 is the successor industrialisation programme and is executed one bounded pull request at a time. Historical Phase 8/9 evidence remains candidate-bound and is not reused for the materially changed integrated platform.

DTMO prefers mature service integrations over rebuilding generic collection, enrichment, graph, exchange and case-management platforms inside DTMO.

## Fixed priority order

1. 11.1 Taranis AI architecture/API/data-model/identity/licensing assessment.
2. 11.2 Taranis → DTMO canonical adapter.
3. 11.3 IntelOwl enrichment integration.
4. 11.4 OpenCTI STIX knowledge-graph integration.
5. 11.5 MISP consolidation and authoritative governed sharing model.
6. 11.6 TheHive incident/case handoff.
7. 11.7 Cortex conditional decision gate.
8. 11.7b owner-required Cortex analyzer connector.
9. 11.8 Kubernetes/Helm/GitOps plus HA/secrets/network/observability/recovery/supply-chain/capacity/upgrade hardening.
10. 11.9 migration/compatibility.
11. 11.10 new production-equivalent validation.
12. 11.11 new independent external assurance.
13. Phase 12 formal production GO/NO-GO.

## Phase 11 — Platform industrialisation

### 11.1–11.2 Taranis AI
**Status:** `PASS / REPOSITORY_COMPLETE`

### 11.3 IntelOwl enrichment integration
**Status:** `PASS / REPOSITORY_COMPLETE`

### 11.4 OpenCTI knowledge-graph integration
**Status:** `PASS / REPOSITORY_COMPLETE`

### 11.5 MISP consolidation
**Status:** `PASS / REPOSITORY_COMPLETE`

### 11.6 TheHive incident/case handoff
**Status:** `PASS / REPOSITORY_COMPLETE`

### 11.7 Cortex decision gate
**Status:** `PASS / REPOSITORY_COMPLETE — HISTORICAL DECISION BASELINE`

### 11.7b Cortex analyzer connector
**Status:** `PASS / REPOSITORY_COMPLETE`

### 11.8 Integrated runtime industrialisation
**Status:** `PASS / REPOSITORY_COMPLETE`

Phase 11.8 was delivered as bounded sub-slices with exact-head repository evidence and professional documentation.

#### 11.8a Runtime foundation
**Status:** `PASS / REPOSITORY_COMPLETE`

#### 11.8b Workload identity and external secret delivery
**Status:** `PASS / REPOSITORY_COMPLETE`

#### 11.8c Ingress/TLS and network segmentation
**Status:** `PASS / REPOSITORY_COMPLETE`

#### 11.8d HA and disruption hardening
**Status:** `PASS / REPOSITORY_COMPLETE`

#### 11.8e Observability hardening
**Status:** `PASS / REPOSITORY_COMPLETE`

#### 11.8f Backup, restore and recovery hardening
**Status:** `PASS / REPOSITORY_COMPLETE`

#### 11.8g Software supply-chain hardening
**Status:** `PASS / REPOSITORY_COMPLETE`

#### 11.8h Capacity and resource planning
**Status:** `PASS / REPOSITORY_COMPLETE`

#### 11.8i Exercised upgrade and rollback
**Status:** `PASS / REPOSITORY_COMPLETE`

Accepted repository evidence requires immutable baseline/candidate/rollback digests, safe RollingUpdate controls, revision history, finite progress/min-ready bounds, mandatory post-upgrade/post-rollback health evidence and restoration of the exact prior digest. Automatic database down migration remains forbidden. Repository acceptance does not prove a live-cluster rollback, stateful recovery, production-equivalent continuity or production authorization.

### 11.9 Migration and compatibility
**Status:** `PASS / REPOSITORY_COMPLETE`

The accepted repository slice validates one connected single-root/single-head Alembic revision graph, explicit upgrade/downgrade contracts and forward-first deployment sequencing. Rolling overlap is allowed only for backward-compatible schema changes. Destructive changes require an explicit expand/migrate/contract sequence. Application rollback never implies automatic database down migration; ambiguity fails closed.

Repository acceptance establishes engineering graph/contract integrity only. It does not prove migration of production data, live application/schema compatibility, production-equivalent continuity, independent assurance or production authorization.

### 11.10 Integrated production-equivalent validation
**Status:** `IN PROGRESS / FRESH CANDIDATE-BOUND EVIDENCE REQUIRED`

The active bounded slice defines and validates the evidence contract for a new production-equivalent exercise against one immutable integrated deployment identity. Acceptance requires fresh migration/compatibility, upgrade, rollback, health, saturation and recovery evidence, all attributable to the same candidate and environment. Historical Phase 8/9 evidence is audit history only and cannot satisfy this gate. Missing, ambiguous, mixed-candidate or inaccessible evidence fails closed.

Repository CI can validate the Phase 11.10 contract and exact-head binding, but repository-green status does not prove that a production-equivalent environment was deployed or exercised. Operational Phase 11.10 acceptance therefore remains separate from repository merge and is required before Phase 11.11.

### 11.11 Independent external assurance
**Status:** `NOT STARTED`

Run fresh independent assurance against the same immutable integrated candidate only after Phase 11.10 production-equivalent evidence is complete and accepted.

## Phase 12 — Production GO/NO-GO
**Status:** `NOT STARTED`

A `GO` requires accepted 11.10 and 11.11 evidence for the same immutable integrated release identity plus accountable production ownership, residual-risk, change/support and rollback authority. Missing evidence remains fail-closed.

## Delivery discipline

Every bounded PR requires one primary objective, exact-head CI, expected-head merge protection, professional documentation synchronization, explicit security/licensing/evidence boundaries and one declared next priority. A code/integration PR does not merge when required documentation is missing or stale.

## Immediate sequence

1. Complete **Phase 11.10 integrated production-equivalent validation** for one immutable candidate using the full fresh evidence set; repository CI alone is insufficient for operational acceptance.
2. Run **Phase 11.11 independent external assurance** against that same immutable integrated candidate only after 11.10 acceptance.
3. Enter Phase 12 only after both 11.10 and 11.11 are accepted for the same candidate.

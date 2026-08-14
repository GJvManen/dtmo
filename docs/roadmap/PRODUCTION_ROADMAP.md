# DTMO Roadmap — Production Readiness and Product Evolution

Last updated: **2026-08-14**

## Purpose

This roadmap separates two complementary tracks:

1. **Production readiness** — the formal evidence path from accepted engineering/product baseline to production approval.
2. **Product evolution** — bounded enhancements that improve the operator experience and governance model without conflating feature development with staging/assurance evidence.

## Current position

| Stage | Scope | Status |
|---|---|---|
| Phases 1–7 | Repository-controlled engineering baseline | `PASS` |
| RC13 + post-RC13 functional owner retest | Unified-console/product acceptance | `PASS / OWNER_ACCEPTED` |
| Phase 8.1 | Real staging environment + immutable deployment identity | `PASS / OWNER_VERIFIED_EXTERNAL_EVIDENCE` |
| Phase 8.2–8.5 | Deployed staging validation and accountable staging acceptance | `IN PROGRESS / NEXT` |
| Phase 9 | Independent external assurance | `NOT COMPLETE` |
| Phase 10 | Formal production go/no-go | `NOT STARTED` |

DTMO is **not production ready**.

# Track A — Production readiness

## Phase 8 — real staging acceptance

### Phase 8.1 — environment and immutable deployment identity

**Status:** `PASS / OWNER_VERIFIED_EXTERNAL_EVIDENCE`

The accountable project owner has checked and verified the real staging deployment identity and the required environment evidence. Environment-specific identifiers and sensitive infrastructure values remain governed by their approved external evidence location and are not reconstructed from repository placeholders.

The accepted evidence scope covers environment identity/ownership, approved access path, exact deployed release/commit, immutable image identities, runtime inventory, configuration parity/deviations, least-privilege identities and secret handling, TLS/network/data controls, no-production-credential reuse, change/rollback records and deployment-time security review.

### Phase 8.2 — platform and identity validation

**Status:** `NEXT ACTIVE OBJECTIVE`

Validate against the same verified immutable staging identity:

- application health/readiness;
- database migrations/connectivity;
- search/cache/object storage;
- authentication/authorization;
- service-account/human separation;
- privileged Administration controls;
- audit/correlation behavior;
- operational metrics and separately authenticated Grafana.

### Phase 8.3 — source-to-intelligence validation

Validate against the same staging identity:

- source catalog/bootstrap;
- source activation/execution;
- upstream fetch;
- raw evidence retention;
- normalization/provenance;
- canonical PostgreSQL commit;
- OpenSearch indexing/search;
- Intelligence visibility;
- Overview/dashboard aggregation;
- Visual Analytics.

### Phase 8.4 — operational and recovery validation

Validate:

- operational metrics/alerts;
- logging/correlation;
- runbook applicability;
- agreed backup/restore/recovery scenarios;
- rollback readiness;
- change/deployment traceability.

### Phase 8.5 — accountable staging acceptance

Phase 8 is complete only after the full deployed-environment evidence package is reviewable and an accountable staging/project acceptance decision is recorded.

## Phase 9 — independent external assurance

Expected assurance classes:

- independent penetration testing;
- representative production-equivalent load/stress validation;
- hardening/configuration review;
- IAM/secrets-management review;
- resilience/recovery review where required;
- monitoring/incident-response readiness review;
- privacy/legal/governance review where required;
- residual-risk disposition.

## Phase 10 — formal production go/no-go

Required decision inputs:

- accepted Phase 8 evidence;
- accepted Phase 9 assurance;
- production environment/ownership model;
- IAM/secrets/network approval;
- backup/recovery/rollback approval;
- monitoring/on-call/escalation approval;
- privacy/data/legal approval;
- open finding/residual-risk statement;
- formal change/release decision.

# Track B — Product evolution

The accepted post-RC13 enhancement baseline now includes:

- shared accessible severity semantics and filters across Overview and Intelligence;
- governed manual source onboarding;
- configurable analytics trends and richer native analytics;
- versioned framework governance and explicit provenance-backed DTMO control crosswalks;
- deeper Administration/RBAC management;
- deeper Governance framework/control evidence and drill-down;
- accepted contrast/usability repairs for recent intelligence and Governance mapping visibility.

Further product evolution may continue as a separate bounded backlog, but it no longer replaces the active Phase 8 production-readiness work.

# Delivery discipline

Each further change is implemented as a bounded PR with explicit acceptance criteria, focused tests, preservation of accepted behavior and governance boundaries, complete exact-head CI before merge, and staging validation when the change affects the deployed Phase 8 candidate.

## Documentation discipline

Professional product, architecture, security, governance and readiness documents describe stable capabilities and controlled current state. Operational PR/incident chronology belongs in development run records, issues and CI evidence.

## Immediate next steps

1. Execute **Phase 8.2 platform and identity validation** against the same owner-verified staging deployment identity.
2. Preserve evidence binding to that identity; do not mix later redeployments without a new identity/evidence record.
3. Continue to Phase 8.3 and Phase 8.4 only after the Phase 8.2 evidence is coherent.
4. Record accountable Phase 8.5 staging acceptance before entering Phase 9 independent assurance.

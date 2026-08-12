# DTMO Roadmap — Production Readiness and Product Evolution

Last updated: **2026-08-12**

## Purpose

This roadmap separates two complementary tracks:

1. **Production readiness** — the formal evidence path from accepted engineering/product baseline to production approval.
2. **Product evolution** — bounded enhancements that improve the operator experience and governance model without conflating feature development with staging/assurance evidence.

## Current position

| Stage | Scope | Status |
|---|---|---|
| Phases 1–7 | Repository-controlled engineering baseline | `PASS` |
| RC13 | Functional unified-console acceptance | `PASS / OWNER_ACCEPTED` |
| Phase 8 | Real production-equivalent staging acceptance | `READY / PENDING_EXTERNAL_DEPLOYMENT_IDENTITY` |
| Phase 9 | Independent external assurance | `NOT COMPLETE` |
| Phase 10 | Formal production go/no-go | `NOT STARTED` |

DTMO is **not production ready**.

# Track A — Production readiness

## Phase 8 — real staging acceptance

### Phase 8.1 — environment and immutable deployment identity

**Objective:** establish one approved production-equivalent staging environment and bind all evidence to one immutable deployment identity.

Required outputs:

- approved environment identifier;
- accountable staging owner;
- approved endpoint/access path;
- exact deployed release and Git commit;
- immutable application/supporting image digests;
- infrastructure/runtime inventory;
- configuration parity and approved deviations;
- separate least-privilege application/service identities;
- secret-management references;
- TLS/network restrictions;
- controlled data/sanitization evidence;
- no-production-credential confirmation;
- deployment/change record;
- rollback target/procedure;
- deployment-time CVE/vendor-advisory/security review.

### Phase 8.2 — platform and identity validation

Validate against the immutable staging identity:

- application health/readiness;
- database migrations/connectivity;
- search/cache/object storage;
- authentication/authorization;
- service-account/human separation;
- privileged Administration controls;
- audit/correlation behavior;
- operational metrics and separately authenticated Grafana.

### Phase 8.3 — source-to-intelligence validation

Validate:

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

Phase 8 is complete only after the full evidence package is reviewable and an accountable staging/project acceptance decision is recorded.

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

GitHub issue #171 is the umbrella backlog for the owner-approved post-RC13 enhancements.

## E1 — shared severity semantics and filters

**Priority:** 1  
**Scope:** Overview + Intelligence

Deliver:

- a single shared severity taxonomy/filter contract;
- informational/low/medium/high filtering;
- accessible semantic presentation (e.g. low/green, medium/amber, high/red) with labels/icons/non-colour cues;
- consistent filtered totals and graphics;
- truthful empty filtered states;
- browser/keyboard/WCAG coverage.

This is the next product-development slice.

## E2 — governed manual source onboarding

**Priority:** 2

Deliver a controlled Sources & Catalog flow for manually registering sources with:

- source identity/type;
- endpoint;
- schedule/freshness expectation;
- authentication mode/logical secret reference;
- ownership;
- default-disabled state;
- validation/test-run before activation;
- audit/RBAC controls.

Source creation/execution must not grant publication authority.

## E3 — richer Visual Analytics and trend analysis

**Priority:** 2

Deliver:

- consistent severity semantics with E1;
- configurable time windows (at minimum 24h/7d/30d when data supports them);
- distinction between volume trend and severity/risk trend;
- richer native visualizations;
- framework aggregation only when backed by explicit first-class mappings.

## E4 — first-class framework mapping model

**Priority:** 3

Create a canonical mapping data/API model supporting explicit, reviewable mappings for agreed frameworks, initially considering:

- Normenkader IBP;
- MITRE ATT&CK;
- CVSS fields/context.

Every mapping should record:

- framework/version;
- control/technique/identifier;
- mapping type/relationship;
- evidence/provenance source;
- confidence/status;
- review state and reviewer context;
- timestamps/versioning.

Missing mappings remain `UNMAPPED`; no automatic semantic equivalence is accepted.

## E5 — richer Administration RBAC

**Priority:** 3

Deliver:

- role-to-permission matrix visibility;
- governed role assignment workflows;
- policy-bounded custom role/assignment capability where approved;
- self-lockout and final-admin protections;
- strict service-account/human separation;
- auditable actor/reason/correlation/before-after state;
- explicit separation from review/share approval authority.

## E6 — deeper Governance framework surface

**Priority:** 3

Build on E4 rather than creating a parallel mapping truth model.

Deliver:

- framework/version inventory;
- mapping coverage and mapped/unmapped counts;
- evidence provenance/review state;
- drill-down from framework control/technique to DTMO mapping/control/intelligence evidence;
- explicit distinction between normative requirement, internal control implementation, intelligence relationship and evidence;
- truthful `UNMAPPED`/`CONTEXT_ONLY` states.

# Delivery discipline

Each product enhancement is implemented as a bounded PR with:

- explicit acceptance criteria;
- focused unit/contract/browser tests;
- preservation of accepted RC13 behavior;
- preservation of RBAC, privacy, provenance and publication boundaries;
- complete exact-head CI before merge;
- staging validation when the enhancement is part of a Phase 8 candidate deployment.

## Documentation discipline

Professional product, architecture, security, governance and readiness documents describe stable capabilities and controlled current state. Operational PR/incident chronology belongs in `docs/development/runs/`, issues and CI evidence and must not replace the professional documentation layers.

## Immediate next steps

1. Complete the professional documentation restoration/reconciliation.
2. Start product enhancement **E1 — shared severity semantics and filters for Overview + Intelligence**.
3. Continue Phase 8.1 real staging identity work as the active production-readiness track.

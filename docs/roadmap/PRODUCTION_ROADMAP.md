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
| E8.1–E8.10 | Vulnerability & CTI ecosystem integrations | `PASS / REPOSITORY_COMPLETE` |
| Phase 8.1 historical identity | Earlier real staging environment + immutable deployment identity | `PASS / OWNER_VERIFIED_EXTERNAL_EVIDENCE — HISTORICAL IDENTITY ONLY` |
| Post-E8 candidate rebind | Deploy and bind the final E8 candidate to a new immutable staging identity | `NEXT ACTIVE OBJECTIVE / EXTERNAL EVIDENCE REQUIRED` |
| Phase 8.2–8.5 | Deployed staging validation and accountable staging acceptance against the new identity | `IN PROGRESS / NEXT` |
| Phase 9 | Independent external assurance | `NOT COMPLETE` |
| Phase 10 | Formal production go/no-go | `NOT STARTED` |

DTMO is **not production ready**.

# Track A — Production readiness

## Phase 8 — real staging acceptance

### Phase 8.1 — environment and immutable deployment identity

**Historical status:** `PASS / OWNER_VERIFIED_EXTERNAL_EVIDENCE`

The earlier Phase 8.1 evidence remains valid for the immutable staging deployment identity it originally covered. E8 materially changed the intended production candidate after that evidence was accepted. Historical evidence is therefore not relabelled as evidence for the post-E8 candidate.

### Post-E8 candidate rebind — next active objective

The repository candidate after E8.10 is identified by Git commit `b5d485ba2770a66ef6cf7e387ebab1613f77c9a4`. That repository identity alone does not prove a staging deployment.

Before Phase 8.2 resumes, the post-E8 candidate must be deployed to the approved production-equivalent staging environment and bound to a new immutable identity containing:

- approved staging environment identity and accountable owner;
- approved reachable staging access path;
- deployed release and exact Git commit;
- immutable application/supporting image digests;
- runtime/infrastructure inventory;
- configuration parity and approved deviations;
- least-privilege identities and approved secret handling;
- TLS/network/data-sanitization evidence;
- no-production-credential reuse confirmation;
- deployment/change and rollback records;
- deployment-time security/CVE review.

Repository CI, Docker Compose, staging emulators and synthetic browser fixtures cannot satisfy this evidence requirement.

### Phase 8.2 — platform and identity validation

**Status:** `IN PROGRESS / NEXT — blocked pending post-E8 immutable deployment identity`

After the new identity is externally verified, validate against that same immutable staging identity:

- application health/readiness;
- database migrations/connectivity;
- search/cache/object storage;
- authentication/authorization;
- service-account/human separation;
- privileged Administration controls;
- audit/correlation behavior;
- operational metrics and separately authenticated Grafana.

### Phase 8.3 — source-to-intelligence validation

Validate against the same new staging identity:

- source catalog/bootstrap and activation/execution;
- OpenCVE and Vulnerability-Lookup ingestion;
- MISP read integration and governed outbound-sharing boundaries;
- AIL read/enrichment and correlation boundaries;
- upstream fetch and raw evidence retention;
- normalization/provenance and canonical PostgreSQL commit;
- OpenSearch indexing/search;
- Intelligence, Overview, Governance and Visual Analytics visibility;
- vulnerability CVSS/EPSS/KEV/vendor/product/CWE/sighting analytics and degraded states.

### Phase 8.4 — operational and recovery validation

Validate:

- operational metrics/alerts;
- logging/correlation;
- runbook applicability;
- agreed backup/restore/recovery scenarios;
- rollback readiness;
- change/deployment traceability.

### Phase 8.5 — accountable staging acceptance

Phase 8 is complete only after the full deployed-environment evidence package is reviewable, bound to the final immutable staging identity and an accountable staging/project acceptance decision is recorded.

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
- OpenCVE and CIRCL Vulnerability-Lookup integrations;
- explainable vulnerability prioritization and governed vendor/product relevance;
- vulnerability analytics in Overview, Intelligence and Visual Analytics;
- governed MISP read and separately approved outbound sharing;
- governed AIL read/enrichment and exact correlation workspace;
- Normenkader IBP SM.07 vulnerability-management evidence mapping with explicit CVSS, EPSS, KEV, MITRE ATT&CK, MISP and AIL semantic boundaries.

E8.1–E8.10 are repository-complete. Further product evolution must not displace the active Phase 8 production-readiness gate.

# Delivery discipline

Each further change is implemented as a bounded PR with explicit acceptance criteria, focused tests, preservation of accepted behavior and governance boundaries, complete exact-head CI before merge, and staging revalidation when a change affects the deployed Phase 8 candidate.

## Documentation discipline

Professional product, architecture, security, governance and readiness documents describe stable capabilities and controlled current state. Operational PR/incident chronology belongs in development run records, issues and CI evidence.

## Immediate next steps

1. Deploy and externally verify the **post-E8 immutable staging deployment identity** for the final candidate.
2. Execute **Phase 8.2 platform and identity validation** against that exact identity.
3. Continue to Phase 8.3 and Phase 8.4 only while evidence remains bound to the same immutable deployment identity.
4. Record accountable Phase 8.5 staging acceptance before entering Phase 9 independent assurance.

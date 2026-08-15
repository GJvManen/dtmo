# DTMO Roadmap — Production Readiness and Product Evolution

Last updated: **2026-08-15**

## Purpose

This roadmap separates two tracks that must remain distinct:

1. **Production readiness** — evidence progression from accepted engineering/product maturity to production authorization.
2. **Product evolution** — bounded capability improvements that do not themselves constitute staging, assurance or production evidence.

## Current position

| Stage | Scope | Status |
|---|---|---|
| Phases 1–7 | Repository-controlled engineering baseline | `PASS` |
| RC13 + owner retest | Unified-console functional acceptance | `PASS / OWNER_ACCEPTED` |
| E8.1–E8.10 | Vulnerability & CTI ecosystem integrations | `PASS / REPOSITORY_COMPLETE` |
| Historical Phase 8.1 identity | Earlier immutable staging identity | `PASS / OWNER_VERIFIED_EXTERNAL_EVIDENCE — HISTORICAL IDENTITY ONLY` |
| Post-E8 external deployment + approved staging | Final E8 candidate externally deployed and extensively owner-tested | `PASS / OWNER_VERIFIED_EXTERNAL_EVIDENCE` |
| Phase 8.2 | Platform and identity validation | `REPOSITORY CONTRACT COMPLETE / EXTERNAL ACCEPTANCE REQUIRED` |
| Phase 8.3 | Source-to-intelligence validation | `REPOSITORY CONTRACT COMPLETE / EXTERNAL ACCEPTANCE REQUIRED` |
| Phase 8.4 | Operations, recovery and rollback validation | `REPOSITORY CONTRACT COMPLETE / EXTERNAL ACCEPTANCE REQUIRED` |
| Phase 8.5 | Accountable staging acceptance | `REPOSITORY CONTRACT COMPLETE / EXTERNAL OWNER DECISION REQUIRED` |
| Phase 9 | Independent external assurance | `NOT COMPLETE / NEXT AFTER PHASE 8 PASS` |
| Phase 10 | Formal production go/no-go | `NOT STARTED` |

DTMO is **not production ready**.

# Track A — Production readiness

## Phase 8 — production-equivalent staging acceptance

The post-E8 candidate has been externally deployed and extensively tested in an owner-approved production-equivalent staging environment. This removes the earlier deployment/staging prerequisite but does not by itself close Phase 8.

Formal Phase 8 closure requires one reviewable external evidence package bound to a single immutable staging deployment identity. That package must include exact deployed release/commit, immutable image digests, runtime/configuration evidence and the accepted results from the 8.2–8.4 validation contracts.

### Phase 8.2 — platform and identity validation

**Repository status:** `CONTRACT COMPLETE / EXTERNAL ACCEPTANCE REQUIRED`

External evidence must cover health/readiness, PostgreSQL, OpenSearch, Redis, object storage, bearer-token trust, RBAC, human/service separation, privileged Administration, audit/correlation, Prometheus and Grafana against the same immutable staging identity.

### Phase 8.3 — source-to-intelligence validation

**Repository status:** `CONTRACT COMPLETE / EXTERNAL ACCEPTANCE REQUIRED`

External evidence must demonstrate a real approved source from retrieval through provenance/raw evidence, normalization, canonical persistence, search/indexing, deduplication/idempotency, enrichment/correlation, vulnerability/CTI semantics, API/UI presentation, governance/classification, traceability and degraded behavior.

### Phase 8.4 — operations, recovery and rollback

**Repository status:** `CONTRACT COMPLETE / EXTERNAL ACCEPTANCE REQUIRED`

External evidence must demonstrate representative service recovery, PostgreSQL/object-storage/OpenSearch/Redis recovery, application rollback, migration recovery boundaries, IAM/secrets continuity, observability continuity, degraded-dependency visibility, RTO/RPO observations and change/rollback traceability.

### Phase 8.5 — accountable staging acceptance

**Repository status:** `CONTRACT COMPLETE / EXTERNAL OWNER DECISION REQUIRED`

Phase 8 is complete only when:

- accepted Phase 8.2, 8.3 and 8.4 evidence is bound to one immutable staging identity;
- exact deployed release/commit and image/runtime identity are recorded;
- approved deviations and residual staging risks are recorded;
- no unresolved release-blocking staging finding remains;
- rollback/change references are complete;
- an accountable owner records an explicit `PASS / OWNER_ACCEPTED` or `BLOCKED` decision.

Repository CI alone cannot satisfy this gate.

## Phase 9 — independent external assurance

**Status:** `NOT COMPLETE / NEXT AFTER PHASE 8 PASS`

The independent assurance scope includes:

- penetration testing against the accepted candidate;
- hardening/configuration review;
- IAM/secrets-management review;
- representative production-equivalent load/stress validation;
- resilience/recovery review;
- monitoring/incident-response readiness review;
- relevant privacy/legal/governance review;
- assurance-time dependency/CVE review;
- severity-based finding triage, remediation and independent retest where required;
- accountable residual-risk disposition;
- final `PASS / EXTERNAL_ASSURANCE_ACCEPTED` record.

Phase 9 cannot be marked PASS from repository CI, project self-attestation or historical pentest evidence for a materially different deployment identity.

## Phase 10 — formal production go/no-go

**Status:** `NOT STARTED`

Required decision inputs:

- accepted Phase 8 evidence;
- accepted Phase 9 independent assurance;
- approved production environment and ownership/support model;
- IAM/secrets/network approval;
- backup/recovery/rollback approval;
- monitoring/on-call/escalation approval;
- privacy/data/legal approval;
- open finding and residual-risk statement;
- formal release/change decision.

# Track B — Product evolution

The accepted repository baseline includes:

- shared accessible severity/classification semantics and filtering;
- governed manual source onboarding;
- configurable native trends and vulnerability analytics;
- versioned provenance-backed framework mappings;
- deeper Administration/RBAC management;
- OpenCVE and CIRCL Vulnerability-Lookup;
- explainable vulnerability prioritization and vendor/product relevance;
- governed MISP read and separately approved outbound sharing;
- governed AIL read/enrichment/correlation;
- vulnerability-management evidence mapping with explicit CVSS, EPSS, KEV, MITRE ATT&CK, MISP and AIL semantic boundaries.

E8.1–E8.10 are repository-complete. Further product evolution must not displace the production-readiness evidence path or silently invalidate the staging candidate under assessment.

# Delivery and documentation discipline

Each material change requires bounded scope, explicit acceptance criteria, applicable tests, exact-head CI and staging/assurance revalidation when it changes the candidate under evidence.

Professional documentation records stable product, architecture, security, governance and current readiness state. PR/run/workflow chronology remains in `docs/development/`, GitHub issues/pull requests and CI artifacts.

## Immediate next steps

1. Complete immutable technical identity binding for the accepted post-E8 staging deployment.
2. Complete and accept external Phase 8.2 evidence against that identity.
3. Complete and accept external Phase 8.3 evidence against that identity.
4. Complete and accept external Phase 8.4 evidence against that identity.
5. Record Phase 8.5 accountable owner decision and residual-risk/deviation disposition.
6. After Phase 8 PASS, execute Phase 9 independent assurance and remediate/retest release-blocking findings.
7. Only after accepted Phase 8 and Phase 9 evidence, execute Phase 10 production go/no-go.

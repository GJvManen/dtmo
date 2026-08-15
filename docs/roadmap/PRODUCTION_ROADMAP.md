# DTMO Roadmap — Production Readiness and Product Evolution

Last updated: **2026-08-15**

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
| Post-E8 external deployment + staging environment | Final E8 candidate externally deployed, extensively owner-tested, and staging environment approved | `PASS / OWNER_VERIFIED_EXTERNAL_EVIDENCE` |
| Post-E8 immutable evidence binding | Bind the accepted deployment to exact deployed release/commit, image digests and runtime identity | `EVIDENCE BINDING REQUIRED FOR FORMAL PHASE 8 CLOSURE` |
| Phase 8.2 | Production-equivalent platform and identity validation | `REPOSITORY CONTRACT COMPLETE / EXTERNAL ACCEPTANCE REQUIRED` |
| Phase 8.3 | Source-to-intelligence validation | `REPOSITORY CONTRACT COMPLETE / EXTERNAL ACCEPTANCE REQUIRED` |
| Phase 8.4 | Operations/recovery and rollback validation | `REPOSITORY CONTRACT COMPLETE / EXTERNAL ACCEPTANCE REQUIRED` |
| Phase 8.5 | Accountable staging acceptance | `IN PROGRESS / ACTIVE` |
| Phase 9 | Independent external assurance | `NOT COMPLETE` |
| Phase 10 | Formal production go/no-go | `NOT STARTED` |

DTMO is **not production ready**.

# Track A — Production readiness

## Phase 8 — real staging acceptance

### Phase 8.1 — environment and immutable deployment identity

**Historical status:** `PASS / OWNER_VERIFIED_EXTERNAL_EVIDENCE`

The earlier Phase 8.1 evidence remains valid for the immutable staging deployment identity it originally covered. E8 materially changed the intended production candidate after that evidence was accepted. Historical evidence is therefore not relabelled as evidence for the post-E8 candidate.

### Post-E8 external deployment and staging acceptance

**Status:** `PASS / OWNER_VERIFIED_EXTERNAL_EVIDENCE`

On 2026-08-15 the accountable owner confirmed that the post-E8 deployment had been extensively and successfully tested externally and that the production-equivalent staging environment is approved. This removes the prior blocker requiring a real external deployment and an approved staging environment before Phase 8.2 can begin.

This owner-provided acceptance is deployment/staging evidence, not a substitute for immutable technical identity evidence. Formal Phase 8 closure still requires the accepted deployment to be bound to the exact deployed release/commit, immutable application/supporting image digests and runtime/infrastructure identity. Where already captured by the deployment platform, those values should be added to the evidence package without redeploying or changing the accepted candidate.

The evidence package for the accepted staging deployment should contain or reference:

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

Repository CI, Docker Compose, staging emulators and synthetic browser fixtures cannot substitute for the externally accepted staging evidence.

### Phase 8.2 — platform and identity validation

**Repository status:** `CONTRACT COMPLETE / EXTERNAL ACCEPTANCE REQUIRED`

The step-scoped platform/identity validation contracts are repository-complete. Formal closure still requires external evidence against the accepted production-equivalent staging deployment and binding to the same immutable deployment identity.

Validate externally:

- application health/readiness;
- database migrations/connectivity;
- search/cache/object storage;
- authentication/authorization;
- service-account/human separation;
- privileged Administration controls;
- audit/correlation behavior;
- operational metrics and separately authenticated Grafana.

### Phase 8.3 — source-to-intelligence validation

**Repository status:** `CONTRACT COMPLETE / EXTERNAL ACCEPTANCE REQUIRED`

The fail-closed source-to-intelligence validation contract is repository-complete. External acceptance must still demonstrate, against the same immutable staging deployment:

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

**Repository status:** `CONTRACT COMPLETE / EXTERNAL ACCEPTANCE REQUIRED`

The fail-closed operations/recovery contract is repository-complete. External acceptance must still demonstrate:

- operational metrics/alerts and observability continuity;
- logging/correlation through failure and recovery;
- runbook applicability;
- agreed PostgreSQL/object-storage/search/cache recovery scenarios;
- application rollback and migration recovery boundaries;
- RTO/RPO observations and deviations;
- change/deployment/rollback traceability.

### Phase 8.5 — accountable staging acceptance

**Status:** `IN PROGRESS / ACTIVE`

Phase 8 is complete only after the full deployed-environment evidence package is reviewable, bound to one final immutable staging identity and an accountable owner acceptance decision is recorded.

Phase 8.5 must consolidate accepted external evidence from Phases 8.2, 8.3 and 8.4, record approved deviations and residual risks, confirm no unresolved release-blocking staging finding remains, and record an explicit `PASS / OWNER_ACCEPTED` or `BLOCKED` decision. Repository CI alone cannot satisfy this gate.

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

1. Complete and accept the external **Phase 8.2** evidence package against one immutable staging deployment identity.
2. Complete and accept **Phase 8.3 source-to-intelligence** evidence against that same identity.
3. Complete and accept **Phase 8.4 operations/recovery** evidence against that same identity.
4. Record accountable **Phase 8.5 staging acceptance** with explicit owner decision and residual-risk/deviation disposition.
5. Enter **Phase 9 independent external assurance** only after Phase 8 is formally `PASS / OWNER_ACCEPTED`.
6. Complete Phase 9 assurance and residual-risk disposition before Phase 10 production go/no-go.

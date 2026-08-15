# DTMO Evidence Index

Last updated: **2026-08-15**

## Purpose

This index maps the DTMO roadmap stages to their primary evidence classes and authoritative documentation. It is a professional evidence map, not a chronological CI/incident log.

Exact workflow/job/commit history is retained in `docs/development/`, GitHub pull requests/issues and CI artifacts.

## Authoritative sources

- Project/documentation portal: `docs/README.md`
- System architecture: `docs/architecture/SYSTEM_ARCHITECTURE.md`
- Current state: `docs/project/CURRENT_STATE.md`
- Executive status: `docs/project/EXECUTIVE_STATUS.md`
- Production readiness report: `docs/project/PRODUCTION_READINESS_REPORT.md`
- Production checklist: `docs/project/PRODUCTION_CHECKLIST.md`
- Production roadmap: `docs/roadmap/PRODUCTION_ROADMAP.md`
- QA/release model: `docs/qa/QA_AND_RELEASE_GATES.md`
- Traceability: `docs/traceability/TRACEABILITY_MATRIX.md`
- Operational run evidence: `docs/development/RUN_LOG.md` and `docs/development/runs/`
- External production-readiness gates: GitHub issues #1, #3 and Phase 8 issue #158

## Evidence hierarchy

DTMO distinguishes four main evidence layers:

1. **Repository-controlled engineering evidence** — exact-head CI, contracts, browser tests, recovery/performance/observability evidence.
2. **Accountable functional evidence** — project-owner functional acceptance of the merged product.
3. **Real environment evidence** — production-equivalent staging deployment and validation tied to an immutable identity.
4. **Independent assurance and formal approval** — external assessment and production go/no-go.

These layers are additive and non-interchangeable.

## Phase evidence map

### Phases 1–7 — engineering baseline

**Status:** `PASS`.

Evidence classes include exact-head workflow/release integrity; authentication/authorization/RBAC and approval boundaries; migrations, persistence, integrity and recovery; connector contracts and provenance; performance; browser/accessibility/UX evidence; observability, alerting, dashboards, runbooks and exercises; and open-source governance.

### RC13 — functional unified-console acceptance

**Status:** `PASS / OWNER_ACCEPTED`.

Primary documentation:

- `docs/qa/RC13_FUNCTIONAL_CONSOLE_ACCEPTANCE_GATE.md`
- `docs/project/CURRENT_STATE.md`
- immutable acceptance record in `docs/development/runs/`

### Phase 8 — real staging acceptance

**Status:** `ACTIVE / OWNER_VERIFIED_EXTERNAL_DEPLOYMENT_AND_APPROVED_STAGING / IMMUTABLE_EVIDENCE_BINDING_INCOMPLETE`.

Primary documentation:

- `docs/qa/PHASE8_STAGING_DEPLOYMENT_PARITY_GATE.md`
- `docs/staging/PHASE8_DEPLOYMENT_IDENTITY_RECORD.md`
- `docs/staging/PHASE8_2_PLATFORM_IDENTITY_VALIDATION.md`
- GitHub issue #158

On 2026-08-15 the accountable owner confirmed that the post-E8 external deployment had been extensively and successfully tested and that the production-equivalent staging environment is approved. This satisfies the external-deployment/staging-approval prerequisite for beginning Phase 8.2.

Formal Phase 8 closure still requires evidence to bind the accepted deployment to its exact deployed release/commit, immutable application/supporting image digests, runtime/infrastructure identity and the remaining parity/security/change references. Repository staging-emulator/readiness workflows remain supporting preparation only and cannot substitute for those external facts.

Required real evidence includes:

- approved environment and owner;
- immutable deployed release/commit/image identity;
- infrastructure/runtime/configuration parity;
- least-privilege IAM and secret-management references;
- TLS/network controls;
- data/sanitization/no-production-credential statement;
- deployment/change and rollback evidence;
- deployment-time security review;
- deployed functional/operational acceptance suites;
- accountable staging acceptance.

### Phase 9 — independent external assurance

**Status:** `NOT COMPLETE`.

Primary contract: `docs/qa/PHASE9_EXTERNAL_ASSURANCE_GATE.md`.

Required evidence classes include independent penetration testing; representative production-equivalent load/stress; resilience/recovery review where applicable; platform/configuration hardening; IAM/secrets-management review; monitoring readiness; privacy/legal/governance assurance where required; and residual-risk disposition.

### Phase 10 — production go/no-go

**Status:** `NOT STARTED`.

Required inputs include accepted Phase 8 and Phase 9 evidence, approved production identity/environment/ownership, release/change/rollback evidence, monitoring/on-call/escalation acceptance, privacy/data/security governance approval and a formal accountable production decision.

## Framework/governance evidence

Framework mapping claims are governed by `docs/governance/GOVERNANCE_MAPPING_REGISTRY.md`. E8.10 added repository-backed vulnerability/CTI evidence mappings and explicit semantic boundaries, including Normenkader IBP SM.07 and related vulnerability-management context. External framework claims remain limited to the mappings and provenance explicitly recorded by the governance registry; no broader compliance claim is inferred.

## Evidence handling rules

- Evidence must be attributable, scoped and reviewable.
- Automated acceptance evidence must match the exact state being accepted.
- A new material deployment invalidates earlier deployment-bound acceptance evidence unless explicitly rebound.
- Missing, queued, skipped, cancelled, failed, stale or inaccessible evidence is not `PASS`.
- Evidence must not contain raw credentials, tokens, secret values or unnecessary personal data.
- Threat/CVE/vendor-advisory evidence must retain provenance, review time, applicability and confidence.
- Human review and external-share approval remain separate from technical execution.
- Historical immutable run records are not rewritten to reflect later decisions.

## Operational evidence location

Detailed implementation chronology, workflow identifiers, root-cause findings and point-in-time blockers are intentionally retained under `docs/development/RUN_LOG.md`, `docs/development/runs/`, GitHub issues/pull requests and CI artifacts. Those records support auditability but do not replace professional project/architecture documentation.

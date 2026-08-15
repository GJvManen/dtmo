# Phase 9 — Independent External Assurance Gate

**Decision:** `NOT COMPLETE`  
**Entry condition:** Phase 8 must be formally `PASS / OWNER_ACCEPTED` before Phase 9 may be accepted.

## Objective

Define the minimum reviewable evidence contract for independent external assurance of DTMO while preserving separation of duties, privacy, provenance, auditability, RBAC, secrets handling and human external-share approval.

This gate defines required evidence. It does not claim independent assurance has already occurred.

## Current lifecycle context

- Phases 1–7: `PASS`;
- RC13 functional product: `PASS / OWNER_ACCEPTED`;
- E8.1–E8.10: `PASS / REPOSITORY_COMPLETE`;
- post-E8 external staging deployment: `PASS / OWNER_VERIFIED_EXTERNAL_EVIDENCE`;
- Phase 8.2–8.4 repository contracts: complete, external acceptance required;
- Phase 8.5 repository contract: complete, external accountable owner decision required;
- Phase 9: `NOT COMPLETE`;
- Phase 10: `NOT STARTED`.

Phase 9 must be performed against the immutable candidate accepted in Phase 8, or against an explicitly equivalent target whose relationship to that accepted identity is reviewable and approved.

## Required assurance classes

### 1. Independent penetration testing

Evidence must identify the independent assessor, scope/rules of engagement, immutable target identity, execution dates, methodology/coverage, findings/severity method, remediation/risk disposition and retest/closure evidence where applicable.

### 2. Representative load and stress validation

Record workload model/provenance, immutable target identity, concurrency/volume assumptions, accepted thresholds/SLOs, privacy-safe measurements, bottlenecks/failure modes and remediation/disposition.

Repository performance gates remain engineering baselines and do not replace representative independent/external execution.

### 3. Resilience and recovery assurance

Review backup/restore and recovery evidence for the target, including components/stores covered, execution dates, integrity validation, RPO/RTO observations where applicable, operator/assessor sign-off and unresolved limitations.

### 4. Platform and configuration hardening

Review the actual target platform for network/TLS restrictions, container/runtime hardening, PostgreSQL/OpenSearch/Redis/object-storage configuration, operational access, monitoring/logging exposure, patch/version posture and approved deviations/residual risk.

### 5. IAM and secrets-management assurance

Evidence must cover approved secret-management mechanisms, least-privilege application/service identities, human/service separation, credential lifecycle/rotation, bearer-token trust architecture, absence of development-only credential exceptions and exclusion of raw secret values from retained evidence.

### 6. Monitoring and incident-response readiness

Review operational telemetry, alerting, audit/correlation, on-call/escalation procedures, incident-response ownership and evidence continuity required for the production candidate.

### 7. Privacy, legal and governance assurance

Where applicable, review data classification/minimization, source usage/redistribution authority, retention, privacy obligations, governance mappings and external-sharing authority boundaries.

### 8. Assurance-time vulnerability review

Review relevant dependency, platform, container/base-image, CVE and vendor-advisory state against the immutable target. Record provenance, review time, applicability, confidence and remediation/disposition.

## Finding management

Every material finding must have:

- severity and rationale;
- affected target/component;
- accountable owner;
- remediation or risk-disposition decision;
- due date where applicable;
- evidence reference;
- independent retest/closure evidence for release-blocking findings where required.

Critical/high or otherwise release-blocking findings cannot be silently waived.

## Evidence rules

- Evidence must be independent, attributable, dated and target-bound.
- Missing, stale, inaccessible, inferred or contradictory evidence is not `PASS`.
- Repository CI, Docker Compose, staging emulators and project self-attestation cannot substitute for independent execution.
- Secret values, credentials, tokens and unnecessary personal data must not be retained in repository evidence.
- Intelligence review and external-share approval remain separate authorities.
- Production authorization cannot be inferred from Phase 9 success; it remains a Phase 10 decision.

## Acceptance rule

Phase 9 may become `PASS / EXTERNAL_ASSURANCE_ACCEPTED` only when the agreed assurance classes are complete and reviewable, all release-blocking findings are closed or formally dispositioned, required retests are accepted, residual risk is explicitly owned and the evidence is traceably bound to the Phase 8 accepted candidate.

## Current dependency

**Complete and accept the Phase 8 external evidence package and accountable Phase 8.5 decision before crediting Phase 9 assurance.**

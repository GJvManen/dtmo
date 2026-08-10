# Phase 9 External Assurance Gate

## Decision

`NOT COMPLETE` — readiness/intake contract defined; no external assurance activity is credited by this document.

## Objective

Define the minimum reviewable evidence contract for Phase 9 so externally executed assurance can be accepted without weakening separation of duties, privacy, provenance, auditability, RBAC or human share approval.

## Required evidence classes

1. **Independent penetration test** — named independent assessor/organization, scope, rules of engagement, immutable target release/environment identity, execution dates, findings, severity method, remediation disposition and retest/closure evidence.
2. **Representative load and stress test** — workload model and provenance, target identity, concurrency/volume assumptions, thresholds/SLOs, raw or summarized privacy-safe measurements, bottlenecks and disposition.
3. **Full backup and restoration exercise** — immutable backup/restore identities, stores covered, execution timestamps, RPO/RTO observations, integrity verification and operator sign-off.
4. **Production platform hardening** — OpenSearch/security controls, network/TLS restrictions, runtime hardening and configuration evidence tied to the target platform identity.
5. **Secrets-management acceptance** — approved secrets manager/identity references, least privilege, credential rotation/replacement evidence and explicit exclusion of secret values from repository evidence.
6. **Operational and stakeholder acceptance** — accountable service owner plus required CISO/ISO and privacy-function approval, with separation between technical access, review and human share approval.
7. **Deployment acceptance** — staging and production acceptance records tied to immutable release/image/deployment identities, approved change records and rollback targets.

## Evidence rules

- Evidence must be independently observable, attributable, dated and tied to the immutable target identity where applicable.
- Missing, stale, inaccessible, inferred or contradictory evidence is not PASS.
- Repository CI or emulator evidence cannot substitute for independent external execution.
- Findings may not be silently waived; unresolved findings require an explicit risk decision by an authorized human role.
- Secret values, credentials, tokens and unnecessary personal data must not be committed.
- `reviewed` and `share approved` remain separate authorities.
- Production acceptance cannot be inferred from staging acceptance.

## Threat, CVE and vendor-advisory provenance

Where an assurance activity depends on the deployed software/platform state, the evidence package must include a time-bounded review of relevant public threat intelligence, CVE data and vendor advisories against the immutable target release/platform. Record source provenance, review time, applicability and confidence. Generic or stale advisory summaries do not close this requirement.

## Claim boundary

This gate defines intake and acceptance criteria only. It does not prove that penetration testing, representative load/stress, full restoration, production hardening, secrets acceptance, stakeholder approval or deployment acceptance has occurred. Issue #1 remains authoritative for external completion state.

## Exactly one next priority

Validate RUN-159 and this Phase 9 intake contract through the complete exact-head PR workflow matrix. Merge only on complete success; after merge, acquire the first missing independent assurance evidence class in issue #1 without marking absent external execution as PASS.

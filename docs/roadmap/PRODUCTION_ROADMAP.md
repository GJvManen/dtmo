# DTMO Production Readiness Roadmap

## Purpose

This roadmap defines the controlled path from DTMO's current release-candidate state to production readiness. It is executed through bounded PDCA runs and tracked in GitHub issue #3.

The release rule is strict: no phase is complete without objective evidence. Missing CI, security, recovery, performance, accessibility, operational or external-assurance evidence blocks production readiness.

## Current status — 2026-08-09

- Phase 1 — CI and workflow integrity: `PASS`.
- Phase 2 — Application security and identity: `PASS` for internal gates.
- Phase 3 — Data integrity and recovery: `PASS` for internal gates.
- Phase 4 — Live connector reliability and provenance: `PASS` for internal gates.
- Phase 5 — Performance and scalability: `PASS` for internal gates.
- Phase 6 — Frontend accessibility and operational UX: `BLOCKED_EXTERNAL` only for genuine VoiceOver/NVDA execution on supported real hosts.
- Phase 7 — Observability and incident operations: `PASS`.
- Phase 8 — Staging acceptance: `BLOCKED_EXTERNAL` at production-equivalent staging environment/deployment-parity acquisition.
- Phase 9 — External assurance: `NOT COMPLETE`; tracked in issue #1.
- Phase 10 — Production go/no-go: `NOT STARTED`.

## Phase 8 — Staging acceptance

Objectives: production-equivalent deployment, smoke/integration/migration/connector/recovery/performance/accessibility tests, secrets/TLS/network restrictions and retained deployment evidence.

Blocking gates:
- reproducible production-equivalent staging deployment;
- immutable application/container/dependency identity and configuration-parity evidence;
- approved secret-management path, least privilege and no production credentials in staging;
- TLS and network restrictions validated with no unintended public exposure;
- smoke/integration, migration, connector, recovery, performance, accessibility and observability tests executed against the deployed staging environment;
- rollback/recovery proven and evidence retained;
- no unresolved blocker is interpreted as PASS.

### RUN-147 staging-readiness baseline — `PASS`

PR #101 exact head `fd87beb441c4e4ed71141ea9ae03717e859681e3` completed 46/46 registered workflows successfully and retained artifact `9043667776` was exact-head bound with machine-readable PASS and JUnit 3/3. PR #101 merged as `5f74bcac92738febfe327ea78f45c009d28e4d55`.

### RUN-148 staging environment and deployment-parity acquisition — `BLOCKED_EXTERNAL`

No real staging endpoint/environment identifier or immutable deployment-parity evidence was found. Phase 8 cannot proceed to acceptance suites until all ten classes in `docs/qa/PHASE8_STAGING_DEPLOYMENT_PARITY_GATE.md` are retained against one staging deployment identity.

### RUN-149 RC4 regression remediation — `PASS`

PR #102 final exact head `c0bf83a8e0a9c51bdbd492fadfb60a71e25c7e9b` completed 46/46 workflows successfully, including RC4 and Phase 8 Staging Readiness Gate, and merged as `60897cdfd36a78297cf90521f14ded5116ec9653`. The remediation changed only the stale lifecycle-state regression assertion and preserved the external staging/deployment-parity claim boundary.

### RUN-150 Phase 8 blocker acceptance reconciliation — `BLOCKED_EXTERNAL`

A fresh live repository and issue #1 recheck after PR #102 acceptance found no approved staging environment, reachable endpoint, immutable deployed release/image digest inventory, infrastructure/configuration parity record, approved staging identity/secrets references, TLS/network evidence, data-class/no-production-credential statement, deployment change record, rollback target or deployment-time security/advisory review.

Repository CI cannot substitute for these environment controls. No staging acceptance suite is considered executed.

Exactly one next priority: provide or provision the approved production-equivalent staging environment and retain all ten deployment-parity evidence classes. Then execute the first bounded staging smoke/integration acceptance run.

## Phase 9 — External assurance

Tracked in issue #1: independent penetration test, representative load/stress, full backup/restoration exercise, production platform hardening, required secrets-management acceptance, operational/stakeholder approvals and production deployment acceptance.

## Phase 10 — Production go/no-go

Go requires every prior phase and external gate complete with retained evidence, green CI, release notes/SBOM/deployment manifest/rollback plan, proven recovery and required approvals. Any missing blocking evidence is `NO-GO`.

## PDCA execution order

1. Phase 1 — CI and workflow integrity.
2. Phase 2 — Application security and identity.
3. Phase 3 — Data integrity and recovery.
4. Phase 4 — Live connector reliability and provenance.
5. Phase 5 — Performance and scalability.
6. Phase 6 — Frontend accessibility and operational UX.
7. Phase 7 — Observability and incident operations.
8. Phase 8 — Staging acceptance.
9. Phase 9 — External assurance coordination.
10. Phase 10 — Production go/no-go.

Every run must document Plan, Do, Check and Act, update run/QA evidence, preserve claim boundaries, and leave exactly one next priority.

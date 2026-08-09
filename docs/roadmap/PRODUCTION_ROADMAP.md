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
- Phase 8 — Staging acceptance: `BLOCKED_EXTERNAL` for real deployment-parity evidence. The staging emulator configuration/topology baseline is `PASS`; RUN-153 runtime smoke is `CI_VALIDATION_PENDING`.
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

PR #101 exact head `fd87beb441c4e4ed71141ea9ae03717e859681e3` completed 46/46 registered workflows successfully; retained artifact `9043667776` was exact-head bound with machine-readable PASS and JUnit 3/3; PR #101 merged as `5f74bcac92738febfe327ea78f45c009d28e4d55`.

### RUN-148 staging environment and deployment-parity acquisition — `BLOCKED_EXTERNAL`

No real staging endpoint/environment identifier or immutable deployment-parity evidence was found. All ten classes in `docs/qa/PHASE8_STAGING_DEPLOYMENT_PARITY_GATE.md` remain required against one real staging deployment identity.

### RUN-149 RC4 regression remediation — `PASS`

PR #102 final exact head `c0bf83a8e0a9c51bdbd492fadfb60a71e25c7e9b` completed 46/46 workflows successfully and merged as `60897cdfd36a78297cf90521f14ded5116ec9653`.

### RUN-150 Phase 8 blocker acceptance reconciliation — `BLOCKED_EXTERNAL`

PR #103 exact head `be9deb34255f6114430d76868c9bf82f0e039f15` completed 46/46 workflows successfully and merged as `1e957f7fa1e9910e5d258cd6d7ed5ce69e9203d1`. No real staging deployment-parity package was found.

### RUN-151 production-equivalent staging emulator baseline — `PASS`

PR #104 final exact head `93d1a659b7b136546ffcf73102890f5d2d00ba84` completed 47/47 registered workflows successfully. Retained artifact `9045039742`, digest `sha256:959586b389579dfd37bda60eecdfb67e0251eaf4a78daed214986cefe771ce65`, was exact-head bound with machine-readable PASS and JUnit 4/4 with zero failures/errors/skips. PR #104 merged as `3c7a4b7f56e8d8a757541963bbd261fe42a7269c`.

The accepted emulator remains a configuration/topology contract. Its CI evidence does not prove a real staging environment or complete dependency runtime behavior.

### RUN-152 staging emulator CI-integrity remediation — `PASS`

The first PR #104 head completed 46/47 workflows; RC4 failed solely because the emulator QA omitted the canonical phrase `human share approval`. The documentation contract was repaired without weakening the test or any governance control. The final exact head then passed 47/47 workflows and was accepted with RUN-151.

### RUN-153 staging emulator runtime smoke — `CI_VALIDATION_PENDING`

RUN-153 builds the DTMO application image from the exact PR head, runs it with production-only configuration validation active, loopback-only host exposure, read-only root filesystem, `/tmp` tmpfs, `no-new-privileges` and dropped Linux capabilities, then exercises health/readiness, disabled connector behavior, response-security headers, request correlation and Prometheus metrics. The gate retains privacy-safe JSON/JUnit/container-log evidence and fails if synthetic sensitive markers appear in retained logs.

This bounded runtime smoke deliberately does not start PostgreSQL, Redis, OpenSearch, object storage or the external TLS gateway. It therefore does not prove the complete emulator topology, a real staging deployment, the ten deployment-parity evidence classes, Phase 8 completion or production acceptance.

Exactly one next priority: verify every registered workflow on the RUN-153 exact PR head and independently inspect retained `phase8-staging-emulator-runtime-evidence`. Merge only on full success. After acceptance, complete dependency-topology emulation or approved real staging provisioning remains the next Phase 8 step, with all ten deployment-parity evidence classes still mandatory before real staging acceptance is credited.

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

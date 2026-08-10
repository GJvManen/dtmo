# DTMO Production Readiness Roadmap

## Purpose

This roadmap defines the controlled path from DTMO's current release-candidate state to production readiness. It is executed through bounded PDCA runs and tracked in GitHub issue #3.

The release rule is strict: no phase is complete without objective evidence. Missing CI, security, recovery, performance, accessibility, operational or external-assurance evidence blocks production readiness.

## Current status — 2026-08-10

- Phase 1 — CI and workflow integrity: `PASS`.
- Phase 2 — Application security and identity: `PASS` for internal gates.
- Phase 3 — Data integrity and recovery: `PASS` for internal gates.
- Phase 4 — Live connector reliability and provenance: `PASS` for internal gates.
- Phase 5 — Performance and scalability: `PASS` for internal gates.
- Phase 6 — Frontend accessibility and operational UX: `BLOCKED_EXTERNAL` only for genuine VoiceOver/NVDA execution on supported real hosts.
- Phase 7 — Observability and incident operations: `PASS`.
- Phase 8 — Staging acceptance: `BLOCKED_EXTERNAL` for real deployment-parity evidence. The RUN-151/RUN-152 staging emulator is accepted as `PASS` for its bounded configuration-contract scope only; PR #106 reconciliation remains `CI_VALIDATION_PENDING` after RUN-154 lifecycle-regression remediation.
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

### RUN-151 production-equivalent staging emulator baseline — `PASS` for bounded emulator scope

RUN-151 adds a deterministic source-controlled staging emulator specification under `infrastructure/staging-emulator/`. It runs DTMO in `production` configuration mode and requires immutable digest-pinned images, external secrets/license/certificate inputs, backend network isolation, loopback-only TLS ingress, secured OpenSearch configuration, authenticated Redis, AIStor object storage, Prometheus/Grafana observability, disabled-by-default live connectors/AI analyst, and preserved human publication/share approval.

The `Phase 8 Staging Emulator Gate` validates rendered Compose topology without pulling or running the declared images. Its evidence therefore proves only the emulator configuration contract, not runtime behavior or a real staging environment.

### RUN-152 staging emulator CI-integrity remediation — `PASS`

PR #104 previous exact head `03611ee74eb2521a85942a34cec6e060ee989a0c` completed 46/47 workflows successfully. The dedicated staging-emulator gate succeeded; RC4 failed because the emulator QA document omitted the canonical phrase `human share approval` required by its governance regression test. The documentation contract was corrected without weakening the test or any governance control.

PR #104 final exact head `93d1a659b7b136546ffcf73102890f5d2d00ba84` then completed 47/47 registered workflows successfully. Retained artifact `9045039742`, digest `sha256:959586b389579dfd37bda60eecdfb67e0251eaf4a78daed214986cefe771ce65`, records decision `pass`, the exact final head, JUnit 4/4 and explicit false claim-boundary fields for container execution, real staging, deployment parity, ten external evidence classes, Phase 8 completion and production acceptance. PR #104 merged as `3c7a4b7f56e8d8a757541963bbd261fe42a7269c`.

### RUN-153 emulator acceptance documentation reconciliation — `CI_VALIDATION_PENDING`

PR #106 reconciles authoritative documentation with the accepted PR #104 evidence without changing runtime or governance controls. Previous exact head `469dcca367dc3fcdb2baf114afe91f903164736b` completed 46/47 workflows; RC4 failed on one stale lifecycle-state assertion.

### RUN-154 staging-emulator lifecycle regression remediation — `CI_VALIDATION_PENDING`

The failing regression still required the obsolete token `CI_VALIDATION_PENDING` in the staging-emulator QA document after the gate had correctly advanced to bounded `PASS`. The assertion now requires the evidenced bounded `PASS` wording while continuing to require the complete non-overclaim boundary and human share approval. Fresh complete exact-head CI is required.

Exactly one next priority: verify every registered workflow on PR #106's changed exact head and merge only on complete success.

After that merge, the next Phase 8 roadmap objective is acquisition/provisioning of one approved real staging deployment and retention of all ten deployment-parity evidence classes against the same immutable deployment identity.

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

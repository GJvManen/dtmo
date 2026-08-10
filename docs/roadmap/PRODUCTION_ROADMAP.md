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
- Phase 8 — Staging acceptance: `BLOCKED_EXTERNAL` for real deployment-parity evidence. The repository-controlled staging-emulator configuration contract and bounded application-container runtime smoke are accepted as `PASS` for their explicit scopes only. RUN-157 CI remediation is evidenced `PASS` on PR #108 exact head `25ac24bfa40f2f9ccebb5d1307615c6fbd14cf05`; the documentation-finalization head still requires fresh complete CI before merge.
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

PR #101 exact head `fd87beb441c4e4ed71141ea9ae03717e859681e3` completed 46/46 workflows successfully and merged.

### RUN-148 staging environment and deployment-parity acquisition — `BLOCKED_EXTERNAL`

No real staging endpoint/environment identifier or immutable deployment-parity evidence was found. All ten classes in `docs/qa/PHASE8_STAGING_DEPLOYMENT_PARITY_GATE.md` remain required against one real staging deployment identity.

### RUN-149 RC4 regression remediation — `PASS`

PR #102 completed 46/46 workflows successfully and merged.

### RUN-150 Phase 8 blocker acceptance reconciliation — `BLOCKED_EXTERNAL`

No real staging deployment-parity package was found.

### RUN-151 / RUN-152 staging emulator configuration contract — `PASS`

PR #104 final exact head `93d1a659b7b136546ffcf73102890f5d2d00ba84` completed 47/47 workflows. Retained artifact `9045039742` is exact-head bound with machine-readable PASS and JUnit 4/4. This proves only the source-controlled emulator configuration/topology contract; it does not prove runtime behavior, real staging, deployment parity, Phase 8 completion or production acceptance.

### RUN-153 / RUN-154 documentation reconciliation — `PASS`

PR #106 final exact head `ff0a490e46c2f9529441d8a5294030af498dbe14` completed 47/47 workflows and merged as `b57a6daa775d2f1f88a2d1b67b191da757fa743f` after the stale lifecycle-state regression was corrected without weakening the claim boundary or human share approval.

### RUN-155 staging-emulator application-container runtime smoke — `PASS`

PR #107 final exact head `52d7a37660c9bb1c9f8468f11010f36d17bd1fba` completed 48/48 registered workflows successfully and merged as `23d629964f55709845683e808f707998cc8d4aa2`. Retained artifact `9057259246`, digest `sha256:d577415a5b40952a305577c5a1fbeae1e3e154fcbf95a42030cdd19632d77aa5`, is exact-head bound with machine-readable PASS, contract JUnit 4/4 and runtime JUnit 12/12. The runtime checks cover production mode, health/readiness, human publication gate, authentication contract, security headers, correlation ID, connectors disabled/fail-closed and metrics. All real-staging/deployment-parity/Phase-8/production claim fields remain false.

The runtime smoke executes only the DTMO application container. It does not execute PostgreSQL, Redis, OpenSearch, object storage or the external TLS gateway and does not satisfy the real deployment-parity gate.

### RUN-156 real staging deployment-parity evidence acquisition — `BLOCKED_EXTERNAL`

A fresh repository and issue review found no approved real staging environment/deployment identity and no reviewable package satisfying all ten deployment-parity evidence classes against one immutable staging release. No missing evidence is treated as PASS and no downstream staging acceptance result is credited.

### RUN-157 runtime-smoke lifecycle regression remediation — `PASS`

PR #108 previous exact head `c4c28938a49b2a3dcba90ab01e6bd1cb430a3439` completed 47/48 workflows. RC4 failed in pytest after lint and type-check passed because the runtime-smoke governance regression still required obsolete `CI_VALIDATION_PENDING` wording after the gate had correctly advanced to bounded `PASS`.

The assertion was corrected to require the exact bounded PASS wording while continuing to require human share approval and the full real-staging/deployment-parity/Phase-8 non-overclaim boundary. PR #108 exact head `25ac24bfa40f2f9ccebb5d1307615c6fbd14cf05` then completed 48/48 registered workflows successfully. RC4 run `31375182061` passed lint, mypy, pytest (292 passed, 16 skipped, 84.96% coverage), compile and aggregate release gate. All three Phase 8 repository gates also succeeded. Retained runtime artifact `9057841831`, digest `sha256:0e68feb37e9937b574a6ef80affeff13aeda162eb83c8805a8f220cb082999b1`, is exact-head bound.

This acceptance remains bounded to the lifecycle regression remediation and does not change the Phase 8 external blocker.

Exactly one next priority: verify all 48 workflows on PR #108's documentation-finalization exact head and merge only on complete success.

After that merge, provide or provision one approved real staging deployment and retain all ten deployment-parity evidence classes against the same immutable deployment identity. Do not begin or credit the staging acceptance suite before that gate is complete.

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

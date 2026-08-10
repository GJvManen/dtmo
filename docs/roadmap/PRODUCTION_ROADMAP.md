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
- Phase 8 — Staging acceptance: `BLOCKED_EXTERNAL` for real deployment-parity evidence. The repository-controlled staging-emulator configuration contract is accepted as `PASS`; RUN-155 bounded application-container runtime smoke is `CI_VALIDATION_PENDING`.
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

### RUN-155 staging-emulator runtime smoke fresh-base remediation — `CI_VALIDATION_PENDING`

Existing PR #105 attempted the next bounded objective and its dedicated runtime gate succeeded, but RC4 failed at Ruff S310 in the runtime probe helper before type-check/tests; the branch then became stale against current `main`. RUN-155 ports the bounded runtime-smoke workflow/test/QA/probe onto current `main` and explicitly restricts probe URLs to loopback HTTP targets before request construction.

The runtime smoke executes only the DTMO application container. It does not execute PostgreSQL, Redis, OpenSearch, object storage or the external TLS gateway and does not satisfy any of the ten real deployment-parity evidence classes.

Exactly one next priority: verify every registered workflow on the RUN-155 exact final PR head and independently inspect retained `phase8-staging-emulator-runtime-evidence`. Merge only on complete success.

After runtime-smoke acceptance, return to acquisition/provisioning of one approved real staging deployment and retain all ten deployment-parity evidence classes against the same immutable deployment identity.

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

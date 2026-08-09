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

## Accepted Phase 7 evidence

RC10.1 through RC10.11 are accepted. RUN-145 reconciled the external operational blocker. RUN-146 recorded acceptance of all six human operational-acceptance evidence classes and PR #100 exact head `44d6f7deab2349ed879e9d7a1c12cb88872fb283` completed 45/45 workflows successfully before merging as `30fab12f4e5978f1e5f7f1007a221239d604a8bb`.

## Object-storage remediation — internal gate accepted

RUN-131 through RUN-134 established and implemented the supported object-storage contract. Commercial entitlement/support, production topology, deployment-time image digest verification, TLS/SSE/KMS, secrets-manager acceptance and production deployment remain external/open.

## Phase 1 — CI and workflow integrity

Current decision: `PASS`.

## Phase 2 — Application security and identity

Current decision: `PASS` for internal gates.

## Phase 3 — Data integrity and recovery

Current decision: `PASS` for internal gates; full representative external restore acceptance remains in issue #1.

## Phase 4 — Live connector reliability and provenance

Current decision: `PASS` for internal gates.

## Phase 5 — Performance and scalability

Current decision: `PASS` for bounded internal gates; representative production load/stress remains external.

## Phase 6 — Frontend accessibility and operational UX

Current decision: `BLOCKED_EXTERNAL` only for genuine VoiceOver/NVDA evidence on supported real host/browser/screen-reader combinations. Browser/DOM automation is not a substitute.

## Phase 7 — Observability and incident operations

Current decision: `PASS`.

Internal observability, alerting, dashboard, runbook, exercise and on-call handover gates are accepted. The operator/project authority confirmed all six external human operational-acceptance evidence classes were accepted, with sensitive underlying records retained outside source control.

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

PR #101 exact head `fd87beb441c4e4ed71141ea9ae03717e859681e3` completed 46/46 registered workflows successfully. Retained artifact `9043667776`, digest `sha256:62287683401694c130144873e7b0ac1c55f565c4e518dcb379e4b6e9bc56b564`, was exact-head bound with machine-readable PASS and JUnit 3/3. PR #101 merged as `5f74bcac92738febfe327ea78f45c009d28e4d55`.

The baseline proves only the staging acceptance contract; its retained claim boundary correctly states that no staging environment, deployment parity or staging test execution was proven.

### RUN-148 staging environment and deployment-parity acquisition — `BLOCKED_EXTERNAL`

Live repository and issue #1 inspection found no real staging endpoint/environment identifier or immutable deployment-parity evidence. Phase 8 cannot proceed to acceptance suites until all of the following are retained against one staging deployment identity:
1. approved staging environment identifier and accountable owner;
2. reachable staging endpoint via the approved access path;
3. immutable deployed application/container image digests and release identity;
4. infrastructure/runtime versions and configuration-parity evidence;
5. approved secrets-manager/identity references and least-privilege staging identities, with no secret values committed;
6. TLS certificate/termination and network-restriction evidence;
7. production-equivalent data-class/sanitization statement and no-production-credential confirmation;
8. deployment log/change record tied to the immutable release identity;
9. rollback target/procedure tied to the staged release;
10. deployment-time security/CVE/vendor-advisory review evidence.

Repository CI cannot substitute for this real environment evidence. Until the gate is supplied, no smoke/integration/migration/connector/recovery/performance/accessibility/observability staging result can be accepted.

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
# DTMO Production Readiness Roadmap

## Purpose

This roadmap defines the controlled path from DTMO's release-candidate state to production readiness. It is executed through bounded PDCA runs and tracked in GitHub issue #3. No phase is complete without objective evidence; missing CI, security, recovery, performance, accessibility, operational or external-assurance evidence blocks the corresponding claim.

## Current status — 2026-08-10

- Phase 1 — CI and workflow integrity: `PASS`.
- Phase 2 — Application security and identity: `PASS` for internal gates.
- Phase 3 — Data integrity and recovery: `PASS` for internal gates.
- Phase 4 — Live connector reliability and provenance: `PASS` for internal gates.
- Phase 5 — Performance and scalability: `PASS` for internal gates.
- Phase 6 — Frontend accessibility and operational UX: `BLOCKED_EXTERNAL` only for genuine VoiceOver/NVDA execution on supported real hosts.
- Phase 7 — Observability and incident operations: `PASS`.
- Phase 8 — Staging acceptance: `BLOCKED_EXTERNAL` for real deployment-parity evidence. Repository-controlled staging-emulator configuration and bounded application-container runtime smoke are `PASS` only for their explicit scopes.
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
- no unresolved blocker interpreted as PASS.

### Accepted repository-controlled evidence

- RUN-147 staging-readiness baseline: `PASS`.
- RUN-151/RUN-152 staging emulator configuration contract: `PASS`; PR #104 final exact head `93d1a659b7b136546ffcf73102890f5d2d00ba84` completed 47/47 workflows. This proves source-controlled configuration/topology only.
- RUN-153/RUN-154 documentation/lifecycle reconciliation: `PASS`; PR #106 final exact head `ff0a490e46c2f9529441d8a5294030af498dbe14` completed 47/47 workflows and merged as `b57a6daa775d2f1f88a2d1b67b191da757fa743f`.
- RUN-155 bounded application-container runtime smoke: `PASS`; PR #107 exact head `52d7a37660c9bb1c9f8468f11010f36d17bd1fba` completed 48/48 workflows and merged as `23d629964f55709845683e808f707998cc8d4aa2`. This does not execute the complete dependency topology or prove real staging.
- RUN-157 lifecycle-regression remediation: `PASS`; PR #108 exact head `25ac24bfa40f2f9ccebb5d1307615c6fbd14cf05` completed 48/48 workflows after the stale lifecycle assertion was repaired. Its documentation-finalization exact head `bbba29a1269b5c09d1a94a27b38c317bae2590e7` also completed 48/48 workflows and merged as `de3561b42f8e4fec5947182e01563a6327d0e029`.

### Real staging deployment-parity blocker

RUN-148, RUN-150, RUN-156 and RUN-158 all found no approved real staging environment/deployment identity and no complete package satisfying the ten required deployment-parity evidence classes against one immutable staged release. RUN-158 repeated that check after PR #108 became authoritative on `main`; issue #1's unchecked external acceptance gates remain unchanged.

Required classes remain: approved environment/owner; reachable endpoint; immutable deployed release/image identity; infrastructure/runtime/configuration parity; approved secrets-manager and least-privilege identities; TLS/network restrictions; staging data-class/sanitization and no-production-credential confirmation; deployment/change record; rollback target/procedure; and deployment-time security/CVE/vendor-advisory review.

Evidence class 10 must be performed against the actual immutable staged release and preserve source provenance, review time and confidence. A generic pre-deployment threat/advisory review does not close the class.

No staging acceptance result is credited until all ten classes are complete against the same deployment identity.

## Phase 9 — External assurance

Tracked in issue #1: independent penetration test, representative load/stress, full backup/restoration exercise, production platform hardening, required secrets-management acceptance, operational/stakeholder approvals and production deployment acceptance.

## Phase 10 — Production go/no-go

Go requires every prior phase and external gate complete with retained evidence, green CI, release notes/SBOM/deployment manifest/rollback plan, proven recovery and required approvals. Any missing blocking evidence is `NO-GO`.

## PDCA execution order

1. CI and workflow integrity.
2. Application security and identity.
3. Data integrity and recovery.
4. Live connector reliability and provenance.
5. Performance and scalability.
6. Frontend accessibility and operational UX.
7. Observability and incident operations.
8. Staging acceptance.
9. External assurance coordination.
10. Production go/no-go.

Every run must document Plan, Do, Check and Act, update run/QA evidence, preserve claim boundaries, and leave exactly one next priority.

## Exactly one next priority

Provide or provision one approved real staging deployment and retain all ten deployment-parity evidence classes against the same immutable deployment identity. Do not begin or credit the staging acceptance suite before that gate is complete.

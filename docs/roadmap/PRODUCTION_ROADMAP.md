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
- Phase 9 — External assurance: `NOT COMPLETE`; RUN-159 defines the repository-controlled intake/readiness contract and is `CI_VALIDATION_PENDING`.
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

Accepted repository-controlled evidence includes RUN-147 readiness, RUN-151/152 emulator configuration, RUN-153/154 lifecycle reconciliation, RUN-155 bounded application-container runtime smoke and RUN-157 lifecycle remediation. PR #109 exact head `fca605acd1e97bd7531967ada080e35ac4ea6a4b` completed 48/48 workflows and merged as `48dace96c389703130457ed61e639477ace5398b`, making RUN-158 authoritative on `main`.

RUN-148, RUN-150, RUN-156 and RUN-158 found no approved real staging environment/deployment identity and no complete package satisfying the ten required deployment-parity classes against one immutable staged release. Required classes remain: approved environment/owner; reachable endpoint; immutable deployed release/image identity; infrastructure/runtime/configuration parity; approved secrets-manager and least-privilege identities; TLS/network restrictions; staging data-class/sanitization and no-production-credential confirmation; deployment/change record; rollback target/procedure; and deployment-time security/CVE/vendor-advisory review.

No staging acceptance result is credited until all ten classes are complete against the same deployment identity. Evidence class 10 must preserve public-source provenance, review time, applicability and confidence against the actual immutable staged release/platform.

## Phase 9 — External assurance

Phase 9 requires independently observable evidence for:
- independent penetration testing against the approved target deployment;
- representative load/stress testing with documented workload assumptions and thresholds;
- full backup/restoration exercise with integrity and RPO/RTO observations;
- production platform hardening, including OpenSearch/security, TLS/network and runtime controls;
- approved secrets-management acceptance and least-privilege identities;
- operational/stakeholder acceptance by accountable service owner and required security/privacy roles;
- staging and production deployment acceptance tied to immutable release/deployment identities and rollback targets.

### RUN-159 external-assurance intake baseline — `CI_VALIDATION_PENDING`

Because Phase 8 is blocked solely by external staging evidence, RUN-159 advances only the next internally executable preparation task. `docs/qa/PHASE9_EXTERNAL_ASSURANCE_GATE.md` defines the evidence intake and claim-boundary contract. It requires attributable, dated, independently observable evidence; immutable target identity where applicable; explicit finding disposition; privacy-safe retention; separation between review and human share approval; and no secret values in source control.

Where assurance depends on deployed software/platform state, the evidence package must include a time-bounded review of relevant public threat intelligence, CVE data and vendor advisories, preserving source provenance, review time, applicability and confidence. This readiness contract does not prove any external assurance activity has occurred. Issue #1 remains authoritative for completion state.

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

Verify every registered workflow on the RUN-159 PR exact head and merge only on complete success. After merge, acquire the first missing independent assurance evidence class in issue #1 without treating absent external execution as PASS.

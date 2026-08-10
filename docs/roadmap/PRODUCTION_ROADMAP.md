# DTMO Production Readiness Roadmap

## Purpose

This roadmap defines the controlled path from DTMO's release-candidate state to production readiness. It is executed through bounded PDCA runs and tracked in GitHub issue #3. No phase is complete without objective evidence; missing CI, security, recovery, performance, accessibility, operational or external-assurance evidence blocks the corresponding claim.

## Current status — 2026-08-10

- Phase 1 — CI and workflow integrity: `PASS`.
- Phase 2 — Application security and identity: `PASS` for internal gates.
- Phase 3 — Data integrity and recovery: `PASS` for internal gates.
- Phase 4 — Live connector reliability and provenance: `PASS` for internal gates.
- Phase 5 — Performance and scalability: `PASS` for internal gates.
- Phase 6 — Frontend accessibility and operational UX: genuine VoiceOver/NVDA execution remains `BLOCKED_EXTERNAL`; RUN-161 introduces the 16.0.0rc5 governed root console and is `CI_VALIDATION_PENDING`.
- Phase 7 — Observability and incident operations: `PASS`.
- Phase 8 — Staging acceptance: `BLOCKED_EXTERNAL` for real deployment-parity evidence. Repository-controlled staging-emulator configuration and bounded application-container runtime smoke are `PASS` only for their explicit scopes.
- Phase 9 — External assurance: `NOT COMPLETE`; the repository-controlled intake/readiness baseline is accepted from PR #110 exact-head evidence.
- Phase 10 — Production go/no-go: `NOT STARTED`.

## Phase 6 — Frontend accessibility and operational UX

Repository-controlled critical journeys, responsive layout, keyboard navigation, contrast, reflow, focus order, text spacing/resize and share-approval controls have historical accepted evidence. Genuine assistive-technology execution on supported VoiceOver/NVDA host/browser combinations remains externally required.

### RUN-161 — 16.0.0rc5 frontend productionization — `CI_VALIDATION_PENDING`

The prior application exposed role-specific UI routes but returned 404 at `/`, making a successful Docker deployment appear to have no application interface. RUN-161 adds a governed DTMO Console at `/` and `/ui/console` with runtime status, connector visibility, intelligence search, review/share governance, read-only audit evidence and CISO token revocation.

The console preserves server-side RBAC and separation of duties. Browser control visibility is convenience only and never substitutes for authorization. Test identity data is limited to per-tab `sessionStorage`; bearer tokens are not persisted. CSP, no-store handling, visible focus, skip navigation, responsive reflow, live status regions and reduced-motion behavior are required by `docs/qa/FRONTEND_RELEASE_GATE.md`.

RUN-161 also repairs the local external-test startup contract by explicitly passing `OPENSEARCH_INITIAL_ADMIN_PASSWORD` to OpenSearch and documenting the external secret input. No real secret value may enter source control.

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

Accepted repository-controlled evidence includes RUN-147 readiness, RUN-151/152 emulator configuration, RUN-153/154 lifecycle reconciliation, RUN-155 bounded application-container runtime smoke and RUN-157 lifecycle remediation. RUN-148, RUN-150, RUN-156 and RUN-158 found no approved real staging environment/deployment identity and no complete ten-class deployment-parity package.

Required classes remain: approved environment/owner; reachable endpoint; immutable deployed release/image identity; infrastructure/runtime/configuration parity; approved secrets-manager and least-privilege identities; TLS/network restrictions; staging data-class/sanitization and no-production-credential confirmation; deployment/change record; rollback target/procedure; and deployment-time security/CVE/vendor-advisory review.

No staging acceptance result is credited until all ten classes are complete against the same deployment identity.

## Phase 9 — External assurance

Phase 9 requires independently observable evidence for:
- independent penetration testing against the approved target deployment;
- representative load/stress testing with documented workload assumptions and thresholds;
- full backup/restoration exercise with integrity and RPO/RTO observations;
- production platform hardening, including OpenSearch/security, TLS/network and runtime controls;
- approved secrets-management acceptance and least-privilege identities;
- operational/stakeholder acceptance by accountable service owner and required security/privacy roles;
- staging and production deployment acceptance tied to immutable release/deployment identities and rollback targets.

### RUN-159 external-assurance intake baseline — `PASS` for readiness contract only

PR #110 exact head `5549ac1f28307c8bfa8c2ea1bf39341bb33983a0` completed all 48 registered workflows successfully and merged as `0b9a6d51dcd6e4fa984888d172e1fb5f5d6d52f2`. `docs/qa/PHASE9_EXTERNAL_ASSURANCE_GATE.md` defines the evidence intake and claim-boundary contract. No external assurance execution is implied.

## Phase 10 — Production go/no-go

Go requires every prior phase and external gate complete with retained evidence, green CI, release notes/SBOM/deployment manifest/rollback plan, proven recovery and required approvals. Any missing blocking evidence is `NO-GO`.

## Documentation baseline

The production-readiness program is supported by `docs/README.md`, executive status, production-readiness report, production checklist, evidence index, traceability matrix, lessons learned, architecture/security/operations documentation, ADRs, detailed QA documents and PDCA run records.

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

Verify every registered workflow on the final 16.0.0rc5 frontend PR head and merge only on complete success. After acceptance, return to the first missing external assurance class without treating absent external execution as PASS.

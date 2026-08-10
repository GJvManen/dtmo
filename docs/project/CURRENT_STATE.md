# DTMO Current Project State

Last reconciled: 2026-08-10 — RUN-20260810-161 (`CI_VALIDATION_PENDING`; 16.0.0rc5 frontend productionization).

## Executive status

- Phase 1 — CI/workflow integrity: `PASS`.
- Phase 2 — application security and identity: `PASS` for internal roadmap gates.
- Phase 3 — data integrity and recovery: `PASS` for internal roadmap gates.
- Phase 4 — connector reliability and provenance: `PASS` for internal roadmap gates.
- Phase 5 — performance and scalability: `PASS` for internal roadmap gates.
- Phase 6 — frontend accessibility and operational UX: repository-controlled browser/accessibility gates are accepted historically; genuine VoiceOver/NVDA behavior remains `BLOCKED_EXTERNAL`.
- Phase 7 — observability and incident operations: `PASS`.
- Phase 8 — staging acceptance: `BLOCKED_EXTERNAL` for one approved real staging deployment and the ten deployment-parity evidence classes. Repository-controlled emulator configuration and bounded application-container runtime smoke are `PASS` only for their explicit scopes.
- Phase 9 — external assurance: `NOT COMPLETE`; the repository-controlled external-assurance intake/readiness contract is accepted on `main`.
- Phase 10 — production go/no-go: `NOT STARTED`.

DTMO is **not production ready**. Issue #1 remains authoritative for external production-acceptance gates.

## 16.0.0rc5 frontend candidate

RUN-161 introduces a governed operational web console at `/` and `/ui/console`. The console consolidates runtime health/version/environment, connector status, role-aware intelligence search, governed review/share decisions, read-only audit evidence and CISO token revocation while retaining the existing dedicated role surfaces.

The browser UI is not an authorization boundary. Every protected operation remains enforced by the existing server-side RBAC dependencies. Review and external share approval remain separate governed decisions. Local/dev/staging test identity material is held only in per-tab `sessionStorage`; the console does not persist bearer tokens. Production authentication remains the configured bearer-token/identity-provider path.

The candidate also fixes the documented local Compose startup contract by passing externally supplied `OPENSEARCH_INITIAL_ADMIN_PASSWORD` into the OpenSearch container and documenting the corresponding `.env` input. Real passwords, API keys, AIStor license material and image digests remain outside source control.

`docs/qa/FRONTEND_RELEASE_GATE.md` defines the exact claim boundary. RUN-161 is not PASS until every registered workflow succeeds on the final exact PR head.

## Latest accepted Phase 9 baseline

PR #110 exact head `5549ac1f28307c8bfa8c2ea1bf39341bb33983a0` completed all 48 registered workflows successfully and merged as `0b9a6d51dcd6e4fa984888d172e1fb5f5d6d52f2`. RUN-159 is accepted only for its bounded external-assurance intake/readiness contract; it does not prove external assurance execution.

## Phase 8 blocker

No approved real staging endpoint/environment identity and no complete ten-class deployment-parity package tied to one immutable staged release are available. Required classes remain: approved environment/owner; reachable endpoint; immutable deployed release/image identity; infrastructure/runtime/configuration parity; approved secrets-manager and least-privilege identities; TLS/network restrictions; staging data-class/sanitization and explicit no-production-credential confirmation; deployment/change record; rollback target/procedure; and deployment-time security/CVE/vendor-advisory review.

No staging acceptance result may be credited until those classes are complete against the same immutable identity.

## Phase 9 external assurance

The accepted Phase 9 intake contract requires independently observable evidence for independent penetration testing, representative load/stress testing, full backup/restoration, production platform hardening, secrets-management acceptance, operational/stakeholder acceptance and staging/production deployment acceptance. Evidence must be attributable, dated and tied to immutable target identities where applicable. Findings require explicit disposition.

## Extended documentation baseline

`main` contains the consolidated documentation index, executive status, production-readiness report, production checklist, evidence index, traceability matrix, lessons learned, ADRs, architecture overview, security overview and operations manual in addition to detailed QA and PDCA records.

## Security and governance invariants

RBAC, separation of duties, privacy, provenance, auditability and human share approval remain unchanged. Technical environment access cannot grant publication or share approval. Missing, stale, inaccessible, inferred, failed, cancelled, skipped or contradictory evidence is never PASS.

## Exactly one current priority

Complete exact-head CI and browser/accessibility validation for the 16.0.0rc5 frontend release candidate. Merge only if every registered workflow succeeds; otherwise remediate the first concrete failing gate.

# DTMO Current Project State

Last reconciled: 2026-08-09 — RUN-20260809-135 (`CI_VALIDATION_PENDING`; RC10.5 API-error alerting implemented but not yet accepted)

## Executive status

- Phase 1 — CI/workflow integrity: `PASS`.
- Phase 2 — application security and identity: `PASS` for internal roadmap gates.
- Phase 3 — data integrity and recovery: `PASS` for internal roadmap gates.
- Phase 4 — connector reliability and provenance: `PASS` for internal roadmap gates.
- Phase 5 — performance and scalability: `PASS` for internal roadmap gates.
- Phase 6 — frontend accessibility and operational UX: `BLOCKED_EXTERNAL` only for genuine VoiceOver/NVDA behavior.
- Phase 7 — observability and incident operations: `IN PROGRESS`; RC10.1–RC10.4 and the internal object-storage migration/reconciliation are accepted; RC10.5 is `CI_VALIDATION_PENDING`.
- Phase 8 — staging acceptance: `NOT STARTED`.
- Phase 9 — external assurance: `NOT COMPLETE`.
- Phase 10 — production go/no-go: `NOT STARTED`.

DTMO is **not production ready**. Issue #1 remains authoritative for external production-acceptance gates.

## Latest accepted reconciliation

PR #91 exact head `d81caaa372b0cf3e079023eb255a57fd4892d6e0` completed **38/38 registered workflows successfully** and was merged with expected-head protection as `23af430c041e3f0e203b7a7f7a6c69f3eea79055`.

The bounded object-storage migration remains accepted from PR #90 exact head `0fe5c5f0003211fe9df8535954d9276a2090af35`, 38/38 workflows, artifact `9041774769`, digest `sha256:24e7241138dc0b293957f5e2cd06a4d3a6606b7ba68d688097795047f114ccf8`, JUnit 4/4.

## RC10.5 API-error alerting

RUN-135 implements:

- normalized route-template-only API error observation;
- 3 consecutive HTTP 5xx outcomes to raise;
- 2 consecutive non-5xx outcomes to clear an active alert;
- repeat-raise suppression;
- bounded request-result/streak/active-state/transition metrics;
- `DTMOApiServerErrors` Prometheus rule;
- safe correlation and actionable structured evidence with `publish_approved=false`;
- middleware coverage for returned status codes and unhandled exception/500 outcomes;
- controlled privacy tests asserting synthetic path/query values do not enter Prometheus alert evidence;
- an independently observable `RC10 API Error Alerting Gate` retaining JUnit/log/machine-readable exact-head evidence.

The implementation remains `CI_VALIDATION_PENDING`. Missing, queued, cancelled, failed or unexecuted CI is not PASS.

## Fresh security/advisory boundary

Fresh dependency review identified Starlette CVE-2026-48817 and CVE-2026-48818 as affecting versions through 1.0.1 and fixed in 1.1.0. DTMO does not directly pin Starlette, so this is recorded as dependency provenance rather than an exploitability claim. Exact dependency resolution and security scanning remain CI acceptance gates.

Production AIStor selection remains subject to the RUN-134 release/advisory floor and a fresh deployment-time advisory review.

## External gates still open

Paid AIStor entitlement/support, production topology, deployment-time registry digest verification, secrets-manager acceptance, production TLS/SSE/KMS, staging/production deployment acceptance, penetration testing, representative load/stress, full backup/restoration, production OpenSearch hardening and operational/stakeholder approvals remain open in issue #1 or the applicable external acceptance process.

## Security and governance invariants

- RBAC remains enforced.
- Review and share approval remain separate human actions.
- Connectors and service accounts cannot approve publication.
- API alerting cannot approve publication and reports `publish_approved=false`.
- API alert labels use normalized route templates, not request URLs/query strings.
- Provenance, confidence and raw-evidence controls remain unchanged.
- License/API/admin/application credentials must not enter source control or telemetry.
- Missing, queued, cancelled, failed or unexecuted CI is never `PASS`.

## Exactly one current priority

Verify the complete exact-head workflow matrix and retained `api-error-alerting-evidence` artifact for RUN-135; merge only after every registered workflow succeeds and retained evidence is exact-head bound and internally consistent.

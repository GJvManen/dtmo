# DTMO Current Project State

Last reconciled: 2026-08-09 — RUN-20260809-139 (`CI_VALIDATION_PENDING`; RC10.7 accepted, operational dashboard implemented but not yet accepted)

## Executive status

- Phase 1 — CI/workflow integrity: `PASS`.
- Phase 2 — application security and identity: `PASS` for internal roadmap gates.
- Phase 3 — data integrity and recovery: `PASS` for internal roadmap gates.
- Phase 4 — connector reliability and provenance: `PASS` for internal roadmap gates.
- Phase 5 — performance and scalability: `PASS` for internal roadmap gates.
- Phase 6 — frontend accessibility and operational UX: `BLOCKED_EXTERNAL` only for genuine VoiceOver/NVDA behavior.
- Phase 7 — observability and incident operations: `IN PROGRESS`; RC10.1–RC10.7 and the internal object-storage migration/reconciliation are accepted; RC10.8 is `CI_VALIDATION_PENDING`.
- Phase 8 — staging acceptance: `NOT STARTED`.
- Phase 9 — external assurance: `NOT COMPLETE`.
- Phase 10 — production go/no-go: `NOT STARTED`.

DTMO is **not production ready**. Issue #1 remains authoritative for external production-acceptance gates.

## Latest accepted evidence

RC10.7 / PR #94 exact head `5a2f60749f6eaf6ece9dcfcc3b70c866887c6cb8` completed **41/41 registered workflows successfully** after RUN-138 fixed the first-head lint blocker without scanner suppression. Artifact `9042398103`, digest `sha256:2014a035338de6bc6ac474581279c06c15cafc6a49f3c86cfbeed111e666575a`, was exact-head bound and independently showed machine-readable PASS plus JUnit 10/10. PR #94 merged as `e52af08204d212cdfba0e9338bacb7a1c5fcfac7`.

## RC10.8 operational dashboard

RUN-139 implements an opt-in Grafana observability overlay and source-controlled `DTMO Operations` dashboard over existing bounded Prometheus telemetry. The dashboard is provisioned read-only and covers HTTP request rate/p95/in-flight, API alerting, connector alerting/outcomes, queue utilization, storage-integrity alerts, search-health alerts and bounded trace-context decisions.

The overlay disables anonymous access, user sign-up and organization creation; binds local port 3000 to loopback; requires externally supplied Grafana admin credentials; and fails closed unless the deployer supplies a supported security-patched `grafana/grafana` image pinned by vendor-verified sha256 digest. No production credentials or fixed assumed-safe Grafana version are stored in source.

The implementation remains `CI_VALIDATION_PENDING`. Missing, queued, cancelled, failed or unexecuted CI is not PASS.

## Fresh security/vendor boundary

First-party Grafana security review identified 2026 advisories including CVE-2026-27876, CVE-2026-28383 and CVE-2026-21721. These reinforce that the observability plane is privileged infrastructure and that deployment-time release/advisory review and digest verification are mandatory.

Production Grafana deployment, SSO/RBAC integration, TLS/network restrictions and lifecycle acceptance are not claimed by RC10.8.

## External gates still open

Paid AIStor entitlement/support, production topology, deployment-time registry digest verification, secrets-manager acceptance, production TLS/SSE/KMS, production Grafana/OpenSearch hardening, staging/production deployment acceptance, penetration testing, representative load/stress, full backup/restoration and operational/stakeholder approvals remain open in issue #1 or the applicable external acceptance process.

## Security and governance invariants

- RBAC remains enforced.
- Review and share approval remain separate human actions.
- Connectors, observability components and service accounts cannot approve publication.
- Dashboard queries use bounded operational metrics and exclude raw request/response bodies, raw URLs/query strings, credentials, identities, object keys and checksums.
- Provenance/confidence controls remain unchanged.
- Missing, queued, cancelled, failed or unexecuted CI is never `PASS`.

## Exactly one current priority

Verify the complete exact-head workflow matrix and retained `operational-dashboard-evidence` artifact for RUN-139; merge only after every registered workflow succeeds and retained evidence is exact-head bound and internally consistent.

# DTMO Current Project State

Last reconciled: 2026-08-10 — 16.0.0rc10 RC10.2 / PR #117 is accepted and merged; RUN-20260810-178 executes RC10.3 Threat Intelligence Workspace.

## Executive status

- Phase 1 — CI/workflow integrity: `PASS`.
- Phase 2 — application security and identity: `PASS` for internal roadmap gates.
- Phase 3 — data integrity and recovery: `PASS` for internal roadmap gates.
- Phase 4 — connector reliability and provenance: `PASS` for the accepted built-in and governed registered-source execution baseline.
- Phase 5 — performance and scalability: `PASS` for internal roadmap gates.
- Phase 6 — frontend accessibility and operational UX: RC10.1 and RC10.2 are accepted; RC10.3 is `CI_VALIDATION_PENDING`. Genuine VoiceOver/NVDA remains `BLOCKED_EXTERNAL`.
- Phase 7 — observability and incident operations: `PASS` for internal gates.
- Phase 8 — staging acceptance: `BLOCKED_EXTERNAL` for one approved real staging deployment and the ten deployment-parity evidence classes.
- Phase 9 — external assurance: `NOT COMPLETE`.
- Phase 10 — production go/no-go: `NOT STARTED`.

DTMO is **not production ready**. Issue #1 remains authoritative for external production-acceptance gates.

## Accepted RC10.2 baseline

PR #117 exact head `d4e35a5fa0c463438299d6cdd3638de162a69026` completed every registered workflow successfully and merged as `db9e72d871fb1c4d536912419ffbb4d68ad680c2`.

## RUN-178 / RC10.3

RC10.3 adds `/ui/intelligence-workspace`, reuses the accepted RBAC-protected `/api/v1/intelligence/search` path and adds GET-only `/api/v1/intelligence/{item_id}/workspace` for canonical investigation detail.

The detail projection exposes only stored canonical title/summary/source/severity/confidence/education relevance/review/share state, tags, bounded safe metadata and provenance. Explicit CVE identifiers are extracted from stored canonical text/tags. `known_exploited` is asserted only when the stored source is `cisa-kev`; vendor/product are shown only when explicitly present in stored metadata. Missing context is never invented.

The workspace adds no review, share-approval, source-management, connector-run, admin or security mutation authority. Existing server-side RBAC, human review, separate share approval and audit controls remain authoritative.

## External blockers

No approved real staging endpoint/environment identity and no complete ten-class deployment-parity package tied to one immutable release are available. Genuine assistive-technology execution, independent penetration testing and remaining external assurance also remain absent.

## Exactly one current priority

Complete exact-head CI validation for RUN-178 / RC10.3. Merge only on complete success; otherwise remediate the first concrete failing root cause only.

# DTMO Current Project State

Last reconciled: 2026-08-10 — 16.0.0rc8 / PR #114 is accepted and merged. RUN-20260810-172 / 16.0.0rc9 implements the next bounded priority: safe registered JSON-source execution plus a curated intelligence-source catalog.

## Executive status

- Phase 1 — CI/workflow integrity: `PASS`.
- Phase 2 — application security and identity: `PASS` for internal roadmap gates.
- Phase 3 — data integrity and recovery: `PASS` for internal roadmap gates.
- Phase 4 — connector reliability and provenance: built-in CISA KEV remains accepted; rc9 extends the source plane with safe NVD/GitHub/generic JSON execution and is `CI_VALIDATION_PENDING`.
- Phase 5 — performance and scalability: `PASS` for internal roadmap gates.
- Phase 6 — frontend accessibility and operational UX: rc6 remains the accepted professional UX baseline and rc8 the accepted admin registry baseline; genuine VoiceOver/NVDA remains `BLOCKED_EXTERNAL`.
- Phase 7 — observability and incident operations: `PASS`.
- Phase 8 — staging acceptance: `BLOCKED_EXTERNAL` for one approved real staging deployment and the ten deployment-parity evidence classes.
- Phase 9 — external assurance: `NOT COMPLETE`.
- Phase 10 — production go/no-go: `NOT STARTED`.

DTMO is **not production ready**. Issue #1 remains authoritative for external production-acceptance gates.

## Accepted rc8 baseline

PR #114 final exact head `95fed1e663bdf256def58020f11529f383c8efe5` completed all 48 registered workflows successfully and merged as `7351ae2ab984b6848969bc634c32e819ec413031`. Persistent human-admin source lifecycle, secret references, audit events and registration-time URL validation are accepted within repository-controlled scope.

## RUN-172 / 16.0.0rc9

rc9 adds a second, runtime SSRF boundary instead of relying on registration syntax alone. Every generic source request is freshly DNS-resolved, rejects the complete answer set if any destination is non-global, and connects to one validated IP while retaining the configured hostname for TLS SNI and certificate validation. Redirects are rejected, environment proxies are not used, only JSON is accepted and bodies are capped at 5 MiB.

Supported normalizers now cover NIST NVD CVE API 2.0 and GitHub Global Security Advisories. Unknown governed JSON sources must follow the explicit DTMO JSON v1 `items[]` schema. Records enter the existing raw-object, canonical database, provenance and OpenSearch path, repeated execution remains idempotent/search-repairable, and source results feed connector health/failure isolation plus alert state. Manual execution remains human-admin-only and cannot grant review or external share approval.

The code-reviewed catalog currently covers CISA KEV, NVD, GitHub, NCSC-NL, CERT-EU, Microsoft MSRC, Cisco, Red Hat, Ubuntu, Debian, Apple, Chrome, Mozilla, Fortinet, Palo Alto, Broadcom/VMware and ENISA. Project documentation additionally records School-CERT/Kennisnet and SURF/SURFcert as high-value education-sector onboarding targets subject to approved interfaces and distribution conditions. Catalog breadth is not confused with executable-parser breadth.

## Public threat/source review

First-party review on 2026-08-10 confirms CISA KEV remains the authoritative CISA list of vulnerabilities exploited in the wild; NIST documents NVD CVE API 2.0 as a JSON REST service; GitHub documents public global security-advisory API access; NCSC-NL distributes public Security Advisories including machine-readable CSAF and RSS; CERT-EU publishes public technical security advisories; MSRC maintains the Security Update Guide. School-CERT and SURF public 2025 threat pictures remain directly relevant to education-sector prioritisation and historical incident learning.

## Open maintenance finding

The previously recorded OpenSearch 2.19.1 patch-maintenance finding remains open and separate. If a new vendor advisory makes it higher severity than the active objective, roadmap ordering must be interrupted accordingly.

## External blockers

No approved real staging endpoint/environment identity and no complete ten-class deployment-parity package tied to one immutable release are available. Genuine assistive-technology execution, independent penetration testing and remaining external assurance also remain absent. Missing external evidence is never inferred from repository CI.

## Exactly one current priority

Complete exact-head CI validation for RUN-172 / 16.0.0rc9. Merge only on complete success; otherwise remediate the first concrete failure. After acceptance, the next product priority is integration of the existing graphical/operational dashboard building blocks into the professional console.

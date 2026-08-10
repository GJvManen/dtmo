# RC10.3 Threat Intelligence Workspace Gate

Status: `CI_VALIDATION_PENDING`

## Scope

Repository-controlled acceptance for the RC10.3 investigation workspace only.

## Required evidence

- `/ui/intelligence-workspace` is wired into the application;
- search reuses the accepted `/api/v1/intelligence/search` path and existing `READ_INTELLIGENCE` authorization;
- canonical detail is GET-only at `/api/v1/intelligence/{item_id}/workspace` and also requires `READ_INTELLIGENCE`;
- result/detail presentation includes stored title, summary, source, severity, confidence, education relevance, review/share state and provenance;
- explicit CVE identifiers may be extracted from stored canonical text/tags, but missing context is not invented;
- `known_exploited` is asserted only for records whose stored source is `cisa-kev`;
- vendor/product are shown only when explicitly present in stored metadata;
- raw object-storage metadata, credentials, request/response bodies, cookies, authorization values and student identifiers are not exposed;
- the workspace contains no review, share-approval, connector/admin or token-revocation mutation path;
- local/dev/staging identity remains per-tab sessionStorage only; server-side RBAC remains authoritative;
- all registered GitHub workflows succeed on one final exact PR head.

## Claim boundary

A PASS proves repository implementation and regression contracts only. It does not prove live source completeness, external enrichment quality, genuine VoiceOver/NVDA execution, real staging parity, independent penetration testing, external assurance or production readiness.

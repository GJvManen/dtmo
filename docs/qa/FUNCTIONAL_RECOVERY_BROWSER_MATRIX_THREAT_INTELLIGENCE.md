# Functional Recovery Browser Matrix — Threat Intelligence

## Status

`EXACT-HEAD CI REQUIRED`

This slice continues the owner-driven post-recovery functional retest after the canonical route/Administration matrix merged in PR #337.

## Acceptance contract

The canonical `/workbench/intelligence` journey must be proven against the real built workbench, same-origin DTMO APIs and temporary PostgreSQL persistence without Playwright route interception or fabricated API responses.

The exact-head browser journey seeds one visibly repository-controlled intelligence fixture directly into temporary DTMO persistence and verifies that the canonical Threat Intelligence page:

- renders the persisted record in **Recent canonical intelligence**;
- opens the real `/api/v1/intelligence/{id}/workspace` detail path;
- displays server-derived source, severity, confidence, education relevance, review and sharing state;
- exposes canonical Analysis & Enrichment and Sharing & Exchange pivots carrying only the persisted object identifier;
- contains no `/ui/*` compatibility link in the exercised canonical journey.

The fixture is removed after the browser journey. It is repository-controlled acceptance data, not live threat intelligence and not source-health evidence.

## Evidence boundary

This is repository-controlled exact-head functional evidence only. It does not execute external connectors and does not constitute owner acceptance, staging evidence, production-equivalent validation, penetration-test evidence, production authorization or independent external assurance.

## Security and authority boundaries

The journey is read-only from the browser perspective. It does not grant review, share approval, publication, analyzer execution, connector execution, case creation, remediation or external-assurance authority. Server-side RBAC, provenance, fail-closed behavior and credential boundaries remain authoritative.

## Next after green

Continue Threat Intelligence with the next bounded real journey: governed search/filter behavior against a real search projection, or fix the first exact-head blocker exposed by this slice before proceeding to IOC Explorer.

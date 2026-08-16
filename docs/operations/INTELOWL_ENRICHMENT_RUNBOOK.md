# IntelOwl Enrichment Operations Runbook

State: **`IMPLEMENTED / EXACT-HEAD VALIDATION REQUIRED`**  
Last reviewed: **2026-08-16**

## Scope

Operational guidance for the governed Phase 11.3 IntelOwl execution/persistence boundary. This runbook does not authorize production use and does not replace Phase 11.10 production-equivalent validation or Phase 11.11 independent external assurance.

## Enablement and secrets

The feature is disabled by default. Enable only with an approved HTTPS IntelOwl API base, a runtime-secret API token and a non-empty analyzer allowlist. Never store the token in repository files, screenshots, CI artifacts or evidence bundles.

Required production-controlled settings are `DTMO_FEATURE_INTELOWL_ENRICHMENT`, `DTMO_INTELOWL_API_BASE`, `DTMO_INTELOWL_API_TOKEN`, `DTMO_INTELOWL_ALLOWED_ANALYZERS`, polling bounds and result-size limits. The existing connector timeout bounds the HTTP client.

## Health and failure interpretation

A policy rejection means no external disclosure was permitted. An upstream HTTP error is dependency failure and must not be converted into successful enrichment evidence. Poll exhaustion means the bounded job did not reach a terminal state; do not infer completion. Unknown analyzer, malformed/oversized result or job-id mismatch is a fail-closed integrity event.

## Persistence checks

Each completed accepted execution creates one `intelowl_enrichment_records` row linked to an existing canonical intelligence item. `(item_id, job_id)` is unique. Confirm `external_share_authorized=false` and `local_compromise_proven=false` remain unchanged. A repeated persistence attempt for the same item/job returns the existing immutable record rather than inventing another evidence event.

## Operational triage

1. Confirm the caller is a human principal with `REVIEW_INTELLIGENCE`.
2. Confirm feature flag, HTTPS API base, runtime token and analyzer allowlist are controlled.
3. Confirm the canonical item exists and the requested observable/handling matches the review context.
4. For a policy failure, resolve governance/handling first; never bypass the policy gate.
5. For 429/5xx/timeouts, treat IntelOwl as unavailable/degraded and preserve the dependency error.
6. For job-id mismatch, unknown analyzer or malformed/oversized result, treat the response as untrusted and investigate the service boundary before retrying.
7. Review durable history through `GET /api/v1/intelowl/items/{item_id}/history`; do not use database edits to fabricate or amend enrichment evidence.

## Recovery

The new table is part of PostgreSQL canonical state and therefore follows the existing PostgreSQL backup/restore control. Recovery evidence for the materially changed Phase 11 candidate must be re-executed during the later integrated runtime hardening/production-equivalent phases; historical Phase 8/9 recovery evidence is not reused as acceptance of this table.

## Security incidents

Rotate the IntelOwl runtime token if credential exposure is suspected. Disable the feature flag when the service boundary cannot be trusted. Preserve logs/correlation identifiers and durable enrichment records; do not rewrite historical results. A compromised or untrusted IntelOwl response never grants DTMO share authority.

## Licensing boundary

IntelOwl/pyIntelOwl remain separate AGPL-3.0 services. This runbook covers API consumption only. Do not vendor, embed or redistribute upstream source as part of DTMO without explicit licensing review.

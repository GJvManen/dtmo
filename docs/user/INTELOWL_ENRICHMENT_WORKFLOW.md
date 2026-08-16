# IntelOwl Governed Enrichment Workflow

State: **`IMPLEMENTED / EXACT-HEAD VALIDATION REQUIRED`**  
Audience: analyst, senior analyst, reviewer, CISO, CERT/SOC reviewer  
Last reviewed: **2026-08-16**

## What this workflow does

The Phase 11.3 governed enrichment workflow lets an authorized human reviewer request bounded IntelOwl enrichment for an existing canonical DTMO intelligence item. IntelOwl evidence is supplemental context. It does not prove compromise, change the canonical review state or approve external sharing.

## Preconditions

The caller must be authenticated and hold `REVIEW_INTELLIGENCE`. The target canonical intelligence item must already exist. `DTMO_FEATURE_INTELOWL_ENRICHMENT` must be enabled and the requested observable class/analyzers must be permitted by configuration and handling policy.

## Execution

`POST /api/v1/intelowl/items/{item_id}/enrich`

Provide `observable_type`, `observable_value`, `handling` and a non-empty analyzer list. The service validates the request before disclosure, runs the bounded IntelOwl job, validates the immutable job identity and returned analyzer set, and stores the terminal result as durable enrichment history.

Restricted handling (`red`, `tlp:red`, `review-required`) is not disclosed to the separate IntelOwl/analyzer service boundary in this slice. The request fails closed before network disclosure.

## Result semantics

A successful receipt contains the DTMO enrichment-record id, canonical item id, IntelOwl job id, terminal status, partial-success marker, analyzer list and two invariant authority fields:

- `external_share_authorized=false`;
- `local_compromise_proven=false`.

Partial results remain partial; failed peer analyzers are not hidden behind successful peers.

## History

`GET /api/v1/intelowl/items/{item_id}/history` requires `READ_INTELLIGENCE` and returns durable enrichment receipts newest first. History is contextual evidence only and must be interpreted with canonical provenance, confidence, handling and review state.

## Human authority remains separate

IntelOwl enrichment never grants publication/share authority. Existing DTMO review and separate human share-approval controls remain authoritative. No IntelOwl tag, score, provider verdict or successful execution may be treated as local-compromise proof.

## Evidence boundary

The API and repository tests can prove only controlled code, policy and persistence behavior. They do not prove live IntelOwl/provider connectivity, analyzer quality, deployed credentials, privacy approval, production-equivalent behavior or production authorization.

# Phase 11.10e — IntelOwl/Cortex Integrated Analysis Workspace

Status: **IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED**  
Last updated: **2026-08-20**

## Purpose

Phase 11.10e replaces the Analysis & Enrichment shell placeholder with one governed DTMO workspace for human-triggered IntelOwl enrichment and analyzer-only Cortex execution against a canonical intelligence object.

The browser remains an unprivileged client. The normal trust path is **browser → DTMO API → governed integration adapter → upstream service**. Upstream credentials, allowlists and execution policy remain server-side.

## Canonical contracts

The workspace uses these DTMO APIs:

- `GET /api/v1/analysis/capabilities` — server-authorized capability/allowlist projection. Configuration is not runtime-health evidence.
- `GET /api/v1/analysis/items/{item_id}/history` — combined immutable IntelOwl and Cortex evidence history for one canonical object.
- `POST /api/v1/intelowl/items/{item_id}/enrich` — existing governed IntelOwl execution contract.
- `POST /api/v1/analysis/items/{item_id}/cortex` — bounded Cortex analyzer-only execution contract introduced by this slice.

Read access requires `read:intelligence`. Execution requires `review:intelligence`. UI visibility is usability only; server-side RBAC remains authoritative.

## Cortex persistence

Phase 11.10e adds `cortex_analysis_records` through migration `0015_cortex_analysis_history`. A record binds the canonical item, stable Cortex job ID, observable, explicit analyzer, TLP, status, bounded report/raw evidence, requesting principal and timestamp.

Database constraints preserve two invariant claims:

- `external_share_authorized = false`;
- `local_compromise_proven = false`.

The repository is idempotent by canonical item and Cortex job identity. Results whose canonical identity does not match the requested DTMO object are rejected.

## IntelOwl boundary

The existing IntelOwl execution and immutable history contract remains authoritative. Phase 11.10e does not bypass its feature flag, analyzer allowlist, handling policy, external-disclosure checks or result-size controls.

## Cortex boundary

Cortex remains analyzer-only. The approved adapter validates observable type/value, explicit analyzer allowlist and TLP before network I/O, verifies stable job identity and returned analyzer identity, and bounds result size. Responders, automatic analyzer discovery, files/attachments, administration and automatic fallback from IntelOwl are not part of this workspace.

## Analyst experience

`/workbench/analysis` provides:

1. explicit canonical item selection or `?item=<uuid>` deep-linking;
2. combined persisted IntelOwl and Cortex history;
3. capability visibility without inferred health;
4. an explicit observable type/value entry point;
5. separate IntelOwl and Cortex execution forms for authorized reviewers;
6. disabled execution controls for read-only principals;
7. explicit evidence text that enrichment is evidence, not a verdict.

No synthetic result is created when history or execution fails.

## Evidence and authority boundary

IntelOwl or Cortex output does **not prove** local compromise by itself. It grants no review completion, case mutation, publication, external sharing, MISP synchronization or production authority. Cortex responder actions remain prohibited by this slice.

Repository and browser CI prove only repository-controlled exact-head behavior. They do not prove live IntelOwl/Cortex availability, analyzer/provider authorization, production-equivalent operation, independent assurance or production authorization. DTMO remains **not production authorized**.

## Acceptance

Phase 11.10e may become `PASS / REPOSITORY_COMPLETE` only when the dedicated exact-head workflow and every other workflow registered for the final PR head are `completed/success`, the PR is mergeable, and professional documentation is synchronized.

After acceptance and merge, the only next bounded slice is **Phase 11.10f — OpenCTI graph/entity workspace**.

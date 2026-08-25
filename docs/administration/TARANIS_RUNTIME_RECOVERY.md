# Canonical Administration — Taranis AI runtime recovery

## Purpose

Taranis AI already has a governed DTMO server-side read adapter with checkpointing, bounded pagination, detail/CTI enrichment and canonical ingest. The remaining functional gap is operator execution from the canonical Administration interface.

## Operator contract

An authorized principal with `manage:connectors` configures Taranis through the existing same-origin Administration API. The API base is non-secret runtime configuration. The API token remains write-only and server-side; it is never returned to the browser.

The canonical Taranis card may expose **Run Taranis import now** only when the persisted integration is enabled, server-derived `ready`, and there are no unsaved browser changes. The browser must call only the DTMO same-origin `POST /connectors/taranis/run` endpoint and must never become a direct Taranis client.

## Existing governed runtime

`TaranisReadConnector` reads news items and stories using bounded pagination. It maintains a local checkpoint and deliberately reconciles a configured number of pages behind that checkpoint so late upstream changes can be observed without pretending the source is append-only.

Detail and CTI enrichment are bounded by `taranis_detail_cti_limit`. A missing detail object is represented as a reconciliation race rather than silently promoted to complete evidence. Exhausting the enrichment budget remains explicit in normalized context.

A successful connector request is normalized and ingested into canonical DTMO persistence and indexing using the existing server-side connector run path.

## Evidence and authority boundary

The Administration card reports request-specific runtime status, returned record count, inserted/indexed counts, attempts, alert state and correlation ID. A completed run proves only that this particular DTMO request completed with the reported result. It is not a blanket Taranis health, completeness, source-truth or publication claim.

Imported Taranis records remain read-only imports with `external_share_authorized = false`. Runtime execution grants no intelligence-review, case, sharing, publication, remediation, external-assurance or production authority.

## Fail-closed behavior

Taranis remains non-runnable from canonical Administration while disabled, configuration-incomplete, credential-incomplete or locally dirty. Upstream HTTP failures, malformed responses, checkpoint errors and pagination errors remain failed connector results and must not be displayed as healthy state.

## Bounded recovery scope

This slice covers only end-to-end Taranis read/import execution from canonical Administration. IntelOwl, Cortex, OpenCTI and TheHive runtime actions remain separate recovery slices.

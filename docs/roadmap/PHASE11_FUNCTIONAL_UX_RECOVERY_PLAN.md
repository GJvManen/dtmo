# Phase 11 Functional UX Recovery Plan

Status: **ACTIVE — R5 Cross-workspace statistics and trends**

## Purpose

The canonical workbench has accumulated substantial backend, integration and security capability, but owner functional testing still finds that the product requires too much setup, presents component capabilities as separate surfaces, and does not yet feel materially improved as one professional operator console.

This plan supersedes screenshot promotion as the active repository priority. Screenshot promotion, candidate freeze, production-equivalent validation and independent assurance resume only after whole-product functional acceptance.

## Non-negotiable boundaries

Recovery must preserve:

- server-side credentials and upstream authentication;
- RBAC and separation of duties;
- attributable provenance and raw-evidence binding;
- fail-closed behavior for missing configuration, scope or authority;
- explicit human review, share and publication authority;
- no fabricated live, production-equivalent, penetration-test or independent-assurance evidence.

Repository-controlled bootstrap/sample content must be labelled as such and must never be represented as live upstream evidence.

## Bounded delivery sequence

### R1 — Usable-by-default open-source bootstrap and integration readiness
Repository status: **MERGED / REPOSITORY-COMPLETE — #379**.

### R2 — Administration information architecture
Repository status: **MERGED / REPOSITORY-COMPLETE — #380**.

### R3 — Unified intelligence object context and workplace
Repository status: **MERGED / REPOSITORY-COMPLETE — #381**.

### R4 — Integrated enrichment
Repository status: **MERGED / REPOSITORY-COMPLETE — #382**.

### R5 — Cross-workspace statistics and trends

Repository status: **ACTIVE — source contribution merged in #383; intelligence type distribution merged in #384; enrichment status merged in #385; collection volume is the current bounded slice**.

Goal: turn the existing visualization foundation into useful operational analytics.

- collection volume/freshness and source contribution;
- intelligence and IOC type/source trends;
- enrichment coverage/status;
- CVSS/EPSS/KEV distributions and vulnerability trends;
- investigation, connector and operational state trends;
- accessible table/text equivalents and non-colour cues.

Completed bounded slice: attributable canonical intelligence source contribution grouped directly from persisted `IntelligenceItem.source_id`, rendered in Visual Analytics with both chart and table equivalents. This is persisted-content evidence only and is not a source-health or reachability claim.

Completed bounded slice: canonical intelligence type distribution grouped directly from persisted `IntelligenceItem.item_type`, rendered in Visual Analytics with both chart and table equivalents. Zero-count canonical types remain explicit when the datastore is available; datastore failure remains unavailable/empty and never synthesizes evidence.

Completed bounded slice: enrichment status distribution grouped directly from persisted `IntelOwlEnrichmentRecord.status`, rendered in Visual Analytics with both chart and table equivalents. This is historical persisted execution evidence only and does not prove analyzer correctness, current upstream availability, compromise, review completion or sharing/publication authority.

Current bounded slice: add persisted collection volume grouped by `ConnectorRun.connector_id` using the sum of canonical `ConnectorRun.inserted` counts, rendered in Visual Analytics with chart and table equivalents. This is historical execution evidence only; it does not establish live connector health, freshness, current upstream availability, or successful present-time collection.

Acceptance: charts are sourced from canonical APIs/persistence and never synthesize values merely to populate a dashboard.

### R6 — Sources & Collection default-open-source experience

Goal: make supported open sources immediately actionable from the canonical console.

- inventory/register/validate/activate/run/status/freshness in one journey;
- safe public sources may be enabled by the supported bootstrap profile where no credential or external authority is required;
- external/credentialed sources remain explicit configuration tasks;
- expose ingestion counts and provenance.

Acceptance: a clean supported installation has a documented path to useful attributable content without legacy UI.

### R7 — Graph, investigations, sharing and automation integration

Goal: eliminate remaining component silos.

- graphable-object discovery and direct graph pivots;
- case handoff/history continuity;
- review/share state and transfer history in context;
- playbook availability/execution history with explicit authority boundaries.

Acceptance: cross-component journeys preserve object identity, provenance and human authority.

### R8 — Whole-product functional acceptance

Run a complete owner functional retest from a clean supported installation. Only an explicit PASS may unblock screenshot promotion, candidate freeze, fresh production-equivalent validation and later independent assurance.

## Delivery discipline

Each recovery item is implemented as one bounded reviewable PR. Every PR starts from current `main`, adds or updates repository-controlled functional acceptance evidence, and stops at fresh exact-head CI. Failures are corrected only from concrete failing job logs and verified root causes.

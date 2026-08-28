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

Goal: reduce unnecessary setup while remaining fail-closed.

- classify integrations as `ready-by-default`, `configuration-required`, `credential-required`, `disabled-by-policy`, `reachable`, `ingesting` or `degraded` as applicable;
- identify public/credentialless supported sources that can safely work in the default local/reference profile;
- expose one actionable readiness inventory instead of forcing operators to infer feature flags;
- keep credential-bearing integrations disabled until server-side prerequisites are satisfied;
- document exactly which capabilities work after supported bootstrap and which require external services.

Acceptance: a clean repository-controlled local/reference bootstrap exposes useful safe defaults and truthful blockers without secret material in the browser.

### R2 — Administration information architecture

Repository status: **MERGED / REPOSITORY-COMPLETE — #380**.

Goal: make Administration behave as one coherent console rather than a long mixed control page.

- provide stable sub-navigation for Overview, Integrations, Sources, Identity, Roles & Permissions, and Security & Audit;
- preserve existing server-authorized mutation endpoints and request IDs;
- improve readiness summaries and configuration guidance;
- keep credential replacement write-only.

Acceptance: an administrator can find and complete an authorized task without navigating to legacy UI or losing context.

### R3 — Unified intelligence object context and workplace

Repository status: **MERGED / REPOSITORY-COMPLETE — #381**.

Goal: make the canonical workbench an analyst workplace rather than a collection of pages.

- make intelligence objects/IOCs the shared context across provenance, observables, enrichment, graph, investigations and sharing;
- add direct governed pivots without UUID copy/paste;
- preserve attributable empty states where related context does not exist.

Acceptance: an analyst can follow one persisted object across the supported investigation journey without manual identifier transfer.

### R4 — Integrated enrichment

Repository status: **MERGED / REPOSITORY-COMPLETE — #382**.

Goal: make IntelOwl/Cortex enrichment part of the intelligence journey.

- extract and present persisted observables;
- show enrichment history and available governed actions in object/IOC context;
- return results to the same context after reload;
- keep analyzer allowlists, credentials and authorization server-side.

Acceptance: authorized enrichment is launchable and reviewable from canonical object context with durable attributable results.

### R5 — Cross-workspace statistics and trends

Repository status: **ACTIVE — source contribution merged in #383; intelligence type distribution merged in #384; enrichment status merged in #385; collection volume merged in #386; collection observation age merged in #388; IOC type distribution merged in #389; KEV status distribution merged in #390; CVSS score distribution merged in #391; EPSS probability distribution is the current bounded slice**.

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

Completed bounded slice: persisted collection volume grouped by `ConnectorRun.connector_id` using canonical `ConnectorRun.inserted` counts, rendered in Visual Analytics with both chart and table equivalents. This is historical execution evidence only and does not establish live connector health, freshness, current upstream availability, or successful present-time collection.

Completed bounded slice: collection observation age per connector from the latest persisted `ConnectorRun.started_at`, rendered in Visual Analytics with chart and table equivalents. Observation age is historical evidence only and is not labelled as connector health, operational freshness, reachability or current upstream availability.

Completed bounded slice: IOC type distribution from persisted canonical `IntelOwlEnrichmentRecord.observable_type` values already used by the server-authorized IOC inventory. This is persisted observable evidence only and does not infer maliciousness, verdict, local compromise, review completion or sharing/publication authority.

Completed bounded slice: KEV evidence-status distribution from canonical vulnerability API rows after the existing raw-evidence integrity verification boundary. The distribution distinguishes known exploited, not-known-exploited and unknown evidence states; KEV evidence does not prove local deployment, exploitability, compromise, remediation authority or external-share approval.

Completed bounded slice: CVSS score-band distribution from canonical vulnerability API rows after raw-evidence integrity verification. The distribution uses explicit critical, high, medium, low, none and unknown bands. CVSS is prioritization evidence only and does not prove exploitability, local deployment, local exposure, compromise, remediation authority or external-share approval.

Current bounded slice: add EPSS probability-band distribution from the same canonical vulnerability API rows after raw-evidence integrity verification. The distribution uses explicit very-high, high, moderate, low and unknown bands. EPSS is prioritization evidence only and does not prove exploitability, local deployment, local exposure, compromise, remediation authority or external-share approval.

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

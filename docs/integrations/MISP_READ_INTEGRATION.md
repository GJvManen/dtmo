# E8.6 — Governed MISP read integration

## Purpose

E8.6 adds an optional, disabled-by-default read-only MISP adapter. MISP remains an upstream CTI source; DTMO remains the canonical governed product surface for review, correlation and any later sharing decision.

The adapter uses the MISP event search API and never calls event/attribute/object mutation, publication, push or synchronization endpoints. A MISP API key is supplied only at runtime through `DTMO_MISP_API_KEY` and is not copied into raw evidence, logs or repository configuration.

## Configuration

- `DTMO_FEATURE_MISP_CONNECTOR=false` by default.
- `DTMO_MISP_API_BASE` identifies the approved MISP instance.
- `DTMO_MISP_API_KEY` is the runtime API key.
- `DTMO_MISP_EVENT_LIMIT` bounds one read cycle (default 50, maximum 500).
- scheduled execution additionally requires the existing `DTMO_FEATURE_LIVE_CONNECTORS=true` switch.

When enabled in production, the MISP base URL must use HTTPS and a runtime API key must be present.

## Read contract

The adapter POSTs only to `events/restSearch` with JSON output, a bounded limit, page 1 and descending timestamp order. Returned event wrappers and direct event objects are accepted.

Each event is retained as raw evidence and receives a `_dtmo_misp` projection containing:

- event UUID, source event ID, event information, date/timestamps and creator organisation;
- event distribution and sharing-group identifier;
- event tags and TLP tags;
- galaxies and galaxy clusters;
- attributes/IOCs with UUID, type, category, value, `to_ids`, first/last seen, distribution, sharing group, tags and galaxies;
- MISP objects, object attributes and object references/relationship types;
- explicit `restriction_authoritative=true`, `read_only_import=true` and `external_share_authorized=false` boundaries.

The canonical DTMO item type `cti_event` is additive and represents a structured CTI event/package without pretending that every MISP event is a campaign, incident or single indicator.

## Distribution and sharing boundary

Incoming MISP distribution/TLP/sharing-group data is evidence and an authoritative constraint. Import success does not mean redistribution is allowed. E8.6 does not grant `share_approved`, does not publish back to MISP and does not create a synchronization relationship.

E8.7 is the separate future slice for governed outbound sharing. It must enforce DTMO human share approval in addition to the incoming MISP constraints; it may never infer permission from successful E8.6 ingestion.

## Evidence boundary

Repository unit/contract tests prove parser, request-shape, secret-handling and restriction-preservation behavior against synthetic MISP payloads only. They do not prove connectivity to a real MISP instance, correctness of a specific organisation's MISP permissions, completeness of live CTI, production deployment, owner acceptance or external-sharing approval.

## Upstream basis

The implementation is aligned with the official MISP documentation describing `events/restSearch`, the MISP core JSON format, taxonomies/galaxies and granular sharing/distribution capabilities. The repository does not vendor upstream credentials or claim a live MISP acceptance run.

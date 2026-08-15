# Taranis AI → DTMO Integration Contract

Contract date: **2026-08-15**  
Phase: **11.1 — Taranis architecture and gap assessment**  
Contract state: **`PROPOSED / EXACT-HEAD VALIDATION REQUIRED`**

## Purpose

This document is the implementation boundary for Phase 11.2. It converts the Phase 11.1 architecture assessment into a testable service-to-service contract. It does not claim a live Taranis deployment, production authorization, external-sharing authority or completed adapter implementation.

## Upstream baseline

The contract was derived from the current `taranis-ai/taranis-ai` `master` source structure inspected on 2026-08-15. The integration uses documented HTTP service boundaries. Taranis source code is not vendored into DTMO.

The Taranis core registers an assessment API below `${APPLICATION_ROOT}api/assess` and an authentication API below `${APPLICATION_ROOT}api/auth`.

## Required read surface

Phase 11.2 starts read-only. The minimum upstream API surface is:

| Purpose | Method | Taranis route | Required upstream permission | DTMO use |
|---|---|---|---|---|
| Authentication method discovery | `GET` | `/api/auth/method` | public discovery | determine configured authentication mode; never infer authorization from this response |
| Token acquisition when local auth is used | `POST` | `/api/auth/login` | valid integration credential | obtain a short-lived bearer token through the configured Taranis authenticator |
| Token refresh | `GET` | `/api/auth/refresh` | authenticated token | rotate access token without storing a user password in DTMO runtime state |
| Source catalogue | `GET` | `/api/assess/osint-sources-list` | `ASSESS_ACCESS` | map stable upstream source identity to DTMO source/provenance records |
| Source groups | `GET` | `/api/assess/osint-source-group-list` | `ASSESS_ACCESS` | retain upstream grouping context without treating it as DTMO governance policy |
| News-item page | `GET` | `/api/assess/news-items` | `ASSESS_ACCESS` | ingest raw evidence candidates using bounded pagination |
| News-item detail | `GET` | `/api/assess/news-items/{item_id}` | `ASSESS_ACCESS` | retrieve a deterministic upstream object by ID |
| News-item CTI | `GET` | `/api/assess/news-items/{item_id}/cti` | `ASSESS_ACCESS` | import extracted CTI as attributed context, not proof of local compromise |
| Story page | `GET` | `/api/assess/stories` | `ASSESS_ACCESS` | ingest assessed/grouped upstream context using bounded pagination |
| Story detail | `GET` | `/api/assess/stories/{story_id}` | `ASSESS_ACCESS` | retrieve deterministic story state by ID |
| Story CTI | `GET` | `/api/assess/stories/{story_id}/cti` | `ASSESS_ACCESS` | import CTI relationships while retaining upstream provenance |

The adapter MUST NOT require `ASSESS_CREATE`, `ASSESS_UPDATE`, `ASSESS_DELETE`, connector-share, publisher or bot-execution permissions for its initial read path.

## Explicitly excluded authority

The Phase 11.2 service identity MUST NOT receive or exercise these capabilities merely to support ingestion:

- create, update or delete Taranis news items or stories;
- invoke bot actions;
- share a story through a connector;
- publish a report;
- change users, roles or configuration;
- gain DTMO MISP/export/share approval;
- convert a Taranis publisher action into DTMO external-share authorization.

Any future write-back requires a separate architecture decision and bounded PR.

## Authentication contract

DTMO treats Taranis as an external service boundary.

1. Prefer a dedicated non-human service identity with only the permissions needed for the read surface.
2. Credentials/tokens are supplied from the runtime secret store, never repository configuration, logs, browser fixtures or screenshots.
3. TLS certificate verification is mandatory outside explicitly marked local development.
4. Access tokens are held in memory only where practical and refreshed through the supported authentication flow.
5. `401` causes one bounded re-authentication attempt; repeated authentication failure transitions the connector to degraded/failed state rather than retrying indefinitely.
6. `403` is an authorization/configuration failure and MUST NOT be bypassed by requesting broader credentials automatically.
7. External-auth header mode may be supported only behind a trusted ingress with header-spoofing prevention; DTMO must not self-assert privileged role headers to an untrusted endpoint.

## Pagination and polling

The initial adapter uses polling, not SSE, as the canonical ingestion trigger.

- `/news-items` supports `limit` up to 1000 and offset/page semantics upstream; DTMO uses a configurable bounded page size.
- `/stories` supports `limit` up to 400 and offset/page semantics upstream; DTMO uses a configurable bounded page size.
- Polling checkpoints are durable and include upstream object type, object ID and observed upstream modification/version material where available.
- SSE may later be used as a wake-up hint, but MUST NOT become the only durability mechanism. A missed SSE event must be recoverable by polling/reconciliation.
- Every polling cycle is bounded by time, pages and records to avoid starvation or runaway upstream load.

## Identity and idempotency

DTMO MUST preserve the original Taranis identifiers. Canonical adapter keys use an explicit namespace:

- source: `taranis:source:{upstream_source_id}`;
- news item: `taranis:news-item:{upstream_item_id}`;
- story: `taranis:story:{upstream_story_id}`.

A replay of an unchanged upstream object MUST be idempotent. A changed object with the same upstream ID MUST create a deterministic canonical update/revision according to existing DTMO persistence semantics, not a duplicate intelligence record.

Hashing may be used as an optimization/evidence fingerprint but MUST NOT replace the stable upstream identity.

## Canonical mapping

| Taranis object/field class | DTMO semantic target | Mandatory rule |
|---|---|---|
| OSINT source ID/name | source catalogue identity | preserve upstream ID and display metadata separately |
| news-item ID | raw-evidence/candidate identity | immutable upstream namespace key retained |
| news-item source reference | provenance source | cannot be dropped during normalization |
| collected/published timestamps | evidence timeline | preserve source timestamp and ingestion timestamp separately |
| URL/content reference | original evidence reference | retain sanitized original reference where policy permits |
| story ID | assessed-context identity | never silently merge with a different story ID |
| story membership | evidence relationship | retain links to contributing news items when supplied |
| tag/IOC/CTI result | observable/context | preserve extraction origin and upstream object link |
| upstream TLP/marking | DTMO classification/handling input | never weaken marking silently; unknown/unmapped values fail closed |
| upstream user/actor metadata | provenance actor reference | informational unless explicitly mapped through the platform IdP |
| report/publisher intent | analytic-product context only | never becomes DTMO share approval |

## TLP and classification

Classification transformation is fail-closed.

- Recognized TLP/handling markings are mapped to an equal or more restrictive DTMO handling level.
- Unknown, missing or unsupported upstream markings are imported with a restrictive review-required state rather than defaulting to shareable.
- A downstream transformation cannot reduce the upstream restriction without an explicit authorized DTMO review action.
- Severity, confidence, relevance and TLP are separate dimensions and MUST NOT be conflated.

## Provenance minimum

Each canonical record created or updated through this adapter must be able to answer:

- which Taranis instance produced it;
- which upstream object type and ID it came from;
- which upstream source was associated with it where available;
- when DTMO retrieved it;
- which adapter version performed normalization;
- whether it was a first observation, replay or changed revision;
- which raw/evidence reference supports the normalized values;
- which correlation/request ID covered the ingestion transaction.

## Failure semantics

The connector is fail-isolated. Taranis failure must not make unrelated DTMO read paths unavailable.

| Condition | Required behavior |
|---|---|
| connection/TLS failure | mark dependency degraded, bounded retry/backoff, no fabricated data |
| `401` | one bounded token recovery path, then fail/degrade |
| `403` | configuration/permission failure; no privilege escalation fallback |
| `404` for detail after listing | record reconciliation race and continue; do not invent deletion semantics |
| `429` | honor retry guidance where present and back off |
| `5xx` | bounded retry; preserve checkpoint before failed page |
| malformed JSON/schema mismatch | quarantine/reject affected object with evidence; continue isolation where safe |
| duplicate/replay | idempotent no-op or deterministic revision |
| partial page failure | do not advance checkpoint past uncommitted records |
| unknown TLP/classification | restrictive review-required handling |

## Threat-model abuse cases

Phase 11.2 tests must cover at least:

1. malicious HTML/script content present in upstream text fields;
2. oversized fields or unexpectedly large pages;
3. malformed IDs and namespace collision attempts;
4. replay storms and repeated unchanged objects;
5. an object changing while retaining the same upstream ID;
6. source identity spoofing inside payload content;
7. unknown or downgraded TLP markings;
8. authentication expiry and token replay;
9. a service identity receiving accidental write/share permissions;
10. upstream publication metadata being misinterpreted as DTMO approval;
11. partial persistence failure between raw evidence and canonical normalization;
12. Taranis outage while the rest of DTMO remains healthy.

## Licensing and redistribution boundary

The integration remains API/service based. No Taranis implementation source is copied, vendored or relicensed into DTMO by Phase 11.2. Upstream project/license notices are retained in architecture and dependency documentation as applicable. Any change from service integration to source redistribution requires a dedicated licensing review before implementation.

## Deprecation rule

Existing DTMO generic collection code is not removed merely because this contract exists. Deprecation starts only after the Phase 11.2 adapter passes its contract/integration gates, migration/rollback is demonstrated and the replacement capability is operationally accepted. Curated education-sector source policy and canonical governance remain DTMO responsibilities.

## Phase 11.2 acceptance contract

The next implementation PR must demonstrate all of the following before merge:

- read-only Taranis client/configuration with HTTPS verification default-on;
- dedicated secret-backed credentials with no broad/write permission requirement;
- source, news-item and story ingestion through bounded pagination;
- deterministic namespaced IDs and idempotent replay;
- raw evidence/provenance preservation;
- fail-closed TLP/classification handling;
- durable checkpoint semantics that do not skip partially committed data;
- bounded retry/backoff for transient failures and explicit `401`/`403` behavior;
- no external-share/publisher authority crossing the boundary;
- contract tests for success, replay, malformed payload, permission failure, outage and partial failure;
- observability carrying connector name, correlation ID, upstream object type/ID and outcome without secrets;
- migration/rollback notes and professional documentation updates.

## Decision

**`PHASE 11.1 CONTRACT BASELINE: PROCEED TO 11.2 AFTER EXACT-HEAD ACCEPTANCE`**.

This decision authorizes implementation planning only. It is not a deployment, staging, external-assurance or production authorization decision.

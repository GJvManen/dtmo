# OpenCTI Integration Operations Runbook

Status: **Phase 11.4 contract slice / implementation not yet enabled**  
Last updated: **2026-08-16**

## Scope

This runbook defines the operational boundary for the planned DTMO↔OpenCTI integration. It intentionally does not claim that OpenCTI is deployed, credentialed or live-connected.

## Preconditions before enablement

- approved OpenCTI edition and licensing/entitlement recorded;
- immutable deployed OpenCTI version identified;
- dedicated DTMO service identity created;
- minimum OpenCTI roles/capabilities and allowed markings reviewed;
- token stored in the approved runtime secret manager;
- TLS endpoint and certificate trust validated;
- GraphQL/TAXII/stream path selected and documented;
- privacy/data-handling review completed for the actual dataset;
- backup/recovery responsibilities known;
- Phase 11.4 adapter exact-head repository gate accepted.

## Normal operation

The first adapter is read-oriented. Operators must confirm that retrieved entities/relationships retain OpenCTI/STIX identity, marking, confidence and provenance before graph context is accepted into DTMO.

DTMO publication/share approval remains unchanged by successful synchronization.

## Fail-closed conditions

Stop or quarantine the integration path on:

- `401` / invalid authentication;
- `403` / insufficient capability or marking access;
- unknown or malformed marking/TLP/PAP data;
- malformed or unsupported STIX object/relationship;
- unstable or missing upstream identity;
- cursor/checkpoint regression;
- replay/deduplication ambiguity;
- oversized payload or repeated timeout;
- `429` without bounded backoff;
- `5xx` beyond the configured retry budget;
- evidence that the configured account has broader privilege than approved.

Do not broaden privileges automatically to make the integration succeed.

## Reconciliation and restart

A future stream/pagination adapter must persist successfully processed DTMO state before advancing its cursor. After interruption:

1. read the last durable cursor/checkpoint;
2. re-request from that position with a bounded overlap when supported;
3. deduplicate by stable OpenCTI/STIX identity and update/version context;
4. handle create/update/delete/merge distinctly;
5. preserve prior DTMO evidence history;
6. advance the cursor only after durable commit.

## Incident handling

For suspected data leakage, authorization bypass, unexpected broader marking access or unapproved side effects:

1. disable the DTMO OpenCTI integration feature/path;
2. revoke or rotate the integration token;
3. preserve request/correlation IDs and non-secret evidence;
4. identify affected OpenCTI entities/markings and DTMO mappings;
5. confirm no DTMO share approval was mutated;
6. record corrective action and revalidation requirements;
7. do not resume until the trust boundary is reviewed.

## Side effects that remain prohibited

The Phase 11.4 contract does not authorize connector registration, MISP sync, external enrichment, arbitrary GraphQL mutations, case creation, report publication or OpenCTI security/marking administration.

## Evidence rule

Repository CI is engineering evidence only. Live endpoint health, effective RBAC/marking segregation, deployed secret handling, real graph correctness, HA/recovery and production readiness require later deployment-bound evidence.
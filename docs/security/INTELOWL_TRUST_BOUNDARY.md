# IntelOwl Governed Execution Trust Boundary

State: **`IMPLEMENTED / EXACT-HEAD VALIDATION REQUIRED`**  
Last reviewed: **2026-08-16**

## Security objective

Preserve DTMO confidentiality, provenance, RBAC and human publication authority while allowing bounded IOC enrichment through the separate IntelOwl service/API boundary.

## Identity and authorization

A governed enrichment request originates from an authenticated human DTMO principal holding `REVIEW_INTELLIGENCE`. The current `SERVICE_ACCOUNT` role does not hold that permission, so service identities cannot autonomously invoke the governed execution endpoint.

DTMO authenticates to IntelOwl with a separate runtime API token. That token is a service secret, is never persisted in enrichment history and must not appear in repository evidence, logs or screenshots.

## Disclosure policy

Every requested analyzer is conservatively classified as external to the DTMO trust boundary in this slice. `red`, `tlp:red` and `review-required` handling therefore blocks execution before the network request. Email/personal-data observable classes remain excluded by default.

The analyzer allowlist is explicit. Unknown requested or returned analyzers are rejected. No fallback provider is selected automatically.

## Side-effect boundary

DTMO submits `connectors_requested=[]`. IntelOwl external Connectors such as MISP, OpenCTI, Slack or email are not authorized side effects of this path. Future side effects require a separate architecture/security/authority decision.

## Result integrity

DTMO verifies immutable IntelOwl job identity, serialized result-size bounds, report structure and analyzer identity. A mismatch or malformed/oversized result fails closed and is not persisted as accepted enrichment evidence.

Durable records are linked to canonical intelligence and preserve the requesting human, handling decision, analyzer identities and raw normalized result. Database constraints require:

- `external_share_authorized=false`;
- `local_compromise_proven=false`.

An enrichment result cannot change canonical `share_approved` state.

## Availability and dependency failure

IntelOwl 429/5xx responses, transport failures and bounded polling exhaustion are dependency failures. They do not trigger an unapproved provider fallback and do not create synthetic success evidence.

## Incident response

If the IntelOwl boundary is suspected compromised, disable `DTMO_FEATURE_INTELOWL_ENRICHMENT`, rotate the runtime token, preserve correlation/log evidence and immutable enrichment history, and investigate before re-enabling. Never edit historical enrichment rows to conceal an incident or strengthen an evidence claim.

## Licensing and supply-chain boundary

IntelOwl/pyIntelOwl remain separate AGPL-3.0 services. No upstream source is vendored, embedded or redistributed by this slice. Container/image provenance, runtime isolation and integrated supply-chain controls are addressed later under Phase 11.8 and cannot be inferred from repository CI.

## Non-evidence

This repository security boundary does not prove deployed network segmentation, secret-store implementation, live provider credentials, production TLS configuration, privacy approval, production-equivalent resilience, independent external assurance or production authorization.

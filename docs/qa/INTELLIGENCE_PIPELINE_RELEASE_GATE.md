# Intelligence Pipeline Release Gate — DTMO 16.0.0rc7

## Scope

This gate covers the repository-controlled end-to-end path from the existing CISA KEV connector through raw evidence landing, canonical persistence and provenance into OpenSearch-backed operator search. It does not authorize arbitrary new sources and does not close staging or external-assurance gates.

## Required evidence

The final exact release head must demonstrate all of the following:

1. search on a fresh deployment does not fail merely because the intelligence index has not yet been created;
2. the strict OpenSearch mapping matches every field written by canonical ingestion;
3. search sorting uses the same canonical confidence field that is indexed;
4. a successful CISA KEV connector run lands and persists every record through the governed intelligence pipeline;
5. connector provenance includes source identity/reliability and raw payload evidence;
6. connector replay is idempotent for the canonical record and can repair a missing/failed derived OpenSearch document;
7. connector execution never changes review or share-approval state;
8. manual connector execution requires `manage:connectors` server-side;
9. service-account and human separation-of-duties invariants remain enforced;
10. the registered CI/workflow matrix completes successfully on the final exact head.

## Known user-facing defect addressed

The accepted rc6 deployment could show:

`Zoeken mislukt: search backend unavailable: HTTPStatusError`

Two repository defects could produce this symptom: an absent index on a fresh deployment and strict-mapping rejection because canonical ingestion wrote confidence fields not declared by the index mapping. Both contracts are remediated in rc7.

## Source ingestion boundary

16.0.0rc7 makes the already-supported CISA KEV connector operational end-to-end. It does **not** introduce arbitrary source creation. Adding sources is intentionally deferred to a governed admin source-registry objective because arbitrary externally supplied URLs can create SSRF, credential-exposure, provenance and trust-boundary risks.

## External and deferred evidence

This gate does not claim:

- additional live-source connectors beyond the existing CISA KEV integration;
- production-safe arbitrary source registration;
- real staging deployment parity;
- independent penetration testing;
- genuine VoiceOver/NVDA execution;
- external stakeholder acceptance;
- production go/no-go.

## Current decision

`CI_VALIDATION_PENDING` until every registered workflow succeeds on the final exact PR head. No locally inferred or unexecuted test is accepted as PASS.

# RC10.11.5 — MSRC source gate

Status: `PENDING_CI`

## Objective

Make Microsoft Security Response Center Security Update Guide data genuinely executable from the unified DTMO console through the official public MSRC CVRF v3 API.

## Accepted source contract

- canonical base: `https://api.msrc.microsoft.com/cvrf/v3.0`
- discovery: `GET /updates`
- document retrieval: `GET /cvrf/{id}`
- update IDs must match `YYYY-mmm`
- maximum 12 update documents per run
- all requests reuse DTMO pinned HTTPS, DNS re-resolution, non-global-address rejection, redirect denial and response-size bounds
- full CVRF document retained as raw provenance
- ingestion never grants review/share approval or publication authority

## Release criteria

- catalog status and executor profile match
- supported-profile contract remains exact
- discovery fails closed on malformed responses
- CVRF parser fails closed on invalid IDs/documents
- normalized record preserves source reliability and raw provenance
- full exact-head required workflow set succeeds

Do not mark PASS or merge until exact-head CI evidence is complete.

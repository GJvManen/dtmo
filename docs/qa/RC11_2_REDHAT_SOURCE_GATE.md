# RC11.2 Red Hat Product Security source gate

Status: **PENDING_CI**

## Objective

Connect the official Red Hat Security Data API to the unified DTMO source framework without HTML scraping, while preserving the existing transport, provenance and publication-governance boundaries.

## Accepted source contract

- Canonical base: `https://access.redhat.com/hydra/rest/securitydata`
- Discovery: `/csaf.json?created_days_ago=10&per_page=25&isCompressed=false`
- Detail: `/csaf/<RHSA_ID>.json?isCompressed=false`
- Execution profile: `redhat-csaf-v1`
- Authentication: none
- Maximum advisory documents per run: 25
- Advisory identifiers must match `RHSA-YYYY:number`
- Detailed documents are normalized through the existing OASIS CSAF parser.

## Security and governance invariants

- Existing HTTPS-only URL validation and DNS re-resolution remain in force.
- Non-global destinations, redirects, invalid response types and responses beyond the global source size limit remain fail-closed.
- The index may only contribute syntactically valid RHSA identifiers; arbitrary URLs are never followed.
- The CSAF tracking ID must equal the RHSA requested from discovery.
- Raw CSAF JSON is retained as record provenance.
- Ingestion does not grant review or publication authority; the existing human-review and separate share-approval gate remains unchanged.

## Regression evidence

`backend/tests/test_rc11_2_redhat_adapter.py` covers catalog/framework registration, bounded and deduplicated discovery, malformed-index rejection, framework dispatch, raw provenance retention and tracking-ID mismatch rejection.

`docs/qa/SOURCE_CONNECTION_MATRIX.md` records Red Hat as `PENDING_CI` until this exact-head gate is accepted.

## Release gate

Do not mark PASS and do not merge until the full exact-head GitHub workflow set, including RC4 Quality Gate, completes successfully. Repository CI does not claim real-staging provider acceptance.

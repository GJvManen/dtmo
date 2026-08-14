# Governed MISP export (E8.7)

## Scope

E8.7 adds a bounded DTMO-to-MISP export path. It does not turn MISP connectivity into publication authority and it does not weaken the existing two-step DTMO decision model.

An item may reach the MISP export path only after it is already `reviewed`, has separate human `share_approved` state and retains the approving principal attribution. The export endpoint itself cannot create review or share approval.

## Runtime boundary

Outbound MISP delivery is disabled by default through `DTMO_FEATURE_MISP_EXPORT=false`. This flag is separate from the read connector flag, so enabling E8.6 read access cannot silently enable E8.7 writes. Runtime delivery additionally requires `DTMO_MISP_API_BASE` and `DTMO_MISP_API_KEY`; production requires HTTPS.

The API key is consumed as a runtime secret and is not written into canonical intelligence, audit metadata or repository evidence.

## Endpoint

`POST /api/v1/intelligence/{item_id}/misp-export`

The caller requires the existing publisher/share-approval authority. The request also supplies a bounded MISP distribution value, optional sharing-group ID where distribution `4` is selected, TLP and `X-Request-ID` correlation.

## Export representation

The first bounded export creates an unpublished MISP event through `events/add`. DTMO sends a deterministic event UUID, the governed intelligence title, canonical URL and bounded summary context. `published` is always `false` in this slice. MISP publication, synchronization and further community distribution are not automated by DTMO E8.7.

## Restriction handling

Distribution and TLP are enforced fail-closed. Sharing-group distribution requires an explicit sharing-group ID. If authoritative MISP-origin restrictions have been projected into canonical metadata, E8.7 refuses distribution/sharing-group changes and refuses a less restrictive TLP.

E8.6 currently retains full incoming MISP restriction evidence in raw evidence. Where those restrictions are not yet projected into canonical metadata, E8.7 refuses re-export of MISP-origin intelligence rather than guessing or relaxing the upstream restriction.

## Replay protection

DTMO reserves an export record in canonical metadata before delivery and derives a stable replay key from the exact outbound event. Successful and delivery-uncertain records block automatic replay. A timeout, HTTP failure or malformed/ambiguous MISP response is recorded as `uncertain`; the request fails and an operator must inspect destination evidence before any later remediation.

Successful delivery records the returned MISP event ID, deterministic UUID and replay key and appends an auditable `intelligence.misp_export` allow decision. Replay rejection and uncertain delivery are fail-closed states.

## Claim boundary

Repository tests use synthetic intelligence and an in-process mocked MISP HTTP transport. They demonstrate code contracts only. They do not prove live MISP connectivity, production deployment, destination permissions, successful external delivery, external publication, owner acceptance, penetration-test acceptance or permission from an upstream intelligence-sharing community.

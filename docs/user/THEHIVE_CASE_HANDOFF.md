# TheHive Case Handoff — User Workflow

Status: **`PHASE 11.6 BOUNDED IMPLEMENTATION / EXACT-HEAD VALIDATION REQUIRED`**

## Who can use this workflow

Case handoff is a human incident-response action, not a publication action. The dedicated DTMO permission is `handoff:case`. In the bounded repository role model it is available to CISO, CERT, Senior Analyst and Administrator roles. Publisher/share-approval permission by itself does not authorize a TheHive case handoff, and service accounts cannot authorize one.

## Before you hand off

Confirm that the intelligence item is the correct canonical DTMO record and that the proposed case summary contains only information needed for incident handling. Do not paste credentials, raw source bodies, private enrichment output, attachments or unrelated personal data into the handoff summary.

Choose the effective TLP and PAP that apply to the case. If the effective restrictions are uncertain, do not submit the handoff. Unknown mappings fail closed by design.

## Handoff sequence

1. Open the canonical intelligence item and verify its title, source context and provenance.
2. Prepare a concise analyst-approved case summary.
3. Select the effective TLP and PAP values.
4. Submit the handoff with a unique request UUID.
5. DTMO first commits a durable reservation and then calls TheHive API v1.
6. A confirmed TheHive case identity results in `delivered` status.
7. If delivery is uncertain, DTMO returns an ambiguity/reconciliation error and stores `ambiguous` status. **Do not submit the same incident again with a new request merely to work around an ambiguous response.** Follow the operations runbook.

## What the handoff does not do

A successful handoff does not publish or externally share the DTMO intelligence item. It does not prove that the organization is compromised. It does not change DTMO canonical review state. It creates an operational case in TheHive only after the explicit human action.

## Status meanings

| Status | Meaning | User action |
|---|---|---|
| `reserved` | DTMO committed the request before external mutation | normally transient; do not duplicate |
| `delivered` | stable TheHive case identity confirmed | continue case lifecycle in TheHive |
| `ambiguous` | request may have reached TheHive but identity was not safely confirmed | stop; follow reconciliation runbook |
| `failed` | bounded request failed without confirmed case identity | correct the stated problem before a new governed request |

## Evidence boundary

Repository implementation and CI do not prove that a live TheHive tenant, license, organization or privacy approval is ready. Live use remains dependent on deployment-specific authorization and later Phase 11 validation.

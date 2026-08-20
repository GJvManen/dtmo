# MISP Sharing & Exchange Workspace

Phase 11.10g makes `/workbench/sharing` the canonical operator workspace for governed MISP exchange.

## What the workspace does

Open a canonical DTMO intelligence UUID to inspect its sharing state. The workspace shows the review decision, reviewer attribution, independent share approval, approver attribution, authoritative MISP restrictions, replay/export history and the current export eligibility decision.

## Decision sequence

The normal sequence is:

1. load the canonical intelligence item;
2. record human review when the signed-in principal has `review:intelligence`;
3. have a **different** human principal with `approve:share` approve external sharing;
4. choose a permitted MISP distribution, TLP and—when distribution `4` is used—sharing group;
5. export the approved canonical revision to an **unpublished** MISP event.

The same person may not be both reviewer and share approver for the item. This is enforced server-side; the UI also disables the approval control when the active principal matches the recorded reviewer.

## What export means

`Export approved intelligence` creates the MISP event with `published=false`. It is a governed technical transfer, not a publication decision. Phase 11.10g intentionally provides no **Publish** or **Synchronize** action.

A MISP configuration indicator means only that the required endpoint/key configuration exists server-side. It does not prove that MISP is reachable or healthy.

## MISP-origin intelligence

MISP-origin items can be re-exported only when DTMO has retained the authoritative source restrictions. The server refuses attempts that weaken or change those restrictions, including less restrictive TLP handling.

## Replay and uncertain delivery

DTMO records an export reservation before the external call. A current revision with `pending`, `success` or `uncertain` export evidence cannot be automatically replayed. An `uncertain` result requires operator inspection rather than blind retry.

## Failure interpretation

- **Sharing state unavailable** means the canonical state could not be read. It does not mean the item is approved or denied.
- **Not configured** does not prove MISP is down.
- **No export history** means no persisted DTMO export evidence is available for this item; it is not a statement about upstream MISP data.
- A successful export does not prove publication, synchronization, downstream consumption, local compromise or production readiness.

## Security boundary

The browser communicates only with same-origin DTMO APIs. MISP credentials remain server-side. Server-side RBAC and audit records are authoritative; button visibility is not authorization.

DTMO remains **not production authorized** while Phase 11 industrialisation is in progress.

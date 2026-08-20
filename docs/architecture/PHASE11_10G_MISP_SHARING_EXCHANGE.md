# Phase 11.10g — MISP Sharing & Exchange

Status: **IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED**  
Production status: **not production authorized**

## Purpose

Phase 11.10g replaces the canonical `/workbench/sharing` shell placeholder with a governed MISP sharing workspace. It does not create a new sharing authority model. The workspace composes the already accepted DTMO review, independent human share-approval and replay-protected MISP export contracts into one operator flow.

## Trust path

`browser → DTMO API → canonical governance state → governed MISP export adapter → MISP`

The browser never receives the MISP API key and never calls MISP directly. All browser requests remain same-origin DTMO API calls.

## Authority model

The workflow has intentionally separate authorities:

1. **Read** — `read:intelligence` may inspect canonical sharing state.
2. **Review** — `review:intelligence` may record human intelligence review.
3. **Share approval** — `approve:share` may approve external sharing only after review and only by a human principal different from the reviewer.
4. **MISP export** — the accepted export endpoint also requires `approve:share`, but it accepts only a canonical item that is already reviewed and share-approved with attribution.
5. **MISP publication/synchronization** — outside Phase 11.10g. No publish or synchronization action is exposed by this workspace.

Service accounts cannot perform human review/share approval and cannot export intelligence to MISP.

## Canonical sharing-state API

`GET /api/v1/sharing/items/{item_id}` requires `read:intelligence` and projects only attributable persisted/configuration state:

- canonical item identity and source;
- review state and reviewer attribution;
- share approval and approver attribution;
- authoritative MISP distribution/sharing-group/TLP restrictions when present;
- persisted MISP export status for prior attempts;
- deterministic event UUID for the current canonical revision;
- explicit export blockers;
- role-derived action capability;
- export feature/configuration state;
- explicit false claims for runtime health, publication authority and synchronization authority.

The endpoint does not expose the MISP API key.

## Handling restrictions

For MISP-origin intelligence, DTMO requires an authoritative restriction projection before re-export. Existing governance rejects:

- distribution changes that violate the authoritative source restriction;
- sharing-group changes inconsistent with the source restriction;
- a requested TLP less restrictive than the authoritative source TLP.

The UI surfaces these constraints but does not replace server-side enforcement.

## Export semantics

The accepted export path creates a deterministic MISP event with `published=false`. A replay reservation is committed before the external side effect. `pending`, `success` and `uncertain` evidence for the same canonical revision blocks automatic replay until the recorded state is inspected.

A successful transfer therefore proves only that the governed unpublished event creation completed for that canonical revision. It does **not** prove MISP publication, synchronization, downstream receipt, local compromise, or production readiness.

## Failure behavior

The workspace fails closed:

- missing canonical sharing state is shown as unavailable, not approved;
- missing review/approval attribution blocks export eligibility;
- a reviewer cannot approve their own item for sharing;
- missing authoritative MISP restrictions block re-export of MISP-origin intelligence;
- an uncertain delivery blocks automatic replay;
- configuration is never promoted to live MISP health;
- no browser state creates publication/synchronization authority.

## Acceptance boundary

Repository CI and deterministic browser fixtures validate code-controlled contracts only. They do not prove live MISP availability, production-equivalent operation, independent assurance or production authorization.

Phase 11.10g can become `PASS / REPOSITORY_COMPLETE` only after every workflow registered for its final exact PR head is `completed/success` and the professional documentation is synchronized. The next bounded slice is Phase 11.10h TheHive Investigations & Cases.

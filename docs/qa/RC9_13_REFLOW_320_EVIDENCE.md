# RC9.13 — 320 CSS px Reflow Evidence

Status: `PASS`

## Objective

Produce bounded retained evidence for WCAG 2.2 SC 1.4.10 Reflow on the four accepted critical surfaces: `/ui/share-approval`, `/ui/analyst-search`, `/ui/ciso-security`, and `/ui/auditor`.

## Accepted exact-head evidence

PR #74 exact head `c5b95597bd51867d5fb5af0477e984e3a4fc5be3` completed all 31 registered workflows successfully and was merged with expected-head protection as `fce31bd0032b1adab67f2877608680ce90117fe7`.

Retained artifact `9039233783`, digest `sha256:2f0cd4b7ba97c1dd0c72aa9b6a6d77cb7771c77d212a38e78862263ba08acbd8`, was independently inspected. JUnit reports 1 test, 0 failures, 0 errors and 0 skips.

The machine-readable evidence is exact-head bound and records, for each accepted surface at 320x900 CSS px:

- `documentClientWidth == 320` and `documentScrollWidth == 320`;
- `bodyScrollWidth == 320`;
- the `main` region remains horizontally contained;
- `overflowingVisibleElements` is empty;
- every governed critical control remains visible, horizontally contained and focusable;
- the intended backend-derived session subject/role is resolved;
- no two-dimensional-content exception is used.

Retained server logs show successful real `/api/v1/ui/session` calls on all four surfaces.

## Governance invariants

Backend-derived RBAC remains authoritative. Separation of duties, auditability and separate human share approval are unchanged. No business mutation, production credential or production data is used.

## Claim boundary

This PASS covers only the tested WCAG 2.2 SC 1.4.10 behavior on the four accepted critical surfaces in Chromium at 320x900 CSS px. It does not establish text-spacing conformance, complete focus-order evidence, genuine assistive-technology behavior or product-wide WCAG 2.2 AA conformance.

## Acceptance decision

`PASS` for the bounded RC9.13 scope.

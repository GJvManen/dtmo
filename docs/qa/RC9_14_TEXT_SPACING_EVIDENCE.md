# RC9.14 — WCAG 2.2 Text Spacing Evidence

Status: `PASS`

## Objective

Produce bounded retained evidence for WCAG 2.2 SC 1.4.12 Text Spacing on `/ui/share-approval`, `/ui/analyst-search`, `/ui/ciso-security`, and `/ui/auditor`.

## Evidence method

The dedicated Chromium gate applies the four WCAG text-spacing overrides simultaneously: line-height 1.5, paragraph spacing 2em, letter spacing 0.12em and word spacing 0.16em. It then checks visible text-bearing descendants of `main` for clipping where authored overflow would hide content and verifies every governed critical control remains visible and keyboard-focusable.

The workflow retains exact-head JSON, JUnit and server logs and fails closed on missing or non-conforming evidence.

## Accepted evidence

- PR #76 exact head: `de52730b9b5165f7815e2c6c19c803413bbfcc60`.
- 32/32 registered workflows completed successfully.
- Retained artifact: `9039432903`.
- Artifact digest: `sha256:f547bd306bb9c63e02d049dda24d52d962086388f777f8857921cc818e75c5f1`.
- JUnit: 1 test, 0 failures, 0 errors, 0 skips.
- Required simultaneous overrides retained: line-height `1.5`, paragraph spacing `2em`, letter spacing `0.12em`, word spacing `0.16em`.
- All four surfaces recorded no detected clipped visible text.
- All governed critical controls recorded focusable.
- Real backend-derived `/api/v1/ui/session` RBAC and separate human share approval were preserved.
- PR #76 merged with expected-head protection as `7d4816658159fac3b2b773fa6151b6274b510351`.

## Governance invariants

Backend-derived RBAC remains authoritative. Separation of duties, privacy boundaries, auditability and separate human share approval remain unchanged. No production data or credentials are used.

## Claim boundary

This PASS covers only the bounded SC 1.4.12 check on the four critical surfaces in Chromium. It does not establish complete focus-order evidence, genuine VoiceOver/NVDA behavior, assistive-technology certification or product-wide WCAG 2.2 AA conformance.

## Decision

`PASS` for RC9.14's bounded scope. Phase 6 remains `IN PROGRESS` because complete focus-order evidence and genuine assistive-technology behavior remain open.

# RC9.14 — WCAG 2.2 Text Spacing Evidence

Status: `CI_VALIDATION_PENDING`

## Objective

Produce bounded retained evidence for WCAG 2.2 SC 1.4.12 Text Spacing on `/ui/share-approval`, `/ui/analyst-search`, `/ui/ciso-security`, and `/ui/auditor`.

## Evidence method

The dedicated Chromium gate applies the four WCAG text-spacing overrides simultaneously: line-height 1.5, paragraph spacing 2em, letter spacing 0.12em and word spacing 0.16em. It then checks visible text-bearing descendants of `main` for clipping where authored overflow would hide content and verifies every governed critical control remains visible and keyboard-focusable.

The workflow retains exact-head JSON, JUnit and server logs and fails closed on missing or non-conforming evidence.

## Governance invariants

Backend-derived RBAC remains authoritative. Separation of duties, privacy boundaries, auditability and separate human share approval remain unchanged. No production data or credentials are used.

## Claim boundary

A PASS covers only this bounded SC 1.4.12 check on the four critical surfaces in Chromium. It does not establish complete focus-order evidence, genuine VoiceOver/NVDA behavior, assistive-technology certification or product-wide WCAG 2.2 AA conformance.

## Acceptance gate

PASS requires every registered workflow on the exact final PR head to complete successfully and retained `browser-text-spacing-evidence` to show the required spacing values, no detected clipped text, and visible/focusable governed controls on all four surfaces. Missing, queued, failed, cancelled or unexecuted CI is not PASS.

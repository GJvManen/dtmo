# RC9.15 — Complete Focus-Order Evidence

Status: `CI_VALIDATION_PENDING`

## Objective

Produce bounded retained evidence for WCAG 2.2 SC 2.4.3 Focus Order on `/ui/share-approval`, `/ui/analyst-search`, `/ui/ciso-security`, and `/ui/auditor`.

## Evidence method

The dedicated Chromium gate waits for each backend-derived session surface to resolve, enumerates every visible enabled tabbable control in DOM order, rejects positive `tabindex`, then drives the actual keyboard Tab sequence across every tabbable exactly once and compares the observed sequence to the logical DOM sequence. It also verifies reverse `Shift+Tab` behavior: multi-control surfaces must move to the immediately preceding tabbable; a surface with exactly one tabbable control must exit to the document boundary (`body` or `html`).

The workflow retains exact-head JSON, JUnit and server logs and fails closed on missing or non-conforming evidence.

## Deterministic first-run finding

The initial PR head `f6c0d2fade7646c469dc7993d5dbefbd92397a53` failed because the original test oracle expected a one-control surface to retain that same control after `Shift+Tab`. Chromium correctly returned focus to `body` on `/ui/auditor`. This was a test-oracle defect, not an application focus-order defect. The oracle was repaired without changing production code.

## Governance invariants

Backend-derived RBAC remains authoritative. Separation of duties, privacy boundaries, auditability and separate human share approval remain unchanged. No production data, credentials or business mutations are used.

## Claim boundary

A PASS covers only the bounded SC 2.4.3 keyboard focus-order behavior on the four critical surfaces in Chromium. It does not establish genuine VoiceOver/NVDA behavior, assistive-technology certification or product-wide WCAG 2.2 AA conformance.

## Acceptance gate

PASS requires every registered workflow on the exact final PR head to complete successfully and retained `browser-focus-order-evidence` to show every tabbable reached exactly once in DOM-logical order, no positive `tabindex`, and valid reverse navigation on all four surfaces. Missing, queued, failed, cancelled or unexecuted CI is not PASS.

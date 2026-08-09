# RC9.15 — Complete Focus-Order Evidence

Status: `PASS`

## Objective

Produce bounded retained evidence for WCAG 2.2 SC 2.4.3 Focus Order on `/ui/share-approval`, `/ui/analyst-search`, `/ui/ciso-security`, and `/ui/auditor`.

## Evidence method

The dedicated Chromium gate waits for each backend-derived session surface to resolve, enumerates every visible enabled tabbable control in DOM order, rejects positive `tabindex`, then drives the actual keyboard Tab sequence across every tabbable exactly once and compares the observed sequence to the logical DOM sequence. It also verifies reverse `Shift+Tab` behavior: multi-control surfaces move to the immediately preceding tabbable; a surface with exactly one tabbable control exits to the document boundary (`body` or `html`).

The machine-readable validator compares semantic focus identity fields (`tag`, `id`, `testid`, `name`, `type`, `text`) rather than representation-only metadata. Positive `tabindex` remains separately prohibited.

## Accepted evidence

Final PR #78 exact head `d2480293f605e8701fb677071c206cc25da97098` completed all 33 registered workflows successfully. Retained `browser-focus-order-evidence` artifact `9039862032` has digest `sha256:09f1f756d0ddddb6d381f0a724938ec3408c8692be0dd61727b36be0dd29fed4` and is bound to that exact head.

JUnit reports 1 test, 0 failures, 0 errors and 0 skips. The retained JSON shows every tabbable reached exactly once in DOM-logical order, no positive `tabindex`, valid reverse navigation on all four surfaces, real backend-session RBAC, and preserved separate human share approval. Server logs retain successful `/api/v1/ui/session` calls for all four critical surfaces.

PR #78 was merged with expected-head protection as `17a43175d6beda4fdf0156f701844d2c25ea4aec`.

## Governance invariants

Backend-derived RBAC remains authoritative. Separation of duties, privacy boundaries, auditability and separate human share approval remain unchanged. No production data, credentials or business mutations are used.

## Claim boundary

PASS covers only the bounded SC 2.4.3 keyboard focus-order behavior on the four critical surfaces in Chromium. It does not establish genuine VoiceOver/NVDA behavior, assistive-technology certification or product-wide WCAG 2.2 AA conformance.

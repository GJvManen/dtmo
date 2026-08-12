# RC13 — Functional Console Acceptance Gate

Status: `REOPENED / BLOCKED_INTERNAL`

## Trigger

A project-owner functional test of `http://localhost:8000/` on 2026-08-11 first showed that repository-controlled component evidence did not prove a usable product. RC13.1–RC13.5 repaired the initial blockers and repository browser evidence passed. The accountable project owner explicitly accepted that repaired journey on 2026-08-12.

A **subsequent project-owner functional retest on 2026-08-12** found additional blocking product defects. That newer owner-observed evidence supersedes the earlier acceptance for the current release decision and reopens RC13.

## Reopened owner-observed blockers

1. Overview **`Alles vernieuwen`** does not function as a usable/reliable operator action.
2. The console can state **`Data bijgewerkt`** while no canonical intelligence data exists.
3. Buttons are not reliably functional under Chrome.
4. The release/version badge in the product navigation is unnecessary clutter.
5. Administration is not sufficiently clear/usable.
6. Graphs are not truthful/useful when datasets are empty.

## Confirmed implementation gaps

Repository inspection confirms at least these root causes in the pre-repair `main` implementation:

- `loadDashboard()` unconditionally changed the global status to `Data bijgewerkt` after a successful summary response, even when `total_intelligence == 0` and recent intelligence was empty.
- the dashboard trend API always returns seven date buckets, so an empty dataset still produced zero-height pseudo-bars instead of a clear empty state;
- the canonical Administration base markup still contained stale pre-RC13.3 copy and legacy source/identity panels, while governed RBAC was appended below that surface;
- the earlier RC13.5 E2E journey did not explicitly gate `Alles vernieuwen`, zero-data semantics, broad button interaction, browser page errors or browser console errors.

## Current bounded repair

The reopened RC13 repair must prove:

1. `Alles vernieuwen` visibly enters a loading state, executes source/dashboard/recent-intelligence refreshes and returns to an enabled state;
2. a successful empty response reports **`Geen intelligence data · bronstatus geladen`**, never `Data bijgewerkt`;
3. partial refresh failure is visible and cannot be reported as success;
4. zero-only intelligence datasets render explicit empty states instead of ambiguous bars;
5. real connector state may still render when it contains measurable operational values;
6. all non-submit product controls use explicit button semantics and the canonical navigation remains functional under the Google Chrome browser channel;
7. browser acceptance captures and requires zero page errors and zero console errors;
8. the navigation version badge is absent;
9. Administration presents governed user/role management as the central surface, with source management kept in `Bronnen & catalogus` and local development identity context de-emphasized;
10. RBAC, separation of duties, privacy, provenance, auditability, human review and separate external share approval remain unchanged.

## Historical RC13 evidence

The following remains valid historical repository evidence and is not rewritten:

- RC13.1 — PR #151 / merge `95c4a5b072d141f50a02d23f8bf9abb862d6f8e2`;
- RC13.2 — PR #152 / merge `b8c254c5d099cde5dca624aa85b17c320594847e`;
- RC13.3 — PR #153 / merge `2e1029a43f7b44d8525fb89197d0a10458a3e992`;
- RC13.4 — PR #154 / merge `21672aaf1cf097228699810660eaac167da842d6`;
- RC13.5 — PR #155 / merge `d6f83557ab18d26f82ad6289b1b95f728346631d`;
- post-RC13.5 reconciliation — PR #156 / merge `e0119b2eb1865ad5b4f2634fd71ccd809fba96a0`;
- Phase 8 transition/intake — PR #157 / merge `a7b7b1503bd7206bd026f87038cb709f141a9459`.

The earlier statement `RC13 owner retest akkoord` is retained as historical accountable evidence, but it no longer closes the gate because the same project owner subsequently reported new blocking defects.

## Current decision

**RC13 = REOPENED / BLOCKED_INTERNAL.** Issue #150 is open.

**Phase 8 = `PAUSED_PENDING_RC13_REPAIR_AND_OWNER_RETEST`.**

No staging, pentest or production-readiness progression is permitted until the repair passes complete exact-head CI, is merged, and the accountable project owner explicitly retests and accepts the repaired local product again.

## Exactly one next priority

Complete the reopened canonical-console usability repair and exact-head Chrome/browser evidence, then require accountable project-owner functional retest.

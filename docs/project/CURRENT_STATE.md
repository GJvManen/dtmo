# DTMO Current Project State

Last reconciled: **2026-08-12**

## Executive summary

DTMO `16.0.0rc12` has accepted repository-controlled engineering through Phase 7. RC13.1–RC13.5 and the earlier owner acceptance remain historical evidence, but a subsequent project-owner functional retest on 2026-08-12 identified new blocking canonical-console defects.

**RC13 = `REOPENED / BLOCKED_INTERNAL`.**

**Phase 8 = `PAUSED_PENDING_RC13_REPAIR_AND_OWNER_RETEST`.**

DTMO remains **not production ready**.

## Phase status

| Phase | Status |
|---|---|
| 1. CI and workflow integrity | `PASS` |
| 2. Application security and identity | `PASS` |
| 3. Data integrity and recovery | `PASS` |
| 4. Connector reliability and provenance | `PASS` |
| 5. Performance and scalability | `PASS` |
| 6. Accessibility and operational UX | `PASS` |
| 7. Observability and incident operations | `PASS` |
| RC13. Functional unified-console acceptance | `REOPENED / BLOCKED_INTERNAL` |
| 8. Real staging acceptance | `PAUSED_PENDING_RC13_REPAIR_AND_OWNER_RETEST` |
| 9. Independent external assurance | `NOT COMPLETE` |
| 10. Production go/no-go | `NOT STARTED` |

## New owner-observed blockers

The current blocking findings are:

- Overview `Alles vernieuwen` did not function as a reliable operator action;
- `Data bijgewerkt` could be shown although canonical intelligence was empty;
- buttons were not reliably functional under Chrome;
- the navigation version badge was unnecessary;
- Administration was unclear and mixed governed management with legacy/development controls;
- zero-only graph datasets were visually ambiguous.

## Current repair state

The repair branch makes the following changes:

- refresh-all has explicit loading, completion and partial-failure states;
- empty intelligence reports `Geen intelligence data · bronstatus geladen`;
- zero-only intelligence datasets render an explicit `Geen data om te visualiseren` state;
- navigation and non-submit controls use explicit button semantics;
- a dedicated Google Chrome-channel E2E covers refresh, navigation, Administration, Governance and requires zero page/console errors;
- the menu version badge is removed;
- governed `Gebruikers & rollen` is visually prioritized in Administration;
- source administration is kept in `Bronnen & catalogus` and technical local identity context is de-emphasized.

Repository-controlled evidence remains synthetic where APIs are fixture-backed. It cannot replace project-owner acceptance after merge.

## Historical evidence boundary

PRs #151–#157 and the earlier `RC13 owner retest akkoord` remain immutable historical evidence. They do not establish current acceptance after newer owner-observed defects.

## Phase 8 boundary

The Phase 8 intake/deployment identity record from PR #157 remains fail-closed preparatory evidence. Issue #158 is paused. No external staging, pentest or production-readiness progression is allowed while issue #150 remains open.

## Security and governance boundaries

Credentialed integrations use logical secret references only. Production bearer tokens remain externally issued. RBAC, least privilege, separation of duties, privacy, provenance, auditability, human review and separate external share approval remain authoritative. Source execution, analytics, Administration, Governance, CI or staging access cannot authorize publication.

## Exactly one current priority

**Issue #150 — complete the canonical-console usability repair, complete exact-head Chrome/browser CI, merge, and require accountable project-owner functional retest again.**

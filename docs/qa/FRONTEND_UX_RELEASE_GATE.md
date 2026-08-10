# Frontend UX Release Gate — DTMO 16.0.0rc6

## Scope

This gate evaluates the repository-controlled professional frontend baseline introduced in 16.0.0rc6. It does not substitute for genuine assistive-technology execution or external user acceptance.

## Required repository evidence

The final exact release head must demonstrate:

1. root console is discoverable at `/` and `/ui/console`;
2. Overview, Intelligence, Governance, Audit and Security work areas are present and navigable;
3. specialized Analyst, Share Approval, Auditor and CISO views remain available;
4. search, review, share approval, audit read and token revocation remain wired to existing governed API endpoints;
5. client-side permission presentation never replaces server-side RBAC enforcement;
6. review and external share approval remain separate actions and permissions;
7. audit evidence remains read-only;
8. local/dev/staging identity helper uses `sessionStorage`, not `localStorage`, and does not embed credentials;
9. UI responses retain CSP/no-store/anti-framing protections;
10. keyboard focus, skip navigation, responsive reflow, reduced motion and live status semantics are retained;
11. registered browser/accessibility regression workflows execute on the final exact head;
12. all registered workflows complete successfully before release acceptance.

## External evidence not satisfied here

This gate does **not** claim completion of:

- genuine VoiceOver behavior;
- genuine NVDA behavior;
- real staging deployment parity;
- independent penetration testing;
- external operational/stakeholder acceptance;
- production go/no-go.

## Governance invariants

RBAC, least privilege, separation of duties, privacy, provenance, append-only auditability and human share approval remain mandatory. A visual affordance or disabled control is not an authorization control; the server is authoritative.

## Current decision

`CI_VALIDATION_PENDING` until every registered workflow succeeds on the final exact PR head.

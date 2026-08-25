# Phase 11.10q — Canonical Administration Security & Audit Recovery

## Purpose

This slice removes the remaining primary security/audit administration dependency on legacy `/ui/*` pages without changing DTMO's authorization model. The canonical `/workbench/administration` route now renders privileged token revocation and read-only audit evidence next to the existing integration and identity/RBAC control-plane functions.

## Canonical contracts

- Session capability discovery: `GET /api/v1/ui/session`.
- Token revocation: `POST /api/v1/security/tokens/revoke` with same-origin credentials and a unique `X-Request-ID`.
- Audit evidence: `GET /api/v1/audit/events?limit=50`.

The browser never receives revocation-store credentials, signing material, bearer-token secrets or integration credentials. Token-state mutation, `revoke:tokens` authorization and the persistent audit event remain server-side. Audit evidence remains guarded by `read:audit` and is exposed as a read-only append-only projection.

## Authority boundaries

The canonical UI does not create independent security authority. Service accounts are not offered the human token-revocation control. Viewing audit evidence does not grant mutation, intelligence review, share approval, publication or external-assurance authority. Empty audit results are not interpreted as proof that no activity has occurred outside the accessible persistence boundary.

Legacy `/ui/ciso-security` and `/ui/auditor` endpoints remain compatibility paths only. They are no longer required as primary navigation for these administration tasks.

## Acceptance evidence

`backend/tests/test_phase11_10q_administration_security_audit.py` verifies canonical rendering, same-origin API usage, permission markers, server-side authorization contracts, read-only audit semantics and absence of primary legacy navigation. `.github/workflows/phase11-10q-administration-security-audit.yml` builds the React head and runs that contract on every relevant pull-request change.

This repository-controlled evidence does not constitute owner functional acceptance, staging validation, production-equivalent validation or external assurance. Phase 11.10q remains blocked until the owner completes the required functional retest.

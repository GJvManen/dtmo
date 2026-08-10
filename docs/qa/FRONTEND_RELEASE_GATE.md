# DTMO Frontend Release Gate — 16.0.0rc5

Status: `CI_VALIDATION_PENDING`

## Scope

This gate covers the repository-controlled DTMO web console introduced in 16.0.0rc5. It does not close the separate external VoiceOver/NVDA blocker, real staging deployment-parity gate, or Phase 9 independent assurance gates.

## Required behavior

The release is acceptable only when the final exact PR head proves all of the following:

1. `/` and `/ui/console` return the governed DTMO console instead of a 404 response.
2. The console exposes runtime health/version/environment, connector status, intelligence search, review/share decisions, read-only audit evidence and CISO token revocation.
3. RBAC continues to govern all protected API actions server-side; hiding/disabling controls in the browser is not an authorization boundary.
4. Review and external share approval remain separate decisions and service accounts cannot acquire human publication authority.
5. Development/staging test identity material is restricted to per-tab `sessionStorage`; bearer tokens are not persisted by this console.
6. Content Security Policy, no-store behavior for dynamic HTML/JS, frame blocking, no-sniff and referrer protections remain in force.
7. Keyboard focus is visible; a skip link is present; live status regions are used; layout reflows responsively; reduced-motion preference is honored.
8. Existing dedicated analyst, share-approval, auditor and CISO surfaces remain available.
9. Docker Compose passes `OPENSEARCH_INITIAL_ADMIN_PASSWORD` to OpenSearch so the documented local startup path is reproducible with external secret input.
10. No real credential, token, password, license content or unnecessary personal data is committed.

## Evidence

Repository regression: `backend/tests/test_frontend_console.py`.

The final decision requires the complete registered GitHub Actions matrix on one exact head. Workflow presence, queued execution, partial success or stale-head evidence is not PASS.

## Claim boundary

A PASS for this gate proves only the repository-controlled frontend/deployment contract. Genuine VoiceOver/NVDA execution, production-equivalent staging, penetration testing and other external acceptance remain independently required.

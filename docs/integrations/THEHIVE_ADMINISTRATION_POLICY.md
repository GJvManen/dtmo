# TheHive Administration policy

## Purpose

Canonical Administration owns TheHive runtime configuration readiness. A TheHive integration is not considered ready merely because an API endpoint and server-side credential exist. DTMO also requires an explicit organization scope before governed handoff can be activated.

## Canonical configuration

An operator with server-authorized `manage:connectors` can configure the following values from **Administration → Framework integrations → TheHive**:

- API endpoint;
- write-only server-side credential replacement;
- **TheHive organization scope**;
- explicit enablement.

`thehive_organization` is non-secret runtime policy and is stored in the existing runtime integration settings document. The API credential remains in the separate server-side secret store and is never returned to the browser.

## Fail-closed readiness

The Administration read model uses the shared `integration_readiness()` contract for TheHive. When endpoint, credential or organization scope is missing, activation remains blocked and the missing requirement is returned as an activation blocker. Submitting TheHive organization policy to another integration is rejected with HTTP 422.

Saving configuration is not evidence that TheHive is reachable, healthy, complete or current. Runtime observations remain separate evidence.

## Authority boundary

Organization configuration does not create a TheHive case and does not authorize a handoff. The governed object-driven handoff remains in the Investigations workflow and retains its own RBAC, review and provenance controls. Administration does not grant responder, remediation, review, sharing, publication, external-assurance or production authority.

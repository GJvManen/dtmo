# Administration activation-readiness recovery

## Objective

Restore the first bounded operator workflow after the 2026-08-26 external functional rejection: expose DTMO's existing governed framework activation-readiness control inside the canonical Administration route.

## Verified integration defect

`frontend/src/FrameworkIntegrationReadiness.tsx` already implemented explicit activation for configured-but-disabled integrations, but the component was not mounted by the canonical `/workbench/administration` route. Operators therefore could configure integrations while the corresponding activation-readiness control remained disconnected from the product UI.

## Recovery behavior

The Administration route now mounts the readiness surface between governed runtime configuration and the security-audit surface. The control:

- reads integration state only through the same-origin DTMO administration API;
- is visible only to principals with `manage:connectors`;
- offers activation only when an endpoint and server-side credential are present;
- requires an explicit human click and never auto-enables an integration;
- preserves component-specific readiness checks such as scopes and analyzer/entity allowlists;
- persists enablement through the existing governed administration endpoint with a request ID;
- never returns stored credential values to the browser.

## Repository-controlled functional evidence

The Phase 11.10q same-origin browser acceptance journey configures MISP as disabled with an `.invalid` endpoint and a write-only server-side credential, opens canonical Administration, verifies the activation-readiness card, explicitly activates MISP, reads the persisted state back from DTMO, reloads the page, and verifies the enabled state remains visible.

No connector execution occurs in that journey, so the `.invalid` MISP endpoint is never contacted. The test proves DTMO UI/API/persistence integration only; it does not prove live MISP health, external connectivity, production-equivalent operation, external assurance or production authorization.

## Security boundary

This recovery does not change RBAC, provenance, fail-closed behavior, human share/publication authority or server-side credential storage. Missing endpoint/credential/scope/allowlist configuration continues to block activation or runtime readiness as defined by the existing backend policy.
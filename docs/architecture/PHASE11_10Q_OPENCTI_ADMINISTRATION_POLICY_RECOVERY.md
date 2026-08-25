# Phase 11.10q OpenCTI Administration policy recovery

Canonical Administration must be able to configure the non-secret OpenCTI runtime policy that shared readiness already requires. Endpoint and credential alone are insufficient.

The bounded recovery contract requires persisted `opencti_allowed_entity_types` and `opencti_checkpoint_path`, both editable through the same-origin, server-authorized Administration control plane. OpenCTI must use the shared fail-closed readiness model so missing policy remains `configuration-required` and is surfaced through activation blockers.

These settings are configuration only. They do not prove OpenCTI runtime health, graph freshness, source completeness, review status, publication status or external assurance. Credentials remain write-only/server-side.

OpenCTI graph discovery and population remain in the governed Knowledge Graph workflow. Administration must not gain a direct `Run OpenCTI` action as part of this slice.
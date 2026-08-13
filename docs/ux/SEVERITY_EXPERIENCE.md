# DTMO Severity Experience

Status: `ACCEPTED_MERGED`

E1/E2 provides one shared severity model across Overview and Intelligence: informational, low, medium, high and critical. Colour is supplementary to labels, counts and accessible filter controls; severity is never communicated by colour alone.

The shared filter applies to Overview KPI totals, 24-hour counts, average confidence, severity distribution and recent intelligence. Recent intelligence is filtered server-side; governed search composes with the same severity selection. Empty filtered states remain truthful and filtering never reclassifies canonical intelligence.

The console contract uses `GET /api/v1/console/severity-summary` and repeatable `severity` parameters on recent intelligence. Unknown severity values fail closed with HTTP 400.

This feature does not change RBAC, review authority, external-share approval, provenance, auditing or framework mapping truth. Severity never implies a Normenkader IBP control, MITRE ATT&CK technique or other framework relationship.

## Release evidence

Accepted with complete exact-head CI and merged through PR #175 on 2026-08-12. Merge commit: `156843bfbe005c4207388cca6d9bbd0a7f89388a`.

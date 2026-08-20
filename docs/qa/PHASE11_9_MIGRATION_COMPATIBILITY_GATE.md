# Phase 11.9 Migration Compatibility Gate

Status: **IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED**

The required workflow is `.github/workflows/phase11-migration-compatibility.yml`.

A passing gate requires the repository migration set to form exactly one connected single-root/single-head graph, every revision to expose explicit upgrade and downgrade functions, the compatibility policy to require forward migration before application cutover, and automatic database down migration to remain forbidden.

The workflow emits `phase11-migration-compatibility-evidence` bound to the exact pull-request head. Missing, failed, stale, skipped or mismatched evidence is not acceptance.

This gate does not prove live migration success, representative production data compatibility, production-equivalent continuity, independent assurance or production authorization. Those remain later Phase 11.10, 11.11 and Phase 12 gates.

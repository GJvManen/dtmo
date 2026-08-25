# Object context default behavior

## Purpose

The canonical DTMO workbench keeps the **Context → Object details** rail closed by default. Initial workspace load prioritizes the selected operational workspace instead of reserving horizontal space for an empty object-detail surface.

## Interaction contract

The context rail opens only through explicit user action from the shell toggle, or through a future deliberate object-selection interaction that is separately implemented and tested. Closing or reopening the rail is presentation state only.

When no canonical object is selected, DTMO does not infer object facts merely because an integration is configured. The existing empty-state evidence boundary remains authoritative.

## Security and authority boundary

This UX change does not change server-side authorization, RBAC, provenance, review/share/publication authority, connector execution authority, credential handling or upstream-service trust boundaries. The browser remains an unprivileged same-origin DTMO client.

## Acceptance boundary

This document records one bounded owner-reported UX remediation. It is not evidence of broader functional acceptance, production-equivalent validation, independent assurance or production authorization. Administration, automatic collection, framework integration and analytics recovery remain separate functional blockers until independently remediated and retested.

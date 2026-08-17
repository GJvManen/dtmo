# TheHive Handoff Configuration — Administration Guide

Status: **`PHASE 11.6 BOUNDED IMPLEMENTATION / EXACT-HEAD VALIDATION REQUIRED`**

## Scope

This guide covers only configuration of the minimal DTMO→TheHive case-handoff path. It does not authorize TheHive platform administration, organization administration, responder/Cortex execution, automatic MISP→TheHive workflows or external sharing.

## Runtime settings

The integration is disabled by default. Configure only after deployment prerequisites are approved:

- `DTMO_FEATURE_THEHIVE_HANDOFF=true` — enables the DTMO handoff endpoint;
- `DTMO_THEHIVE_API_BASE` — HTTPS base URL of the approved TheHive service;
- `DTMO_THEHIVE_API_TOKEN` — runtime-only token for the dedicated non-human service identity;
- `DTMO_THEHIVE_ORGANIZATION` — explicit organization scope.

Never commit the token to the repository, screenshots, evidence bundles or support notes.

## RBAC

The dedicated DTMO permission is `handoff:case`. The bounded role assignment is CISO, CERT, Senior Analyst and Administrator. SOC, Analyst, Reviewer, Publisher and Service Account roles do not receive this permission. Publication/share approval remains separate.

TheHive's service identity is non-human and exists only to execute the already-authorized API mutation. It does not receive DTMO human approval authority.

## Database migration

Apply migration `0014_thehive_handoff_state` before enabling the feature. Verify that `thehive_handoff_state` exists and that the no-share/no-local-compromise constraints are present. The migration remains in the Alembic chain after `0013_misp_synchronization_state`.

## Deployment prerequisites

Before live enablement verify, outside repository CI: activated TheHive entitlement permitting the write operation; HTTPS trust and network path; dedicated service identity restricted to the approved organization and minimum case-create permission; privacy/data-handling approval; approved TLP/PAP mapping profile; secret-management and rotation; and an operator process for `ambiguous` handoffs.

## Failure handling

Do not compensate for `401`, `403`, licensing/read-only rejection, organization mismatch or `ambiguous` delivery by broadening permissions, switching to an administrator token or blind-retrying the mutation. Fix deployment configuration or execute governed reconciliation.

## Evidence boundary

A green repository gate proves neither TheHive entitlement nor effective runtime permissions. Deployment-bound evidence belongs to later Phase 11.10 validation and Phase 11.11 independent assurance for the same integrated candidate.

# TheHive Handoff Operations Runbook

Status: **`PRE-IMPLEMENTATION / CONTRACT BASELINE`**

## Purpose

This runbook defines the operational controls that must exist before enabling any live DTMO→TheHive case mutation. No live handoff is authorized by this document alone.

## Preconditions

Before runtime enablement, operators must verify:

- approved TheHive instance and organization;
- activated Community/Gold/Platinum entitlement appropriate to the deployment;
- HTTPS certificate validation;
- dedicated non-human service identity with minimum case-handoff permissions;
- runtime secret storage outside the repository;
- deterministic DTMO severity/TLP/PAP/access mappings;
- privacy/data-minimization approval for the handoff payload;
- durable DTMO handoff reservation/mapping persistence;
- explicit human case-handoff RBAC and audit attribution.

## Normal handoff

1. Analyst selects a canonical DTMO intelligence item and explicitly approves case handoff.
2. DTMO validates actor permission, canonical identity, provenance, handling restrictions and target organization.
3. DTMO creates a durable handoff reservation/idempotency record before mutation.
4. DTMO sends the minimized case payload to TheHive API v1.
5. On an unambiguous successful response, DTMO records the returned TheHive case identity and outcome.
6. TheHive owns subsequent case lifecycle state; DTMO canonical CTI remains unchanged unless separately governed updates occur.

## Fail-closed conditions

Do not send or retry when approval, identity, provenance, target organization, TLP/PAP/access mapping or license/write state is unknown. Treat `401`, `403`, read-only/license failures, malformed responses and conflicting identity mappings as hard failures.

If delivery times out or the response is ambiguous after the request may have reached TheHive, **do not blind-retry**. Mark the reservation uncertain and reconcile against TheHive before any further mutation.

## Recovery and rollback

A failed handoff never rolls back canonical DTMO intelligence. If TheHive created a case but DTMO did not receive a definitive response, reconcile and bind the existing case rather than creating a duplicate. Case deletion or ownership/access mutation is not an automatic rollback mechanism and requires separate governed authority.

## Observability

Record actor/principal, canonical item identity, handoff request identity, target organization, correlation/request identity, sanitized outcome and mapped TheHive case identity. Never log tokens, credentials, raw sensitive payload bodies or attachments.

## Evidence boundary

Repository tests and runbooks do not prove a live TheHive environment, license entitlement, deployed permission scope, privacy approval, operational readiness or production authorization. Those require fresh later Phase 11 deployment-bound evidence.

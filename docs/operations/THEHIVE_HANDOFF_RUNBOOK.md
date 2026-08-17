# TheHive Handoff Operations Runbook

Status: **`BOUNDED IMPLEMENTATION / EXACT-HEAD VALIDATION REQUIRED`**

## Purpose

This runbook governs the repository implementation of the minimal DTMO→TheHive case handoff. It does not authorize live enablement by itself. Live writes remain blocked until the deployment-specific license, credentials, organization, privacy/handling and later validation dependencies are satisfied.

## Preconditions

Before enabling `DTMO_FEATURE_THEHIVE_HANDOFF=true`, operators must verify:

- approved TheHive instance and explicit organization scope;
- activated Community/Gold/Platinum entitlement appropriate to the deployment;
- HTTPS certificate validation;
- dedicated non-human TheHive identity with only the accepted case-create permission;
- `DTMO_THEHIVE_API_TOKEN` held in runtime secret storage outside repository/evidence;
- approved TLP/PAP mapping and privacy/data-minimization profile;
- migration `0014_thehive_handoff_state` applied;
- human user has the dedicated DTMO `handoff:case` permission;
- publication/share approval is not being treated as case-handoff authority.

## Normal handoff

1. A human with `handoff:case` selects a canonical DTMO intelligence item and submits a unique handoff request UUID plus analyst-approved summary and effective TLP/PAP.
2. DTMO verifies the canonical item exists and has repository provenance.
3. DTMO maps title, severity, TLP/PAP and bounded tags; unknown handling mappings fail closed.
4. DTMO commits a `reserved` row to `thehive_handoff_state` before any external mutation.
5. DTMO sends the minimized payload to `POST /api/v1/case` using the dedicated TheHive service identity and configured organization.
6. A stable returned case identity transitions the reservation to `delivered` and persists the mapping.
7. TheHive owns subsequent case lifecycle state. DTMO canonical CTI, compromise semantics and share/publication authority remain unchanged.

## Fail-closed conditions

Do not send when human case-handoff permission, canonical identity, provenance, target organization, token, TLP/PAP mapping or feature enablement is missing. Authentication/authorization or write/licensing rejection is recorded as `failed` and does not broaden authority.

If a timeout/network ambiguity occurs after a request may have reached TheHive, or a success response lacks stable case identity, transition the reservation to **`ambiguous`**. Do not blind-retry that request UUID. Reconciliation is required before any later governed recovery action.

A reused request UUID that points to another item/principal/organization, or that is already `delivered`/`ambiguous`, is rejected.

## Reconciliation procedure

For an `ambiguous` row:

1. record the DTMO request UUID, canonical item UUID, organization and timestamp;
2. inspect TheHive using an operator with separately authorized read access;
3. determine whether a corresponding case already exists using durable identifiers/provenance, not mutable title or description;
4. do not create a replacement case automatically;
5. retain the row as evidence until a separately governed reconciliation capability is implemented.

This bounded slice intentionally does not provide an administrative override, delete, ownership-change or replay endpoint.

## Recovery and rollback

A failed handoff never rolls back canonical DTMO intelligence. TheHive case deletion or access/ownership mutation is not an automatic rollback mechanism. Those operations remain outside the accepted API allowlist and require separate governance.

## Observability and audit

Persist actor/principal, canonical item identity, handoff request identity, organization, TLP/PAP authority snapshot, state transition and sanitized upstream outcome. Do not log or persist the API token, credentials, attachments or raw sensitive request bodies as evidence.

## Health isolation

TheHive unavailability affects only the explicit handoff request. It must not make DTMO intelligence reads, source ingestion, governance, MISP, OpenCTI or IntelOwl paths unavailable.

## Evidence boundary

Repository tests can establish route, RBAC, state-machine, migration and fail-closed contract behavior using synthetic data. They cannot prove live TheHive connectivity, effective service-account permissions, license entitlement, organization configuration, privacy approval, correct real-data handling, HA/recovery, production-equivalent validation, independent assurance or production authorization.

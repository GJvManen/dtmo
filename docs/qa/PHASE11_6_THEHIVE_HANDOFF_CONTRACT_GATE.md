# Phase 11.6 TheHive Handoff Contract Gate

Status: **`IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`**

## Objective

Validate the bounded Phase 11.6 TheHive service/API/identity/licensing/authority contract before any runtime mutation adapter is implemented.

## Acceptance criteria

The contract must explicitly preserve all of the following:

- TheHive remains a separate service and DTMO does not vendor upstream source;
- reviewed upstream baseline is TheHive 5.5.16 and API v1 (`/api/v1`);
- TheHive 5.3+ write operation depends on an activated license/entitlement appropriate to deployment;
- case creation is not automatic and requires explicit human-authorized DTMO handoff;
- server-side RBAC distinguishes case-handoff authority from publication/share authority;
- stable DTMO and TheHive identities plus a durable idempotency/handoff reservation are required;
- uncertain mutation delivery blocks blind replay;
- TLP/PAP/access mapping is fail-closed and cannot broaden authoritative restrictions;
- attachments/raw bodies/private enrichment/personal data are excluded by default;
- TheHive case state does not become canonical CTI truth, local-compromise proof or DTMO share authority;
- administration, Cortex execution, responder execution, automatic MISP→TheHive automation and external sharing remain excluded;
- repository CI is engineering evidence only and cannot substitute for deployment, licensing, privacy, assurance or production evidence.

## Required repository evidence

- `docs/architecture/THEHIVE_DTMO_HANDOFF_CONTRACT.md`
- `backend/tests/test_thehive_handoff_contract.py`
- `.github/workflows/phase11-thehive-handoff-contract.yml`
- synchronized Phase 11 lifecycle/current-state documentation

## Failure policy

Any missing authority, identity, licensing, restriction, idempotency or evidence boundary fails the gate. A green repository gate does not authorize live case creation.

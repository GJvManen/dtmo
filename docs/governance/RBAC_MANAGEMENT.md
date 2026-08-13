# Administration RBAC Management

## Purpose

E6 extends the existing managed-principal administration model with a first-class role-to-permission matrix and a governed assignment-change path. It does not introduce a second authorization model, browser-defined roles, or free-form permissions.

## Policy source of truth

Roles and permissions remain defined server-side in `dtmo.auth.policy`. The Administration matrix is a read-only projection of that policy. Human principals may receive only human roles; service accounts remain restricted to the dedicated `service_account` role.

## Governed assignment changes

Role/status changes made through the E6 Administration surface require a concrete change reason. The API records the authenticated human actor, request/correlation identifier, reason, and normalized before/after managed-principal state in the existing tamper-evident persistent audit chain.

After a successful governed update, the Administration card reconciles its visible state from the canonical server response. Display name, active/inactive status and selected roles therefore reflect the accepted persisted assignment immediately; the UI does not present an audit-success message while retaining stale pre-save state.

Existing safety invariants remain authoritative:

- administrators cannot change their own managed assignment;
- the last active managed human administrator cannot be removed or deactivated;
- service accounts cannot combine machine and human/administrator roles;
- assignments are constrained to the immutable server-side role catalogue;
- production token claims are not rewritten by DTMO and require identity-provider reconciliation/token reissue.

## Separation of duties

RBAC administration does not constitute intelligence review or external-share approval. `review:intelligence` and `approve:share` remain independent permissions and external sharing continues to require a distinct authorized human approver under the existing policy contract. A user who can administer assignments cannot bypass these runtime checks merely by viewing or editing Administration data.

## UI

The unified Administration view exposes:

- the complete role-to-permission matrix;
- textual policy-boundary cards in addition to visual matrix marks;
- existing managed-principal state and role controls;
- a required reason field before governed assignment changes are submitted;
- immediate reconciliation of the card from the accepted server-side principal state;
- request/correlation evidence after a successful update.

The matrix uses textual headers and explicit accessible labels; permission state is never communicated by colour alone.

## Release gate

E6 is accepted only when its focused contract gate and all returned exact-head regression workflows complete successfully. A new commit invalidates previous exact-head evidence.
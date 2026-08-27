# R2 Administration Information Architecture

Status: **IN PROGRESS — repository-controlled recovery slice**

## Owner finding addressed

Administration is already available on the canonical workbench route, but the current page is long and combines readiness, integrations, identity/RBAC and security/audit controls without a stable information architecture. The result does not yet feel like one coherent administrative console.

## This bounded slice

R2 introduces one canonical Administration console wrapper for `/workbench/administration` with stable section navigation for:

- Overview;
- Integrations;
- Sources;
- Identity;
- Roles & Permissions;
- Security & Audit.

Overview keeps bundled-platform and framework readiness together. Integrations, Identity, Roles & Permissions and Security & Audit navigate to the existing canonical sections without reloading or opening a legacy application. Sources intentionally opens the canonical Sources & Collection workspace because source lifecycle execution belongs there rather than duplicating that authority inside Administration.

The existing governed Administration workspace remains the implementation authority for connector configuration and identity/RBAC mutations. The existing Security & Audit workspace remains the authority for token revocation and read-only audit evidence.

## Security boundary

The navigation layer grants no new permission and performs no privileged mutation. Existing same-origin APIs, request IDs, server-side RBAC, separation of duties, write-only credential replacement, token-revocation authority and audit persistence remain unchanged. UI visibility is not authorization.

## Repository acceptance

The dedicated R2 gate must:

1. verify exact-head checkout;
2. build/typecheck the canonical frontend from the locked dependency graph;
3. verify the canonical `/administration` route renders `AdministrationConsole` rather than four unstructured sibling workspaces;
4. verify all six section-navigation entries and canonical targets are present;
5. verify navigation text preserves the server-authority boundary.

A green gate is repository engineering evidence only. It does not prove owner usability acceptance, production-equivalent operation, penetration-test results, independent assurance or production authorization.

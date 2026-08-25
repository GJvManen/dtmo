# Phase 11.10q — Canonical Administration Identity & RBAC Recovery

This bounded recovery slice moves managed identity and RBAC administration into the canonical React Administration workspace. It reuses the existing same-origin DTMO server contracts rather than duplicating authorization policy in the browser.

The workspace now reads the immutable role catalogue, managed principals and the server-side role/separation-of-duties matrix. Authorized human administrators with `manage:users` can create managed principals and submit governed assignment changes with an explicit reason. The server remains authoritative for eligible principal types, self-management blocking, last-admin protection and persistent audit recording.

Externally issued bearer tokens are not rewritten by the browser or by a role-assignment mutation. The UI surfaces the existing token reissue / identity-provider reconciliation boundary after assignment changes. Integration credentials remain server-side and are never returned to the browser.

This slice removes a legacy-only administration dependency, but it does not constitute owner functional acceptance. `docs/roadmap/FUNCTIONAL_RECOVERY_ACCEPTANCE.md` remains authoritative and PR #316 stays draft until the owner completes the required canonical functional retest.

# DTMO Current Project State

Last reconciled: 2026-08-11 — RC10.5 / PR #120 is accepted and merged as `df138ebbdde1fa0f30f4003e1a158b3419a3d3fe`; PR #121 RC10.6 is under exact-head CI revalidation after RUN-187 bounded startup remediation.

## Executive status

- Phases 1–7 repository-controlled internal gates: accepted within documented claim boundaries.
- RC10.1 Operations Workspace: `PASS`.
- RC10.2 unified operational dashboards: `PASS`.
- RC10.3 Threat Intelligence Workspace: `PASS`.
- RC10.4 Source Center refinement: `PASS`.
- RC10.5 Administration Consolidation: `PASS`.
- RC10.6 UX polish: `CI_VALIDATION_PENDING`.
- Phase 8 staging acceptance: `BLOCKED_EXTERNAL` for approved real deployment-parity evidence.
- Phase 9 external assurance: `NOT COMPLETE`.
- Phase 10 production go/no-go: `NOT STARTED`.

DTMO is **not production ready**.

## RUN-187 / RC10.6

Exact PR #121 head `c81f9d77a7e91e0706a1c96fd417a1c454cebf3b` failed the workflow matrix and is not accepted. The first inspected concrete failure was application startup: `/metrics` referenced nonexistent `Permission.READ_METRICS`, causing FastAPI import to abort before browser gates could execute.

The bounded remediation restores `backend/dtmo/main.py` to accepted RC10.5 health, connectors and metrics behavior while retaining only the intended RC10.6 preferences-router import and mount. The GET-only `/ui/preferences` remains browser-local presentation state and introduces no server-side preference mutation API.

This remediation does not alter server-side RBAC, separation of duties, privacy, provenance, auditability, human review or separate external share approval. Acceptance still requires full success of every registered workflow on one later exact PR head.

## External blockers

No approved real staging endpoint/environment identity and no complete ten-class deployment-parity package tied to one immutable release are available. Genuine assistive-technology execution, independent penetration testing and remaining external assurance also remain absent.

## Exactly one current priority

Complete full exact-head CI validation for the remediated PR #121 head. Merge only on complete success; otherwise remediate only the first concrete failing root cause.

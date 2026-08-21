# Phase 11.10k Automation & Playbooks Gate

## Acceptance scope

Phase 11.10k is repository-complete only when the canonical `/automation` workspace is wired to the DTMO-owned scheduler/connector control plane and its exact-head contract plus Chromium acceptance are green together with every other workflow registered for that unchanged PR head.

The dedicated gate must verify:

- `/automation` renders the Automation & Playbooks workspace rather than the generic shell foundation;
- scheduler observation comes from `/health` and connector/playbook capability from `/connectors`;
- explicit execution uses the existing server-owned `/connectors/{id}/run` path with a request identifier;
- the browser contains no upstream credential values or direct upstream-service calls;
- human execution visibility requires `manage:connectors` and does not present service-account sessions as human authority;
- missing canonical state fails closed;
- source truth, compromise, containment, remediation, review, case, share/publication and production authority are never inferred from scheduler or execution success;
- documentation remains synchronized with the active Phase 11 lifecycle.

## Evidence boundary

The workflow records repository-controlled exact-head evidence only. It must not claim live connector health, production scheduler operation, production-equivalent validation, remediation success, external assurance or production authorization. Phase 10 remains **NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED**.

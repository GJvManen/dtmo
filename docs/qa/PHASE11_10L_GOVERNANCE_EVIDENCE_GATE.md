# Phase 11.10l Governance & Evidence Gate

Acceptance requires the canonical `/workbench/governance` route to render repository-backed governance knowledge exclusively through DTMO-owned APIs, with deterministic contract and browser coverage on the unchanged exact PR head.

Required evidence:

- `GET /api/v1/governance/knowledge` remains RBAC-protected and fail-closed;
- Normenkader IBP and MITRE ATT&CK are not presented as mapped unless explicit governed crosswalk evidence exists;
- CVSS remains context-only unless a first-class governed mapping exists;
- repository-backed DTMO mappings show provenance and source sections;
- governance visibility does not grant review, case, remediation, connector, sharing, publication or production authority;
- missing/stale/inaccessible evidence is never converted into PASS or compliance;
- deterministic repository contracts and Chromium browser acceptance succeed;
- Professional Documentation Gate and every registered workflow for the final exact head are `completed/success`.

Repository CI is repository-controlled exact-head evidence only. It is not production-equivalent validation or external assurance. Phase 10 remains **NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED**.

# Phase 11.10l Governance & Evidence Acceptance Gate

Status: **IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED**

## Acceptance scope

Phase 11.10l is accepted only when the canonical `/workbench/governance` workspace is wired to `GovernanceWorkspace`, reads governance state exclusively through DTMO-owned APIs, and every registered workflow for the unchanged final PR head completes successfully.

The bounded gate verifies:

- `GET /api/v1/governance/knowledge` remains the canonical browser-facing governance source;
- server-side `read:intelligence` authorization remains authoritative;
- Normenkader IBP and MITRE ATT&CK are not represented as mapped without explicit repository-backed crosswalks;
- CVSS remains context-only where no first-class mapping exists;
- repository-backed internal mappings retain source/provenance references;
- missing or inaccessible governance state fails closed and is not converted into compliance, assurance or zero-risk claims;
- governance visibility grants no review, external-share, publication or production authority;
- browser acceptance exercises the canonical application-shell route rather than a parallel test UI.

## Exact-head evidence rule

The dedicated **Phase 11 Governance Evidence Workspace Gate** provides **repository-controlled exact-head evidence only**. Its contract/browser fixtures do not establish live compliance, certification, independent external assurance, production-equivalent operation or production authorization. Any new commit invalidates all prior workflow evidence and requires a complete new exact-head cycle.

Phase 10 remains **NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED**. Phase 11.10p production-equivalent validation, Phase 11.11 independent external assurance and Phase 12 formal production GO/NO-GO remain later gates.

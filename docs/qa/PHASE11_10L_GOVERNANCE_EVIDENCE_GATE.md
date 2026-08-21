# Phase 11.10l Governance & Evidence Acceptance Gate

Status: **IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED**

## Acceptance scope

Phase 11.10l is accepted only when the canonical `/workbench/governance` workspace is wired to `GovernanceWorkspace`, reads governance state exclusively through DTMO-owned APIs, and every registered workflow for the unchanged final PR head completes successfully.

The bounded gate verifies:

- `GET /api/v1/governance/knowledge` remains the canonical browser-facing governance source;
- server-side `read:intelligence` authorization remains authoritative;
- the API reuses the explicit repository-backed crosswalk in `backend/dtmo/governance_crosswalk.py` and `docs/governance/GOVERNANCE_MAPPING_REGISTRY.md`;
- Normenkader IBP, MITRE ATT&CK and NIST CSF are represented only through explicit typed relationships already present in that crosswalk;
- the crosswalk remains explicitly **partial** and unrecorded controls/techniques/categories are not inferred;
- CVSS remains `context-only` scoring semantics and is not converted into a compliance or local-exposure claim;
- repository-backed internal mappings retain source/provenance references;
- missing or inaccessible governance state fails closed and is not converted into compliance, assurance or zero-risk claims;
- a mapping never becomes certification, blanket compliance, semantic equivalence, proof of environment effectiveness or audit acceptance;
- governance visibility grants no review, case, remediation, connector, external-share, publication, administration or production authority;
- browser acceptance exercises the canonical application-shell route rather than a parallel test UI;
- deterministic repository contracts, frontend build and Chromium browser acceptance succeed.

## Exact-head evidence rule

The dedicated **Phase 11 Governance Evidence Workspace Gate** provides **repository-controlled exact-head evidence only**. Its contract/browser fixtures do not establish live compliance, certification, accountable owner acceptance, independent external assurance, production-equivalent operation or production authorization. Any new commit invalidates all prior workflow evidence and requires a complete new exact-head cycle.

Acceptance additionally requires Professional Documentation Gate and **every workflow registered for the exact final head** to be `completed/success`; queued, in-progress, failed, cancelled, skipped, stale or missing evidence is not PASS. The PR must be mergeable and ready for review, and squash merge must use expected-head protection.

Phase 10 remains **NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED**. Phase 11.10p production-equivalent validation, Phase 11.11 independent external assurance and Phase 12 formal production GO/NO-GO remain later gates.

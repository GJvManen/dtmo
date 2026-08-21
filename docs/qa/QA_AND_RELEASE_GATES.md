# DTMO QA and Release Gates

## Purpose

DTMO separates repository engineering evidence, accountable functional acceptance, production-equivalent validation, independent assurance and formal production authorization. The release model is fail-closed: configured checks, mock data, design artifacts or documented intent are never promoted to evidence they do not establish.

## Core release principles

1. **Exact-head evidence** — PR evidence belongs only to the exact final PR head.
2. **New commit, new evidence** — any new commit invalidates earlier exact-head acceptance evidence.
3. **No inferred PASS** — queued, in-progress, skipped, cancelled, failed, stale, missing or inaccessible evidence is not `PASS`.
4. **Expected-head merge protection** — merge must reject a moved head.
5. **Evidence classes remain separate** — CI, owner acceptance, real-environment validation, external assurance and production authorization are not interchangeable.
6. **Historical evidence is immutable** — later lifecycle changes do not rewrite prior candidate evidence.
7. **One bounded objective per PR** — the next slice does not start before the current slice is green and merged.
8. **Professional documentation is a merge criterion** — affected authoritative documentation and tests must be current on the exact head.
9. **External evidence remains external** — fixtures, emulators, screenshots and CI artifacts do not prove production-equivalent operation.
10. **UI convenience is not authority** — role-aware visibility never replaces server-side RBAC or required human approval.

## Current acceptance status

| Stage | Status |
|---|---|
| Phases 1–7 | `PASS` |
| RC13 | `PASS / OWNER_ACCEPTED` |
| E8.1–E8.10 | `PASS / REPOSITORY_COMPLETE` |
| Phase 8 | `PASS / OWNER_ACCEPTED — HISTORICAL CANDIDATE` |
| Phase 9 | `PASS / EXTERNAL_ASSURANCE_ACCEPTED — HISTORICAL CANDIDATE` |
| Phase 10 | `NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED` |
| Phase 11 | `IN PROGRESS / ACTIVE` |
| Phase 11.1–11.9 | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.10 | `IN PROGRESS / FRESH CANDIDATE-BOUND EVIDENCE REQUIRED` |
| Phase 11.10a–11.10k | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.10l Governance & Evidence | `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED` |
| Phase 11.10m–11.10o | `NOT STARTED` |
| Phase 11.10p | `NOT STARTED / CANDIDATE FREEZE REQUIRED` |
| Phase 11.11 | `NOT STARTED` |
| Phase 12 | `NOT STARTED` |

DTMO is **not production authorized**.

## Gate families

| Gate family | Objective | Evidence boundary |
|---|---|---|
| Build & quality | Packaging, lint, typing, tests | Repository CI |
| Security & identity | Authentication, authorization, secrets, privileged actions | Repository CI + deployed assurance |
| Data integrity & recovery | Migration, persistence, integrity, recovery | Repository CI + deployed validation |
| Connector reliability | Contract/state/retry/timeout/replay/provenance/isolation | Repository CI + deployed validation |
| Governance | Explicit mapping truth, provenance and authority separation | Repository CI + governance review |
| Platform integration | Upstream API/model interoperability | Phase 11 repository evidence |
| Integrated runtime | Kubernetes/Helm/GitOps, identity, network, HA, recovery, observability, supply chain | Phase 11 repository + deployed evidence |
| Workbench 11.10a–11.10k | Accepted bounded functionality | Repository/browser evidence |
| Governance & Evidence | Explicit partial crosswalks, no inferred compliance, fail-closed evidence | Active Phase 11.10l repository/browser evidence |
| Candidate workspaces | Operations/Admin, role-aware UX/accessibility, consolidation | Phase 11.10m–11.10o repository/owner evidence |
| Production-equivalent validation | Same-candidate migration/upgrade/rollback/health/saturation/recovery | Phase 11.10p real-environment evidence |
| Independent assurance | Independent assessment of integrated candidate | Phase 11.11 |
| Production decision | Formal accountable GO/NO-GO | Phase 12 |

## Accepted Phase 11.10a–11.10k baseline

The accepted workbench sequence preserves **browser → DTMO API → governed integration adapter/data contract → governed service/evidence source**, server-side RBAC, provenance, replay protection, human review/share/publication authority and separate case authority. None of the accepted slices proves live upstream health, local compromise, independent assurance or production authorization.

## Active Phase 11.10l Governance & Evidence gate

Dedicated gate: `docs/qa/PHASE11_10L_GOVERNANCE_EVIDENCE_GATE.md`  
Workflow: `.github/workflows/phase11-governance-evidence.yml`

The final exact head must prove:

- `/workbench/governance` is wired to `GovernanceWorkspace` in the canonical application shell;
- the browser uses only the same-origin `GET /api/v1/governance/knowledge` DTMO API;
- server-side `read:intelligence` remains authoritative;
- the API reuses the explicit typed repository crosswalk in `backend/dtmo/governance_crosswalk.py` and the Governance Mapping Registry;
- Normenkader IBP, MITRE ATT&CK and NIST CSF mappings are surfaced only where explicit repository relationships exist;
- CVSS remains context-only scoring semantics;
- partial relationships are never rendered as certification, blanket compliance, semantic equivalence or environment effectiveness;
- unrecorded mappings and unavailable evidence fail closed rather than becoming PASS/compliant/healthy;
- governance visibility grants no review, case, remediation, connector, external-share, publication, administration or production authority;
- deterministic contract and Chromium browser tests succeed;
- frontend production build succeeds;
- Professional Documentation Gate and every other workflow registered for the final unchanged head are `completed/success`.

Repository CI for this gate is **repository-controlled exact-head evidence only**. It is not production-equivalent validation, owner acceptance, independent assurance or production authorization.

## Merge acceptance procedure

A bounded PR may be merged only when all of the following are true at the same final unchanged SHA:

1. every registered workflow is `completed/success`;
2. no queued, in-progress, skipped, cancelled, failed, stale or missing exact-head evidence remains;
3. the PR is mergeable and ready for review;
4. professional documentation and documentation-contract tests are synchronized;
5. the head has not moved since verification;
6. squash merge uses expected-head protection.

After accepted merge of 11.10l, exactly the next bounded priority is **11.10m Operations & Administration**.

## Later external gates

Phase 11.10p remains `NOT STARTED / CANDIDATE FREEZE REQUIRED` until 11.10a–11.10o are complete and one immutable candidate is frozen. Historical Phase 8/9 evidence cannot satisfy it. Phase 11.11 then requires fresh independent assurance for that same candidate. Phase 12 is the later formal accountable production GO/NO-GO.

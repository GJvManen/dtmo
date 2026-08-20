# DTMO Executive Status

Date: **2026-08-20**  
Software baseline: **16.0.0rc12 plus accepted post-RC13/E8/Phase-11 repository enhancements**

## Management summary

DTMO retains Phases 1–7 `PASS`, RC13 `PASS / OWNER_ACCEPTED`, E8.1–E8.10 `PASS / REPOSITORY_COMPLETE`, and historical Phase 8 `PASS / OWNER_ACCEPTED` plus Phase 9 `PASS / EXTERNAL_ASSURANCE_ACCEPTED` for their earlier candidate only. Phase 10 remains **`NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`**. DTMO is **not production authorized**.

Phase 11 is `IN PROGRESS / ACTIVE`. Phase 11.1–11.9 and Phase 11.10a–11.10e are `PASS / REPOSITORY_COMPLETE`. Phase 11.10 remains **`IN PROGRESS / FRESH CANDIDATE-BOUND EVIDENCE REQUIRED`**.

The current bounded priority is **Phase 11.10f OpenCTI graph/entity workspace**, status `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`. It makes Knowledge Graph functional through read-only DTMO APIs over persisted OpenCTI/STIX mapping evidence. Phase 11.10g, Phase 11.10p, Phase 11.11 and Phase 12 remain `NOT STARTED`.

## Decision position

| Decision area | Status | Consequence |
|---|---|---|
| Engineering baseline | `PASS` | Repository foundation accepted |
| Functional product | `PASS / OWNER_ACCEPTED` | Historical pre-workbench functional baseline accepted within scope |
| E8 product evolution | `PASS / REPOSITORY_COMPLETE` | Product-evolution baseline accepted |
| Phase 8 | `PASS / OWNER_ACCEPTED — HISTORICAL CANDIDATE` | Prior candidate only |
| Phase 9 | `PASS / EXTERNAL_ASSURANCE_ACCEPTED — HISTORICAL CANDIDATE` | Prior candidate only |
| Phase 10 | `NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED` | Production authorization not granted |
| Phase 11.1–11.9 | `PASS / REPOSITORY_COMPLETE` | Integrations/runtime/migration baseline accepted |
| Phase 11.10 | `IN PROGRESS / FRESH CANDIDATE-BOUND EVIDENCE REQUIRED` | Candidate completion + fresh real-environment validation required |
| Phase 11.10a | `PASS / REPOSITORY_COMPLETE` | Frontend architecture/design accepted |
| Phase 11.10b | `PASS / REPOSITORY_COMPLETE` | Canonical application shell accepted |
| Phase 11.10c | `PASS / REPOSITORY_COMPLETE` | Canonical Command Center accepted |
| Phase 11.10d | `PASS / REPOSITORY_COMPLETE` | Unified Intelligence Workspace accepted |
| Phase 11.10e | `PASS / REPOSITORY_COMPLETE` | Integrated IntelOwl/Cortex analysis accepted |
| Phase 11.10f | `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED` | OpenCTI graph/entity is the sole active bounded slice |
| Phase 11.10g | `NOT STARTED` | Blocked until 11.10f acceptance/merge |
| Phase 11.10p | `NOT STARTED / CANDIDATE FREEZE REQUIRED` | External validation deferred until candidate completion |
| Phase 11.11 | `NOT STARTED` | Blocked until 11.10 owner acceptance |
| Phase 12 | `NOT STARTED` | Formal production decision not started |

## Active Phase 11.10f objective

The Knowledge Graph workspace must provide attributable OpenCTI/STIX context without synthetic or overclaimed topology:

- `/workbench/intelligence/graph` as the canonical graph/entity route;
- one canonical DTMO intelligence object as graph root;
- persisted OpenCTI mappings as graph/entity nodes;
- only proven `canonical-mapping` edges;
- stable OpenCTI/STIX identity, markings, confidence, external references, provenance and immutable revisions in entity detail;
- `read:intelligence` as the server-side authority for all frontend-facing graph/entity reads;
- no browser-held OpenCTI credential or direct `/graphql` call;
- no OpenCTI mutation, connector invocation, MISP synchronization, TheHive case creation or publication/share action;
- empty mapping evidence distinguished from upstream absence;
- dependency failures shown unavailable rather than as an empty graph.

The accepted persistence boundary does not durably store generic OpenCTI entity-to-entity relationship topology. Missing topology evidence must **fail closed** and must not be inferred from graph proximity or object coexistence.

OpenCTI graph/entity presence, confidence or markings do **not prove** local exposure, exploitability, compromise, attribution certainty or remediation state. Existing persistence constraints keep external sharing unauthorized and local compromise unproven. **Server-side RBAC** and human-governance boundaries remain authoritative.

## Candidate-completion sequence

11.10a architecture/design, 11.10b shell, 11.10c Command Center, 11.10d Unified Intelligence and 11.10e Integrated Analysis are accepted. 11.10f is active. The fixed next sequence remains 11.10g MISP, 11.10h TheHive, 11.10i Vulnerability/Exposure, 11.10j Sources/Collection, 11.10k Automation, 11.10l Governance/Evidence, 11.10m Operations/Admin, 11.10n role-aware UX/accessibility and 11.10o consolidation/full functional acceptance.

Only after 11.10o is one immutable integrated candidate frozen for 11.10p.

## 11.10p external evidence boundary

11.10p requires fresh candidate identity, migration/compatibility, upgrade, exact prior-digest rollback plus post-rollback health, health/readiness, representative saturation/capacity and recovery/continuity evidence for the **same immutable** candidate and environment.

Historical Phase 8/9 evidence cannot satisfy this gate. Missing, placeholder, inaccessible, historical-only or mixed-candidate evidence must **fail closed**. Application rollback does not authorize automatic database down migration.

Repository CI validates architecture, implementation and evidence contracts only. It **does not prove** live OpenCTI connectivity/health or upstream completeness, production-equivalent execution, independent assurance or production authorization.

## Executive recommendation

Complete only **Phase 11.10f OpenCTI graph/entity workspace** until its final exact head is fully green and professionally documented. Merge with expected-head protection. Only then begin **11.10g MISP Sharing & Exchange**. Do not execute 11.10p or start Phase 11.11 until the integrated workbench candidate is complete, frozen and ready for fresh external validation.

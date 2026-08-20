# DTMO Executive Decision View

## Purpose

This document gives accountable decision makers the current production-readiness position and the evidence required before the programme may advance.

## Current position

| Decision area | Current state | Decision consequence |
|---|---|---|
| Repository-controlled engineering | Phases 1–7 `PASS` | Engineering foundation accepted |
| Functional product | RC13 `PASS / OWNER_ACCEPTED` | Accepted pre-workbench functional baseline |
| E8 product line | `PASS / REPOSITORY_COMPLETE` | Product-evolution baseline accepted |
| Phase 8 staging | `PASS / OWNER_ACCEPTED — HISTORICAL CANDIDATE` | Prior-candidate evidence only |
| Phase 9 assurance | `PASS / EXTERNAL_ASSURANCE_ACCEPTED — HISTORICAL CANDIDATE` | Prior-candidate assurance only |
| Phase 10 authorization | `NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED` | No production GO |
| Phase 11.1–11.9 | `PASS / REPOSITORY_COMPLETE` | Integration/runtime/migration baseline accepted |
| Phase 11.10 | `IN PROGRESS / FRESH CANDIDATE-BOUND EVIDENCE REQUIRED` | Candidate completion plus fresh external validation required |
| Phase 11.10a | `PASS / REPOSITORY_COMPLETE` | Frontend architecture/design accepted |
| Phase 11.10b | `PASS / REPOSITORY_COMPLETE` | Canonical application shell accepted |
| Phase 11.10c | `PASS / REPOSITORY_COMPLETE` | Canonical Command Center accepted |
| Phase 11.10d | `PASS / REPOSITORY_COMPLETE` | Unified Intelligence Workspace accepted |
| Phase 11.10e | `PASS / REPOSITORY_COMPLETE` | Integrated IntelOwl/Cortex analysis accepted |
| Phase 11.10f | `PASS / REPOSITORY_COMPLETE` | OpenCTI graph/entity workspace accepted |
| Phase 11.10g | `PASS / REPOSITORY_COMPLETE` | Human-governed MISP Sharing & Exchange accepted |
| Phase 11.10h | `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED` | TheHive Investigations & Cases is the sole active decision gate |
| Phase 11.10i | `NOT STARTED` | Vulnerability/Exposure blocked until 11.10h acceptance |
| Phase 11.10p | `NOT STARTED / CANDIDATE FREEZE REQUIRED` | External validation blocked until candidate completion/freeze |
| Phase 11.11 | `NOT STARTED` | Blocked until 11.10 acceptance |
| Phase 12 | `NOT STARTED` | Requires fresh validation and assurance |

Phase 11 remains `IN PROGRESS / ACTIVE`. DTMO is **not production authorized**.

## Active decision boundary

The immediate question is whether **Phase 11.10h TheHive Investigations & Cases** provides a trustworthy canonical investigation surface while preserving the existing explicit human case-handoff boundary and refusing to infer TheHive objects or outcomes that DTMO does not persist/read back.

The exact-head gate must prove:

- functional `/workbench/investigations` route inside the accepted canonical shell;
- canonical investigation-state reads protected by `read:intelligence`;
- existing case mutation remains protected by `handoff:case` and explicit human action;
- service accounts cannot authorize case handoff;
- canonical provenance is required before case mutation;
- the browser uses DTMO APIs only and receives no TheHive credential or organization authorization header;
- TLP/PAP mapping and authoritative handling restrictions fail closed;
- durable `reserved`, `delivered`, `ambiguous` and `failed` handoff state is attributable;
- `reserved` or `ambiguous` state requires manual reconciliation and blocks blind new UI case requests;
- stable case identity returned at creation is not promoted to upstream case completeness;
- alerts, tasks, case timeline, later case state and responders are not fabricated when the accepted persistence has no such readback evidence;
- feature/configuration state is not presented as live TheHive health;
- handoff presence is not presented as external-share authority, responder/remediation proof or local compromise;
- dependency failures are unavailable rather than synthesized into case/health conclusions;
- professional lifecycle/evidence/roadmap documentation is synchronized to the same exact head.

The canonical trust path remains **browser → DTMO API → governed integration adapter → upstream service**. `/ui/console`, `/ui/intelligence-workspace` and `/ui/misp-workspace` remain temporary **compatibility paths**.

## Candidate-completion decision chain

```mermaid
flowchart LR
    A[11.10a architecture accepted] --> B[11.10b shell accepted]
    B --> C[11.10c Command Center accepted]
    C --> D[11.10d Unified Intelligence accepted]
    D --> E[11.10e Integrated Analysis accepted]
    E --> F[11.10f OpenCTI Graph accepted]
    F --> G[11.10g MISP Sharing accepted]
    G --> H[11.10h TheHive active]
    H --> R[11.10i-o bounded completion]
    R --> Z[Immutable candidate freeze]
    Z --> P[11.10p fresh evidence]
    P --> O{Accountable owner review}
    O -->|PASS / OWNER_ACCEPTED| N[11.11 may start]
    O -->|otherwise| X[BLOCKED]
```

## Decision rules

- One bounded PR is active at a time; exact-head CI must be fully green before merge.
- Professional documentation is a merge criterion.
- Role-aware UI is not authorization; server-side enforcement remains authoritative.
- Human publication/share authority and TheHive case-handoff authority remain distinct.
- Review and share approval remain separate human decisions in the accepted MISP boundary.
- TheHive case handoff grants no external sharing or responder authority.
- Authoritative source handling restrictions cannot be weakened by the UI or case request.
- Enrichment, graph presence, correlation, MISP exchange or TheHive case presence does not establish local compromise.
- Taranis AI, IntelOwl, Cortex, OpenCTI, MISP and TheHive remain separate service/licensing boundaries.
- Design mockups, fixtures and browser mocks are not live or production-equivalent evidence.
- Historical Phase 8/9 evidence is preserved but cannot be reused as Phase 11.10/11.11 evidence.
- Repository CI **does not prove** production-equivalent operation.
- 11.10p evidence must bind to the **same immutable** candidate and environment.
- Rollback must restore the exact prior immutable digest and include post-rollback health.
- Application rollback does not authorize automatic database down migration.
- Missing, placeholder, inaccessible, historical-only or mixed-candidate evidence must **fail closed**.

## Current decision

**Phase 10 remains `NO-GO / BLOCKED`. Phase 11.1–11.9 and 11.10a–11.10g are `PASS / REPOSITORY_COMPLETE`. Phase 11.10 is `IN PROGRESS / FRESH CANDIDATE-BOUND EVIDENCE REQUIRED`; 11.10h is the active bounded TheHive Investigations & Cases gate. 11.10i, Phase 11.11 and Phase 12 are `NOT STARTED`. DTMO remains not production authorized.**

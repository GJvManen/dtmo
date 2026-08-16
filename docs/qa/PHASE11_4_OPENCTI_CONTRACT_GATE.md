# Phase 11.4 OpenCTI Contract Gate

Status: **EXACT-HEAD VALIDATION REQUIRED**  
Last updated: **2026-08-16**

## Objective

Accept the bounded OpenCTI service/API/data-model/identity/security/licensing contract before any adapter implementation begins.

## Required repository evidence

The exact final PR head must prove that:

- OpenCTI 7.260811.0 is recorded as the reviewed compatibility baseline;
- Community Edition Apache-2.0 and separate Enterprise Edition licensing are distinguished;
- DTMO uses a separate service/API boundary and vendors no OpenCTI source;
- GraphQL, STIX 2.1, TAXII 2.1 and stream interfaces are bounded and described;
- the initial implementation is read-oriented and excludes automatic connector/MISP/case/publication side effects;
- OpenCTI/STIX and DTMO canonical identities remain separate and explicitly mapped;
- markings/TLP/PAP, confidence and provenance are preserved;
- least-privilege non-human identity and runtime-secret handling are mandatory;
- bypass/admin authority is not required for routine integration;
- unknown/malformed marking or STIX semantics fail closed;
- pagination/stream replay must be durable, restart-safe and idempotent before repository completion;
- OpenCTI graph data cannot grant DTMO publication/share authority or prove local compromise;
- Phase 11.3 is reconciled as `PASS / REPOSITORY_COMPLETE` and 11.4 is the active bounded priority;
- README, docs portal, current state, roadmap, security overview, operations, QA and evidence index remain synchronized;
- Professional Documentation Gate and all required exact-head CI complete successfully.

## Non-evidence

A green repository gate does not prove live OpenCTI connectivity, deployed credentials, effective production RBAC/marking configuration, real STIX interoperability, graph quality/performance, privacy approval, HA/recovery, independent assurance or production authorization.

Historical Phase 8/9 evidence remains candidate-bound and is not reused for the materially changed Phase 11 integrated candidate.

## Next step

After protected merge of a fully green exact head, begin one bounded PR for the read-only OpenCTI STIX/identity adapter with pagination/reconciliation and provenance preservation. Phase 11.5 MISP consolidation remains blocked.
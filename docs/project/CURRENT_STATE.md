# DTMO Current Project State

Last reconciled: 2026-08-09 — RUN-20260809-126

This document is the human-readable current-state view of DTMO. It complements the immutable run history in `docs/development/runs/`, the chronological `docs/development/RUN_LOG.md`, the production roadmap, QA gate records and GitHub issues #1–#3.

## Executive status

- Phase 1 — CI and workflow integrity: `PASS`.
- Phase 2 — application security and identity: `PASS` for internal roadmap gates.
- Phase 3 — data integrity and recovery: `PASS` for internal roadmap gates.
- Phase 4 — connector reliability and provenance: `PASS` for internal roadmap gates.
- Phase 5 — performance and scalability: `PASS` for internal roadmap gates. External representative production load/stress remains separate in issue #1.
- Phase 6 — frontend accessibility and operational UX: `BLOCKED_EXTERNAL` only for genuine VoiceOver/NVDA behavior on supported real host/browser/screen-reader combinations. Browser/DOM automation is not accepted as a substitute.
- Phase 7 — observability and incident operations: `IN PROGRESS`.
  - RC10.1 request observability: `PASS`.
  - RC10.2 controlled connector-failure alerting: `PASS`.
  - RC10.3 queue-backlog alerting: next bounded implementation objective after RUN-126 documentation acceptance.
- Phase 8 — staging acceptance: `NOT STARTED`.
- Phase 9 — external assurance: `NOT COMPLETE`.
- Phase 10 — production go/no-go: `NOT STARTED`.

DTMO is therefore **not production ready**. Issue #1 remains the source of truth for external production-acceptance gates.

## Roadmap graph

```mermaid
flowchart LR
    P1[Phase 1 CI/workflow integrity\nPASS] --> P2[Phase 2 Security & identity\nPASS internal]
    P2 --> P3[Phase 3 Data integrity & recovery\nPASS internal]
    P3 --> P4[Phase 4 Connector reliability & provenance\nPASS internal]
    P4 --> P5[Phase 5 Performance & scalability\nPASS internal]
    P5 --> P6[Phase 6 Accessibility & operational UX\nBLOCKED_EXTERNAL]
    P6 --> P7[Phase 7 Observability & incident operations\nIN PROGRESS]
    P7 --> P8[Phase 8 Staging acceptance\nNOT STARTED]
    P8 --> P9[Phase 9 External assurance\nNOT COMPLETE]
    P9 --> P10[Phase 10 Production go/no-go\nNOT STARTED]
```

Phase 7 work may proceed while Phase 6 remains externally blocked; the VoiceOver/NVDA requirement itself remains open and is not bypassed.

## Runtime and governance dataflow

```mermaid
flowchart TD
    SRC[Approved intelligence sources] --> CONN[Governed connectors]
    CONN --> NORM[Normalization + provenance]
    NORM --> Q{Valid / unique / fresh?}
    Q -- no --> QUAR[Quarantine\npublish_approved=false]
    Q -- yes --> CAND[Candidate intelligence\npublish_approved=false]
    CAND --> PG[(PostgreSQL)]
    CAND --> OBJ[(MinIO raw evidence)]
    CAND --> OS[(OpenSearch)]
    CAND --> KG[Knowledge graph / correlation]
    CAND --> REVIEW[Human review]
    REVIEW --> APPROVE[Separate human share approval]
    APPROVE --> PUB[Approved publication/export]
    QUAR --> HREC[Named human recovery review]
    HREC --> CAND
```

## CI and evidence model

```mermaid
flowchart TB
    PR[Pull request exact head] --> QG[RC4 Quality Gate]
    PR --> REC[RC6 Recovery gates]
    PR --> CON[RC7 Connector gates]
    PR --> PERF[RC8 Performance gates]
    PR --> UX[RC9 Browser/accessibility gates]
    PR --> OBS[RC10 Observability gates]

    QG --> ACCEPT{All registered exact-head gates green?}
    REC --> ACCEPT
    CON --> ACCEPT
    PERF --> ACCEPT
    UX --> ACCEPT
    OBS --> ACCEPT

    ACCEPT -- no --> BLOCK[BLOCKED / CI_VALIDATION_PENDING]
    ACCEPT -- yes --> ART[Inspect retained artifacts]
    ART --> MERGE[Expected-head protected merge]
```

Configured or queued workflows are not evidence of success. The accepted state requires completed exact-head CI, retained evidence where specified, independent inspection and the actual protected merge.

## Latest accepted Phase 7 evidence

### RC10.1 — request observability

PR #80 exact head `01a175e12da7c8af8566178a2d7e6b34a57d58bc` passed all 34 registered workflows. Retained artifact `9040196394`, digest `sha256:6792020994d94b0484cb84140d202433303eceb82565f8598ffd5937940531d6`, independently proved:

- validated/safe correlation IDs;
- correlation ID and method in real `structlog` request context;
- structured request completion/failure events;
- bounded route-template Prometheus request metrics;
- request latency metrics;
- in-flight request metric;
- JUnit 5 tests, 0 failures/errors/skips.

PR #80 merged as `1675d88bb24dcd50e20545f49b26dd7cc2810d97`.

### RC10.2 — controlled connector-failure alerting

PR #82 exact head `b38aeae44588e39e35339f4c4d9667947804b243` passed all 35 registered workflows. Retained artifact `9040485255`, digest `sha256:96883158cfd790c3c6b21c2db819acbcbc03d431d4dd79bb32038b6ff258de25`, independently proved:

- terminal connector failure sets an active bounded alert signal;
- Prometheus alert metric and `DTMOConnectorFailure` rule;
- structured safe correlation evidence;
- actionable operator guidance;
- raw connector error text excluded from alert logs;
- repeated failure does not create another raise transition while already active;
- subsequent success clears the signal and emits clear evidence;
- publication approval remains unchanged;
- JUnit 4 tests, 0 failures/errors/skips.

PR #82 merged as `f6680423860389288d9feced34592294d774bf4a`.

RC10.2 does not claim pager/e-mail/chat notification delivery, queue/storage/API/search alerting, dashboards, runbooks or Phase-7 completion.

## Phase 6 external accessibility boundary

RC9.1–RC9.15 contain accepted bounded browser/accessibility evidence, including keyboard navigation, supported browsers, contrast, text resize, 320px reflow, text spacing and complete focus-order evidence. RC9.16 defines the remaining real-assistive-technology evidence contract.

Phase 6 remains `BLOCKED_EXTERNAL` until genuine VoiceOver and NVDA execution is retained from supported real host/browser/screen-reader combinations. Browser/DOM automation is not accepted as a substitute.

## Phase 5 capacity boundary

Internal Phase 5 is `PASS`, including capacity/scaling guidance. All performance figures are bounded internal/synthetic evidence and do not certify production capacity. Issue #1's independent representative production load/stress gate remains separate and open.

## External gates still open

Issue #1 remains authoritative for externally executed production gates, including independent penetration testing, representative load/stress, full backup/restoration exercise, production OpenSearch hardening, secrets-manager replacement where required, staging/production deployment acceptance and operational/stakeholder approval.

## Security and governance invariants

- RBAC remains enforced.
- Review and share approval remain separate human actions.
- The same principal may not review and share-approve the same item.
- Connectors and service accounts cannot approve publication.
- Ingestion, replay, retry, recovery, timeout, performance or observability success never implies publication approval.
- Provenance, confidence and raw evidence remain retained according to their controls.
- Performance and controlled-failure fixtures use synthetic or explicitly approved non-production data.
- Missing, queued, cancelled, failed or unexecuted CI is never `PASS`.

## Exactly one current priority

Complete RUN-20260809-126 documentation reconciliation through exact-head CI and protected merge. After that, implement Phase 7 / RC10.3: a bounded queue-backlog alerting gate with explicit threshold semantics, actionable correlated evidence and controlled breach/recovery behavior. Storage-integrity, API-error and search-health alerting remain later Phase-7 objectives.

# RC10.4 Storage Integrity Alerting Gate

## Decision

`PASS`

RC10.4 implements exactly one bounded Phase 7 objective: observe the existing immutable raw-evidence integrity verifier and raise a critical operational signal when checksum/size verification fails, without exposing object identity, digest or payload data.

## Accepted exact-head evidence

PR #86 exact head `8aa56dacd64583de5e96c0fda188ba954437ffda` completed all 37 registered workflows successfully.

Dedicated workflow run `31325197952` completed both `storage-integrity-alerting` and fail-closed `storage-integrity-alerting-gate` successfully.

Retained artifact `9041327884`, digest `sha256:456b09902727552d62fa7e1c96f119c6050a692d2519e0f8cecdd160e8b1dab3`, was independently inspected and exact-head bound. JUnit/pytest recorded 5 tests, 0 failures, 0 errors and 0 skips.

Evidence confirms:

- `IntelligenceLake.verify()` remains the size/SHA-256 integrity source of truth;
- the alert observer consumes only bounded storage name plus boolean verification result;
- integrity check, active-alert and transition Prometheus metrics are present;
- critical rule `DTMOStorageIntegrityFailure` is defined;
- structured raise/active/clear events retain safe correlation evidence and actionable guidance;
- raw object keys, expected digest, original payload and tampered payload are absent from alert evidence;
- repeated failures suppress duplicate raise transitions;
- a later successful re-verification clears the alert;
- the observer does not mutate storage or approve publication;
- no production data was used.

PR #86 was squash-merged with expected-head protection as `4d7494e8b8fcdcddb73349bf87157d8c16763c33`.

## Existing controls preserved

`IntelligenceLake.land()` and `IntelligenceLake.verify()` remain authoritative for immutable raw-evidence receipts and size/SHA-256 verification. RC10.4 does not change storage write, restore, verification, RBAC, separation of duties, provenance, auditability or human share approval.

## Claim boundary

RC10.4 does **not** claim:

- scheduled or fleet-wide production integrity scanning is configured or accepted;
- pager/e-mail/chat notification delivery is configured or accepted;
- API-error alerting is complete;
- search-health alerting is complete;
- dashboards, runbooks or on-call handover are complete;
- Phase 7 is complete;
- Phase 6's genuine VoiceOver/NVDA external gate is closed.

## Runtime security/lifecycle blocker — RUN-20260809-131

The separate runtime gate is `BLOCKED_EXTERNAL`. The repository still pins `minio/minio:RELEASE.2025-07-23T15-54-02Z`, which remains inside documented affected-version ranges identified in the fresh advisory review. Upstream MinIO is now archived and explicitly no longer maintained; legacy binary/container releases are historical and unmaintained.

This lifecycle finding does not invalidate RC10.4's bounded behavioral evidence, but it prevents treating the current object-storage runtime as production-ready. A patched community source build would not, by itself, satisfy the supported-runtime gate. No unsupported replacement was made.

Affected-version and upstream-maintenance-status confidence are high. Suitability of a successor for DTMO is not yet evidenced and is not claimed.

## Exactly one next priority

Obtain and record an explicit supported object-storage target for DTMO, including its supported product/image or deployment method, lifecycle/support source, and required entitlement/credential boundary. Then perform one bounded migration implementation and rerun security, recovery, storage-integrity and full regression gates before resuming RC10.5 API-error alerting.

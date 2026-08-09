# RC10.4 Storage Integrity Alerting Gate

## Decision

`CI_VALIDATION_PENDING`

RC10.4 implements exactly one bounded Phase 7 objective: observe the existing immutable raw-evidence integrity verifier and raise a critical operational signal when checksum/size verification fails, without exposing object identity, digest or payload data.

## Scope

- reuse `IntelligenceLake.verify()` as the source of truth for raw-object size and SHA-256 integrity;
- the alert observer consumes only a bounded storage name plus the boolean verification result;
- expose bounded integrity check, active-alert and transition Prometheus metrics;
- define critical Prometheus rule `DTMOStorageIntegrityFailure`;
- emit structured `storage_integrity_alert_raised`, `storage_integrity_alert_active` and `storage_integrity_alert_cleared` events with safe correlation evidence;
- never include raw object keys, SHA-256 receipts, payload bytes or payload text in alert labels/logs;
- suppress duplicate raise transitions while the alert is already active;
- clear only after a subsequent successful integrity verification;
- controlled tamper/recovery tests use the real `IntelligenceLake.verify()` implementation;
- retain exact-head JSON, JUnit and pytest evidence as `storage-integrity-alerting-evidence`.

## Existing controls preserved

`IntelligenceLake.land()` and `IntelligenceLake.verify()` remain authoritative for immutable raw-evidence receipts and size/SHA-256 verification. RC10.4 does not change how storage is written, restored or verified; the observer only receives the verification outcome.

## Gate

`PASS` requires every registered workflow on the exact final pull-request head to complete successfully and retained `storage-integrity-alerting-evidence` to be independently inspected. Missing, queued, cancelled, failed or unexecuted CI is never `PASS`.

## Claim boundary

RC10.4 does **not** claim:

- scheduled or fleet-wide production integrity scanning is configured or accepted;
- pager/e-mail/chat notification delivery is configured or accepted;
- API-error alerting is complete;
- search-health alerting is complete;
- dashboards, runbooks or on-call handover are complete;
- Phase 7 is complete;
- Phase 6's genuine VoiceOver/NVDA external gate is closed.

## Governance

No production credentials or production data are required. The observer does not mutate storage or approve publication. RBAC, separation of duties, privacy, provenance, persistent auditability and separate human share approval remain unchanged.

## Exactly one next priority

Inspect every registered workflow on the final RC10.4 pull-request head and independently inspect retained `storage-integrity-alerting-evidence`; repair only the first deterministic failure, or accept/merge only after complete successful evidence.

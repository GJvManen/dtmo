# DTMO Continuous Development Run Log

This file is the chronological audit record for continuous development runs. Detailed run records are stored under `docs/development/runs/`.

## Runs

- [RUN-20260809-125 — RC10.2 controlled connector-failure alerting](runs/RUN-20260809-125.md) — `CI_VALIDATION_PENDING`: added bounded terminal connector-failure metrics, structured correlated alert transitions, repeat-raise suppression, successful-run clear behavior, an actionable Prometheus alert rule, controlled regression tests and a dedicated retained exact-head alerting gate. Existing RC7 retry/backoff and failure isolation remain authoritative.
- [RUN-20260809-124 — RC10.1 exact-head acceptance and documentation reconciliation](runs/RUN-20260809-124.md) — `PASS`: PR #80 exact head `01a175e12da7c8af8566178a2d7e6b34a57d58bc` passed all 34 registered workflows; retained artifact `9040196394` (`sha256:6792020994d94b0484cb84140d202433303eceb82565f8598ffd5937940531d6`) independently proved the bounded request-observability controls with 5/5 JUnit tests passing; merged as `1675d88bb24dcd50e20545f49b26dd7cc2810d97`. Historical RC9.3–RC9.5 acceptance records were reconciled into the authoritative documentation set.
- [RUN-20260809-123 — RC10.1 request observability baseline](runs/RUN-20260809-123.md) — `PASS`: implementation run later accepted by RUN-124; added safe correlation-ID handling, real structlog context binding, structured request completion/failure events, bounded route-template Prometheus request metrics, an in-flight gauge, regression tests and a retained exact-head observability gate.
- [RUN-20260809-122 — RC9.16 genuine assistive-technology behavior](runs/RUN-20260809-122.md) — `BLOCKED_EXTERNAL`: real VoiceOver and NVDA behavior cannot be truthfully executed in the current automation environment. Defined the required macOS/Safari/VoiceOver and Windows/Firefox-or-Chrome/NVDA evidence matrix, criterion-level observations, privacy-safe retained evidence contract, RBAC checks and separate human share-approval verification.
- [RUN-20260809-121 — RC9.15 complete focus-order evidence](runs/RUN-20260809-121.md) — `PASS`: PR #78 final exact head `d2480293f605e8701fb677071c206cc25da97098` passed all 33 registered workflows; retained artifact `9039862032` (`sha256:09f1f756d0ddddb6d381f0a724938ec3408c8692be0dd61727b36be0dd29fed4`) independently proved complete bounded SC 2.4.3 focus order across all four critical surfaces; merged as `17a43175d6beda4fdf0156f701844d2c25ea4aec`.
- [RUN-20260809-120 — RC9.14 exact-head acceptance](runs/RUN-20260809-120.md) — `PASS`: PR #76 exact head `de52730b9b5165f7815e2c6c19c803413bbfcc60` passed all 32 registered workflows; retained artifact `9039432903` (`sha256:f547bd306bb9c63e02d049dda24d52d962086388f777f8857921cc818e75c5f1`) independently proved bounded WCAG 2.2 SC 1.4.12 text-spacing behavior; merged as `7d4816658159fac3b2b773fa6151b6274b510351`.
- [RUN-20260809-119 — RC9.14 WCAG 2.2 text-spacing evidence](runs/RUN-20260809-119.md) — implementation run later accepted by RUN-120.
- [RUN-20260809-118 — RC9.13 exact-head acceptance](runs/RUN-20260809-118.md) — `PASS`: bounded SC 1.4.10 reflow accepted for PR #74.
- [RUN-20260809-116 — RC9.12 exact-head acceptance](runs/RUN-20260809-116.md) — `PASS`: bounded SC 1.4.4 200% text resize accepted for PR #72.
- [RUN-20260809-114 — RC9.11 exact-head acceptance](runs/RUN-20260809-114.md) — `PASS`: bounded text/UI/focus contrast accepted for PR #70.
- [RUN-20260809-112 — RC9.10 exact-head acceptance](runs/RUN-20260809-112.md) — `PASS`: A11Y-001 session-status remediation accepted for PR #68.
- [RUN-20260809-110 — RC9.9 manual/non-automatable WCAG 2.2 AA critical-journey review](runs/RUN-20260809-110.md) — `BLOCKED`: automated/manual gaps have progressively closed; genuine VoiceOver/NVDA behavior remains the remaining Phase 6 accessibility evidence gap.
- [RUN-20260809-103 — RC9.5 exact-head acceptance](runs/RUN-20260809-103.md) — `PASS`: PR #59 exact head `cbd3dfc973a6daf06347e3ba4df2b5415848a063` passed all 24 workflows; retained keyboard artifact `9037726559` was independently inspected; merged as `187928c66143e0c8470082097fafba740da691c6`.
- [RUN-20260809-101 — RC9.4 exact-head acceptance](runs/RUN-20260809-101.md) — `PASS`: PR #57 exact head `487dbe1320a4ef820ff32f1c9ef8f8c7652a4868` passed all 23 workflows; retained auditor artifact `9037246175` was independently inspected; merged as `c7877015869bf58dec3a5f2628d71c4b0c2cf97a`.
- [RUN-20260809-099 — RC9.3 exact-head acceptance](runs/RUN-20260809-099.md) — `PASS`: PR #55 exact head `e945702adff884f174a40393b3121f3aed99648b` passed all 22 workflows; retained token-revocation artifact `9037014726` was independently inspected; merged as `3743203bc1a6d93743af53fcb8d4257af153a710`.

## Current decision

Phase 6 remains `BLOCKED_EXTERNAL` only for genuine VoiceOver/NVDA behavior on real supported hosts. Browser/DOM automation is not treated as a substitute.

Phase 7 is `IN PROGRESS`. RC10.1 request observability is accepted as `PASS`. RC10.2 connector-failure alerting is `CI_VALIDATION_PENDING` and cannot be accepted until complete exact-head CI and retained evidence inspection succeed. Issue #1 external production gates remain independently open.

## Exactly one next priority

Inspect every required workflow on the final RC10.2 pull-request head and retained `connector-alerting-evidence`; repair only the first deterministic failure, or accept/merge only after complete successful evidence.

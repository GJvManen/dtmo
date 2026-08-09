# DTMO Continuous Development Run Log

This file is the chronological audit record for continuous development runs. Detailed run records are stored under `docs/development/runs/`.

## Runs

- [RUN-20260809-128 — RC10.3 exact-head acceptance and documentation reconciliation](runs/RUN-20260809-128.md) — `PASS` in the final merged state: RC10.3 product evidence is accepted; the first documentation head `118d10c7b3ac971176fb7390499397049d7b4269` passed all 36 registered workflows, and the final status-bearing head is required to repeat complete exact-head success before protected merge.
- [RUN-20260809-127 — RC10.3 bounded queue-backlog alerting](runs/RUN-20260809-127.md) — `PASS`: PR #84 exact head `8058b476298eee4bcd2942d9cca54384ec12aa74` passed all 36 workflows; retained artifact `9040996591` (`sha256:42aaad1424d7c1ad40accd056b4746ea6fb328a561b24df5ebc293c0425b1910`) independently proved bounded queue depth/capacity/utilization metrics, 80% raise/50% clear hysteresis, correlated actionable evidence and RC8 queue-pressure reuse with 5/5 JUnit tests; merged as `42ccbe04cbc1081f93e4a155243627b5a3038573`.
- [RUN-20260809-126 — RC10.2 acceptance and historical documentation reconciliation](runs/RUN-20260809-126.md) — `PASS`: RC10.2 exact-head acceptance was recorded, stale/current-state documentation was reconciled, missing RUN-088/089/091/095/097 history was restored, and PR #83 final exact head `b321e9c7c1a23843d9d7cf4a64ab1bff57a969a4` passed all 35 workflows before merge as `24f3ff6210d8d1a5d70cca41a661641e974a4549`.
- [RUN-20260809-125 — RC10.2 controlled connector-failure alerting](runs/RUN-20260809-125.md) — `PASS`: PR #82 exact head `b38aeae44588e39e35339f4c4d9667947804b243` passed all 35 registered workflows; retained artifact `9040485255` (`sha256:96883158cfd790c3c6b21c2db819acbcbc03d431d4dd79bb32038b6ff258de25`) independently proved terminal alert, Prometheus rule/metric, correlated actionable evidence, repeat-raise suppression, raw-error exclusion and recovery/clear behavior with 4/4 JUnit tests; merged as `f6680423860389288d9feced34592294d774bf4a`.
- [RUN-20260809-124 — RC10.1 exact-head acceptance and documentation reconciliation](runs/RUN-20260809-124.md) — `PASS`: PR #80 exact head `01a175e12da7c8af8566178a2d7e6b34a57d58bc` passed all 34 registered workflows; retained artifact `9040196394` (`sha256:6792020994d94b0484cb84140d202433303eceb82565f8598ffd5937940531d6`) independently proved the bounded request-observability controls with 5/5 JUnit tests; merged as `1675d88bb24dcd50e20545f49b26dd7cc2810d97`.
- [RUN-20260809-123 — RC10.1 request observability baseline](runs/RUN-20260809-123.md) — `PASS`: implementation later accepted by RUN-124.
- [RUN-20260809-122 — RC9.16 genuine assistive-technology behavior](runs/RUN-20260809-122.md) — `BLOCKED_EXTERNAL`: real VoiceOver and NVDA behavior cannot be truthfully executed in the current automation environment; the required supported-host evidence matrix remains open.
- [RUN-20260809-121 — RC9.15 complete focus-order evidence](runs/RUN-20260809-121.md) — `PASS`: PR #78 exact head `d2480293f605e8701fb677071c206cc25da97098` passed all 33 workflows; retained artifact `9039862032` independently proved bounded SC 2.4.3 focus order; merged as `17a43175d6beda4fdf0156f701844d2c25ea4aec`.
- [RUN-20260809-120 — RC9.14 exact-head acceptance](runs/RUN-20260809-120.md) — `PASS`: PR #76 exact head `de52730b9b5165f7815e2c6c19c803413bbfcc60` passed all 32 workflows; retained artifact `9039432903` independently proved bounded text-spacing behavior; merged as `7d4816658159fac3b2b773fa6151b6274b510351`.
- [RUN-20260809-118 — RC9.13 exact-head acceptance](runs/RUN-20260809-118.md) — `PASS`: bounded SC 1.4.10 reflow accepted for PR #74.
- [RUN-20260809-116 — RC9.12 exact-head acceptance](runs/RUN-20260809-116.md) — `PASS`: bounded SC 1.4.4 200% text resize accepted for PR #72.
- [RUN-20260809-114 — RC9.11 exact-head acceptance](runs/RUN-20260809-114.md) — `PASS`: bounded text/UI/focus contrast accepted for PR #70.
- [RUN-20260809-112 — RC9.10 exact-head acceptance](runs/RUN-20260809-112.md) — `PASS`: A11Y-001 session-status remediation accepted for PR #68.
- [RUN-20260809-103 — RC9.5 exact-head acceptance](runs/RUN-20260809-103.md) — `PASS`: PR #59 passed all 24 workflows and merged as `187928c66143e0c8470082097fafba740da691c6`.
- [RUN-20260809-101 — RC9.4 exact-head acceptance](runs/RUN-20260809-101.md) — `PASS`: PR #57 passed all 23 workflows and merged as `c7877015869bf58dec3a5f2628d71c4b0c2cf97a`.
- [RUN-20260809-099 — RC9.3 exact-head acceptance](runs/RUN-20260809-099.md) — `PASS`: PR #55 passed all 22 workflows and merged as `3743203bc1a6d93743af53fcb8d4257af153a710`.
- [RUN-20260809-097 — RC9.2 exact-head acceptance](runs/RUN-20260809-097.md) — `PASS`: PR #53 passed all 21 workflows and merged as `22bf74bb6c5c367195a3e67b0c8db4ec0489a449`.
- [RUN-20260809-095 — RC9.1 exact-head acceptance](runs/RUN-20260809-095.md) — `PASS`: PR #50 passed all 20 workflows and merged as `ef59eba29d7fa8b2d88b5674e7bb00e98c0dab18`.
- [RUN-20260809-091 — RC8.8 exact-head acceptance and Phase 5 closure](runs/RUN-20260809-091.md) — `PASS`: PR #48 passed all 19 workflows and merged as `62b34472948d0f301104ddd452e14efb945fa6bd`.
- [RUN-20260809-089 — RC8.7 expected-head acceptance](runs/RUN-20260809-089.md) — `PASS`: PR #46 passed all 19 workflows and merged as `7ecd1bf88d0577074390a173847186c8a92e48b6`.

## Current decision

Phase 1–5 internal roadmap gates are `PASS`.

Phase 6 remains `BLOCKED_EXTERNAL` only for genuine VoiceOver/NVDA behavior on real supported hosts. Browser/DOM automation is not treated as a substitute.

Phase 7 is `IN PROGRESS`. RC10.1 request observability, RC10.2 connector-failure alerting and RC10.3 queue-backlog alerting are accepted as `PASS`. RUN-128 is authoritative `PASS` only after the final status-bearing exact head completes 36/36 and is protected-merged. Issue #1 external production gates remain independently open.

## Exactly one next priority

Phase 7 / RC10.4 — implement bounded storage-integrity alerting with controlled integrity-failure/recovery evidence, actionable correlation, no raw sensitive payload leakage and retained exact-head evidence. API-error and search-health alerting remain later Phase-7 objectives.

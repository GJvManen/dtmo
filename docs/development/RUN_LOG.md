# DTMO Continuous Development Run Log

This file is the chronological audit record for continuous development runs. Detailed run records are stored under `docs/development/runs/`.

## Runs

- [RUN-20260809-121 — RC9.15 complete focus-order evidence](runs/RUN-20260809-121.md) — `CI_VALIDATION_PENDING`: initial exact-head CI found a single-control reverse-navigation oracle defect; the next exact head `8441057557d4c25370f7fdbccdf98889e01ad48b` then produced a passing browser test and exact-head artifact `9039753331`, but the workflow validator incorrectly compared expected objects containing `tabIndex` with observed identity objects that omitted it. Both evidence-oracle defects were repaired without production-code changes. Final exact-head CI and retained focus-order evidence must rerun before PASS.
- [RUN-20260809-120 — RC9.14 exact-head acceptance](runs/RUN-20260809-120.md) — `PASS`: PR #76 exact head `de52730b9b5165f7815e2c6c19c803413bbfcc60` passed all 32 registered workflows; retained artifact `9039432903` (`sha256:f547bd306bb9c63e02d049dda24d52d962086388f777f8857921cc818e75c5f1`) independently proved bounded WCAG 2.2 SC 1.4.12 text-spacing behavior across all four accepted critical surfaces with 1/1 JUnit test passing, no detected clipped text, all governed controls focusable, real backend-session RBAC and preserved human share approval; merged as `7d4816658159fac3b2b773fa6151b6274b510351`.
- [RUN-20260809-119 — RC9.14 WCAG 2.2 text-spacing evidence](runs/RUN-20260809-119.md) — `CI_VALIDATION_PENDING`: implemented the bounded Chromium SC 1.4.12 gate later accepted by RUN-120.
- [RUN-20260809-118 — RC9.13 exact-head acceptance](runs/RUN-20260809-118.md) — `PASS`: bounded SC 1.4.10 reflow accepted for PR #74.
- [RUN-20260809-116 — RC9.12 exact-head acceptance](runs/RUN-20260809-116.md) — `PASS`: bounded SC 1.4.4 200% text resize accepted for PR #72.
- [RUN-20260809-114 — RC9.11 exact-head acceptance](runs/RUN-20260809-114.md) — `PASS`: bounded text/UI/focus contrast accepted for PR #70.
- [RUN-20260809-112 — RC9.10 exact-head acceptance](runs/RUN-20260809-112.md) — `PASS`: A11Y-001 session-status remediation accepted for PR #68.
- [RUN-20260809-110 — RC9.9 manual/non-automatable WCAG 2.2 AA critical-journey review](runs/RUN-20260809-110.md) — `BLOCKED`: automated/manual gaps have progressively closed; genuine VoiceOver/NVDA behavior remains open, while RC9.15 now addresses complete focus-order evidence.

## Current decision

`RUN-20260809-121` remains `CI_VALIDATION_PENDING`. The browser behavior is not presently known to be defective; both observed RC9.15 failures were evidence-oracle defects and were repaired. The final exact head must now execute every registered workflow and produce retained focus-order evidence before acceptance. Phase 6 remains `IN PROGRESS`; genuine assistive-technology behavior remains unevidenced. Issue #1 external production gates remain open.

## Exactly one next priority

Verify every registered workflow on the final repaired RC9.15 PR head and independently inspect retained `browser-focus-order-evidence`; repair only the first deterministic failure, or merge only after complete successful exact-head evidence.

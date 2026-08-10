# DTMO Continuous Development Run Log

This file is the chronological audit record for continuous development runs. Detailed run records are stored under `docs/development/runs/`.

## Runs

- [RUN-20260810-164 — RC6 residual RC9 exact-head remediation](runs/RUN-20260810-164.md) — `CI_VALIDATION_PENDING`: RUN-163 exact head `327b3d87ff8f1748d0c306a6837948ed0377df15` completed 43/48 registered workflows successfully but retained five RC9 failures. Direct logs identified CISO `ready` state compatibility, 320 CSS px auditor table reflow, measurable button backgrounds, and a shared text-resize/text-spacing Playwright CSP harness interaction. RUN-164 applies only those bounded fixes; production CSP remains unchanged. A complete fresh exact-head matrix is required.
- [RUN-20260810-163 — RC6 frontend RC9 acceptance-contract regression remediation](runs/RUN-20260810-163.md) — `FAILED_CI`: initial exact head `0e6bc86b425b4e6511520bd6734f79baf7413d97` failed 11 RC9 workflows / 22 checks. Remediation reduced the failure set, but validation head `327b3d87ff8f1748d0c306a6837948ed0377df15` still failed 5 of 48 workflows, so RUN-163 is not accepted.
- [RUN-20260810-162 — 16.0.0rc6 professional frontend UX overhaul](runs/RUN-20260810-162.md) — `FAILED_CI`: the professional task-oriented UX was implemented, but first exact head `0e6bc86b425b4e6511520bd6734f79baf7413d97` is not accepted because 11 registered RC9 workflows failed. Subsequent bounded remediation is tracked by RUN-163 and RUN-164; no PASS claim from RUN-162 is retained.
- [RUN-20260810-161 — 16.0.0rc5 frontend productionization](runs/RUN-20260810-161.md) — `PASS`: PR #111 exact head `1e59cd6f02bd5b853d0e8bf66a09c90d46d89467` completed all 48 registered workflows successfully and merged as `05e72443b132e0e0c162d2a07b1578e84daaa25c`. This acceptance is repository-controlled only and does not close genuine VoiceOver/NVDA, real staging or external-assurance gates.
- [RUN-20260810-160 — Documentation consolidation on main](runs/RUN-20260810-160.md) — `DOCUMENTATION_CONSOLIDATED`: extended living documentation was added directly to `main` after PR #110 exact head `5549ac1f28307c8bfa8c2ea1bf39341bb33983a0` completed all 48 registered workflows successfully and merged as `0b9a6d51dcd6e4fa984888d172e1fb5f5d6d52f2`. This run creates no new technical, staging, external-assurance or production PASS claim.
- [RUN-20260810-159 — Phase 9 external-assurance intake baseline](runs/RUN-20260810-159.md) — `PASS` for the readiness/intake contract only: PR #110 exact head `5549ac1f28307c8bfa8c2ea1bf39341bb33983a0` completed all 48 registered workflows successfully and merged as `0b9a6d51dcd6e4fa984888d172e1fb5f5d6d52f2`. No external assurance activity is claimed complete. Phase 8 remains externally blocked and Phase 9 remains `NOT COMPLETE`.
- [RUN-20260810-158 — Phase 8 real staging deployment-parity recheck](runs/RUN-20260810-158.md) — `BLOCKED_EXTERNAL`: PR #108 documentation-finalization exact head `bbba29a1269b5c09d1a94a27b38c317bae2590e7` completed 48/48 workflows successfully and merged as `de3561b42f8e4fec5947182e01563a6327d0e029`; fresh repository/issue review still found no approved real staging deployment or complete ten-class deployment-parity evidence package.
- [RUN-20260810-157 — Phase 8 runtime-smoke lifecycle regression remediation](runs/RUN-20260810-157.md) — `PASS`: PR #108 exact head `25ac24bfa40f2f9ccebb5d1307615c6fbd14cf05` completed 48/48 workflows successfully after the stale runtime-smoke lifecycle assertion was corrected; final documentation head also completed 48/48 and merged.
- [RUN-20260810-156 — Phase 8 real staging deployment-parity evidence acquisition](runs/RUN-20260810-156.md) — `BLOCKED_EXTERNAL`: repository-controlled evidence passed; no approved real staging deployment or complete ten-class deployment-parity package existed.
- [RUN-20260810-155 — Phase 8 staging-emulator runtime smoke fresh-base remediation](runs/RUN-20260810-155.md) — `PASS`.
- [RUN-20260810-154 — Phase 8 staging-emulator lifecycle regression remediation](runs/RUN-20260810-154.md) — `PASS`.
- [RUN-20260810-153 — Phase 8 staging emulator acceptance reconciliation](runs/RUN-20260810-153.md) — `PASS`.
- [RUN-20260809-152 — Phase 8 staging emulator CI-integrity remediation](runs/RUN-20260809-152.md) — `PASS`.
- [RUN-20260809-151 — production-equivalent staging emulator baseline](runs/RUN-20260809-151.md) — `PASS` for the repository-controlled emulator contract only.
- [RUN-20260809-150 — Phase 8 blocker acceptance reconciliation](runs/RUN-20260809-150.md) — `BLOCKED_EXTERNAL`.
- [RUN-20260809-149 — Phase 8 staging-readiness regression remediation](runs/RUN-20260809-149.md) — `PASS`.
- [RUN-20260809-148 — staging environment identification and deployment-parity evidence](runs/RUN-20260809-148.md) — `BLOCKED_EXTERNAL`.
- [RUN-20260809-147 — staging-readiness baseline](runs/RUN-20260809-147.md) — `PASS`.
- [RUN-20260809-146 — Phase 7 external operational-acceptance reconciliation](runs/RUN-20260809-146.md) — `PASS`.

Older run records remain under `docs/development/runs/` and in repository history.

## Current decision

Phase 1–5 are `PASS`. Phase 6 remains externally blocked for genuine VoiceOver/NVDA execution; rc5 is the last accepted frontend baseline while rc6 PR #112 is under RUN-164 remediation and is not accepted. Phase 7 is `PASS`. Phase 8 remains `BLOCKED_EXTERNAL` for one approved real staging deployment and all ten deployment-parity evidence classes. Phase 9 remains `NOT COMPLETE`; its repository-controlled readiness/intake contract is accepted. Phase 10 remains `NOT STARTED`. DTMO is not production ready.

## Exactly one next priority

Verify every registered workflow on the final RUN-164 remediation head of PR #112. Merge only on complete exact-head success; otherwise remediate the first concrete remaining failure.

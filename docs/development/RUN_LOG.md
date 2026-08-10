# DTMO Continuous Development Run Log

This file is the chronological audit record for continuous development runs. Detailed run records are stored under `docs/development/runs/`.

## Runs

- [RUN-20260810-169 — Search and live intelligence ingestion remediation](runs/RUN-20260810-169.md) — `CI_VALIDATION_PENDING`: acceptance feedback exposed a user-blocking search failure and a disconnected live-connector path. rc7 aligns the strict OpenSearch mapping with canonical confidence fields, creates the index safely on fresh-search, makes indexing replay-repairable, routes CISA KEV records through raw/canonical/provenance/search storage, and protects manual connector execution with `manage:connectors`. Added runtime-contract and connector-pipeline regression tests. No PASS claim until the complete registered workflow matrix succeeds on one final exact head.
- RUN-20260810-168 — PR #112 acceptance and merge reconciliation — `PASS`: exact head `e5e0d5e808d1f66c8f512fa35bd0ea3932fe8631` completed all 48 registered workflows successfully. PR #112 merged as `5c2a9c9a5d0d936784597899c97bf5be253c2394`, making 16.0.0rc6 the accepted repository-controlled professional frontend baseline. Genuine VoiceOver/NVDA, real staging, external assurance and production go/no-go remain outside this PASS claim.
- [RUN-20260810-167 — PR #112 visual accessibility evidence-scope remediation](runs/RUN-20260810-167.md) — `PASS`: final exact head `e5e0d5e808d1f66c8f512fa35bd0ea3932fe8631` completed 48/48 registered workflows successfully. The `.sr-only` Analyst search label remains accessible while visual geometry evidence correctly excludes intentionally non-visual content.
- [RUN-20260810-166 — PR #112 residual reflow and focus-contrast remediation](runs/RUN-20260810-166.md) — `FAILED_CI`: remediation fixed the RC9 Reflow and RC9 Contrast failures, but validation head `b33f270b201527249f847107863ee1184954f352` completed only 46/48 registered workflows successfully because RC9 Text Spacing and RC9 Text Resize still failed on the `.sr-only` analyst-search label. Follow-up was RUN-167.
- [RUN-20260810-165 — PR #112 RC9 final remediation](runs/RUN-20260810-165.md) — `FAILED_CI`: remediation fixed CISO success-copy compatibility, Share Approval control-boundary contrast, 200% text-resize scaling and text-spacing clipping, but validation head `854cbe9b6687ed65569d0551b280593a973a9cfd` still completed only 46/48 registered workflows successfully; follow-up was RUN-166.
- [RUN-20260810-164 — RC6 residual RC9 exact-head remediation](runs/RUN-20260810-164.md) — `FAILED_CI`: exact head `10a7953de141e4502f0ac87037f3a4eec4725602` completed 44/48 registered workflows successfully and retained four RC9 failures; follow-up remediation was tracked in RUN-165.
- [RUN-20260810-163 — RC6 frontend RC9 acceptance-contract regression remediation](runs/RUN-20260810-163.md) — `FAILED_CI`: initial exact head `0e6bc86b425b4e6511520bd6734f79baf7413d97` failed 11 RC9 workflows / 22 checks. Remediation reduced the failure set, but validation head `327b3d87ff8f1748d0c306a6837948ed0377df15` still failed 5 of 48 workflows, so RUN-163 is not accepted.
- [RUN-20260810-162 — 16.0.0rc6 professional frontend UX overhaul](runs/RUN-20260810-162.md) — `FAILED_CI` on its first exact head; subsequent bounded remediation in RUN-163 through RUN-167 produced the accepted final head recorded in RUN-168.
- [RUN-20260810-161 — 16.0.0rc5 frontend productionization](runs/RUN-20260810-161.md) — `PASS`: PR #111 exact head `1e59cd6f02bd5b853d0e8bf66a09c90d46d89467` completed all 48 registered workflows successfully and merged as `05e72443b132e0e0c162d2a07b1578e84daaa25c`.
- [RUN-20260810-160 — Documentation consolidation on main](runs/RUN-20260810-160.md) — `DOCUMENTATION_CONSOLIDATED`.
- [RUN-20260810-159 — Phase 9 external-assurance intake baseline](runs/RUN-20260810-159.md) — `PASS` for the readiness/intake contract only.
- [RUN-20260810-158 — Phase 8 real staging deployment-parity recheck](runs/RUN-20260810-158.md) — `BLOCKED_EXTERNAL`.
- [RUN-20260810-157 — Phase 8 runtime-smoke lifecycle regression remediation](runs/RUN-20260810-157.md) — `PASS`.
- [RUN-20260810-156 — Phase 8 real staging deployment-parity evidence acquisition](runs/RUN-20260810-156.md) — `BLOCKED_EXTERNAL`.
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

Phase 1–5 remain `PASS`, but RUN-169 records a higher-severity functional regression in the accepted application surface that must be remediated before advancing external staging evidence. Phase 6 rc6 remains the accepted repository-controlled frontend baseline while genuine VoiceOver/NVDA execution remains `BLOCKED_EXTERNAL`. Phase 7 is `PASS`. Phase 8 remains `BLOCKED_EXTERNAL` for one approved real staging deployment and all ten deployment-parity evidence classes. Phase 9 remains `NOT COMPLETE`; Phase 10 remains `NOT STARTED`. DTMO is not production ready.

## Exactly one next priority

Complete exact-head CI validation of RUN-169 / 16.0.0rc7. If and only if all registered workflows succeed, proceed to the governed admin configuration and source-registry workspace; otherwise remediate the first concrete remaining CI failure.

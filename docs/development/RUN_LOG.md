# DTMO Continuous Development Run Log

This file is the chronological audit record for continuous development runs. Detailed run records are stored under `docs/development/runs/`.

## Current RC13 runs

- [RUN-20260811-176 — RC13.1 merge and RC13.2 single-session analytics](runs/RUN-20260811-176.md) — RC13.1 accepted/merged; RC13.2 `PENDING_CI`.
- [RUN-20260811-175 — RC13 functional acceptance status correction](runs/RUN-20260811-175.md) — owner-observed functional blockers inserted RC13 and paused Phase 8.

## Earlier runs

- [RUN-20260811-188 — RC10.6 acceptance reconciliation](runs/RUN-20260811-188.md) — `PASS`: PR #121 exact head `2fa71cf01cb0eb6d249cdff9b50d8a2aef9a3896` completed the full registered workflow matrix successfully and is merged as `20e042baccae655655dd410545a68a81937e832e`; RC10 advancement stops complete.
- [RUN-20260811-187 — RC10.6 exact-head startup remediation](runs/RUN-20260811-187.md) — superseded by RUN-188 acceptance; restored accepted RC10.5 `main.py` behavior after the first inspected PR #121 failure exposed nonexistent `Permission.READ_METRICS`.
- [RUN-20260811-186 — RC10.6 local display preferences](runs/RUN-20260811-186.md) — `PASS` via subsequent exact-head validation and PR #121 merge.
- [RUN-20260811-185 — RC10.5 acceptance reconciliation and RC10.6 boundary](runs/RUN-20260811-185.md) — `PASS`: reconciles PR #120 merge and opens RC10.6 from accepted merge `df138ebbdde1fa0f30f4003e1a158b3419a3d3fe`.
- [RUN-20260811-184 — RC10.5 Administration Consolidation](runs/RUN-20260811-184.md) — `PASS` via PR #120 exact-head validation and merge.
- [RUN-20260811-183 — RC10.5 transition boundary](runs/RUN-20260811-183.md) — RC10.5 branch opened from accepted RC10.4 merge `8fcba5b1aff1aa5d3fe53426488f11e00e95d3a0`.
- [RUN-20260810-182 — RC10.4 quality-gate type narrowing remediation](runs/RUN-20260810-182.md) — `PASS` via subsequent exact-head validation and PR #119 merge.
- [RUN-20260810-181 — RC10.4 Source Center refinement](runs/RUN-20260810-181.md) — `PASS` via PR #119 acceptance and merge `8fcba5b1aff1aa5d3fe53426488f11e00e95d3a0`.
- RUN-20260810-180 — RC10.3 acceptance reconciliation — `PASS`: PR #118 merged as `1377899e7096c01362ab803c502c1d40812ef581`.
- [RUN-20260810-179 — RC10.3 quality-gate lint remediation](runs/RUN-20260810-179.md) — `PASS` via subsequent exact-head validation and PR #118 merge.
- [RUN-20260810-178 — RC10.3 Threat Intelligence Workspace](runs/RUN-20260810-178.md) — `PASS` via PR #118 acceptance.

Older run records remain under `docs/development/runs/` and in repository history.

## Current decision

Phases 1–7 are accepted. RC13 functional unified-console acceptance is `BLOCKED_INTERNAL`; RC13.1 is accepted via PR #151 and RC13.2 is the current priority. Phase 8 is `PAUSED_PENDING_RC13`; Phase 9 remains `NOT COMPLETE`; Phase 10 remains `NOT STARTED`. DTMO is not production ready.

## Exactly one next priority

**RC13.2 — exact-head accept single-session native Visual analytics without a separate Grafana login path.**

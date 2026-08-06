# DTMO Continuous Development Run Log

This file is the chronological audit record for continuous development runs. Detailed run records are stored under `docs/development/runs/`.

## Runs

- [RUN-20260806-028 — Align secure production configuration regression test](runs/RUN-20260806-028.md) — `BLOCKED`: Quality Gate #193 reached pytest and exposed a stale positive production fixture that omitted the new mandatory signing secret; fixture updated without weakening production validation; replacement exact-head CI pending
- [RUN-20260806-027 — Restore direct-call-safe principal resolution](runs/RUN-20260806-027.md) — `BLOCKED`: Quality Gate #189 reached pytest and exposed a FastAPI `Header` default object during direct invocation; dependency metadata now uses `Annotated` with real string defaults; replacement exact-head CI pending
- [RUN-20260806-026 — RC5.3 PyJWT type-contract remediation](runs/RUN-20260806-026.md) — `BLOCKED`: Quality Gate #185 reached strict MyPy after Ruff passed; PyJWT decode options now use the vendor `Options` contract; replacement exact-head CI pending
- [RUN-20260806-025 — RC5.3 trusted principal token validation](runs/RUN-20260806-025.md) — `CI_VALIDATION_PENDING`: production identity headers replaced by signed bearer-token principal resolution with issuer, audience, signature, time-claim and human/machine-boundary validation
- [RUN-20260806-024 — RC5.2 least-privilege RBAC and separation of duties](runs/RUN-20260806-024.md) — `PASS`: Quality Gate #179 succeeded and PR #10 was merged into `main`
- [RUN-20260806-023 — Restore clean RC5.1 delivery path](runs/RUN-20260806-023.md) — `PASS`: obsolete PRs closed; migration contract fixed; Quality Gate #177 succeeded and PR #9 was merged
- [RUN-20260806-022 — Reversible canonical intelligence migration](runs/RUN-20260806-022.md) — `PASS`: data-preserving RC4-to-RC5 migration validated by exact-head upgrade/downgrade/re-upgrade evidence
- [RUN-20260806-020 — Remediate pytest dependency advisory](runs/RUN-20260806-020.md) — `PASS`: pytest constrained to fixed version 9.0.3+ and later dependency audits succeeded
- [RUN-20260806-019 — RC5.1 canonical intelligence model](runs/RUN-20260806-019.md) — `PASS`: canonical classifications and deterministic confidence scoring merged after Quality Gate #177
- [RUN-20260806-013 — Restore observable GitHub Actions execution](runs/RUN-20260806-013.md) — `PASS`
- [RUN-20260806-012 — GitHub Actions execution canary](runs/RUN-20260806-012.md) — `BLOCKED`
- [RUN-20260806-011 — Aggregate CI release gate](runs/RUN-20260806-011.md) — `BLOCKED`
- [RUN-20260806-010 — Repository-side CI execution readiness preflight](runs/RUN-20260806-010.md) — `BLOCKED`
- [RUN-20260806-009 — Deterministic CI evidence pair verification](runs/RUN-20260806-009.md) — `BLOCKED`
- [RUN-20260806-008 — Identity-bound CI evidence manifest](runs/RUN-20260806-008.md) — `BLOCKED`
- [RUN-20260806-007 — Harden manual CI observation evidence](runs/RUN-20260806-007.md) — `BLOCKED`
- [RUN-20260806-006 — Independent CI execution observer](runs/RUN-20260806-006.md) — `BLOCKED`
- [RUN-20260806-005 — Diagnose absent GitHub Actions execution evidence](runs/RUN-20260806-005.md) — `BLOCKED`
- [RUN-20260806-004 — Observable CI workflow contract gate](runs/RUN-20260806-004.md) — `BLOCKED`
- [RUN-20260806-003 — CI workflow contract guard](runs/RUN-20260806-003.md) — `BLOCKED`
- [RUN-20260805-002 — Secured intelligence ingestion and search API](runs/RUN-20260805-002.md)
- RUN-20260805-001 — Continuous development bootstrap

## Entry template

```markdown
## RUN-YYYYMMDD-NNN — Title

- **Started:** timestamp and timezone
- **Workstream:** selected workstream
- **Objective:** bounded objective
- **Changes:** files, commits, issues or configuration
- **Validation:** tests and actual outcomes
- **CI evidence:** workflow/status details or `PENDING`
- **Known blockers:** concrete blockers
- **Next action:** one concrete next step
- **Release gate:** `PASS`, `BLOCKED` or `NO-CHANGE`
```

# RC12.6 — Unified console programme completion gate

Status: `PENDING_CI`

## Objective

Close the repository-controlled RC10.11/RC11/RC12 remediation programme only after the canonical documentation reflects the implementation actually merged through PR #147 and the close-out head itself completes the full registered workflow set.

## Accepted implementation evidence

### Executable source framework

- RC11.1 / PR #132 introduced one governed source adapter registry and dispatcher.
- RC11.2–RC11.10 / PRs #133–#141 completed the remaining operational vendor onboarding set.
- `docs/qa/SOURCE_CONNECTION_MATRIX.md` is the maintained connected-source contract.

### Unified product shell

- RC12.1 / PR #142 integrated source administration and operations into the canonical DTMO console.
- Registration/bootstrap, enable/disable, interval management, validation and manual execution reuse existing governed admin APIs.
- Legacy routes may remain for compatibility but do not define separate intended product shells.

### Graphical analytics

- RC12.2 / PR #143 adopted self-hosted Grafana for operational dashboarding.
- RC12.3 / PR #144 added dedicated least-privilege intelligence reporting views/role and a non-editable Grafana datasource.
- RC12.4 / PR #145 embedded Operations and Intelligence dashboards in the unified console.
- RC12.5a / PR #146 added the managed same-origin `/grafana/` gateway foundation.
- RC12.5b / PR #147 switched console embeds away from browser-facing `:3000` access to relative `/grafana/...` paths.
- PR #147 exact head `339207dd5ad038727da34e0a0058c74076847eea` merged as `6e74c5e45b6683e1fceba3ff14f554e36815b95f` after the returned exact-head workflow set completed successfully.

## Governance invariants

1. Server-side RBAC remains authoritative.
2. Source administration, ingestion, investigation and dashboard access do not grant publication authority.
3. Human review and separate share approval remain distinct decisions.
4. Grafana anonymous access remains disabled.
5. Grafana intelligence queries use only the accepted reporting boundary and do not reuse the DTMO application database identity.
6. Credential values are excluded from the catalog, registry and repository evidence.
7. Provenance, privacy, auditability, fail-closed execution and accessible table alternatives remain required.
8. Repository CI or emulator evidence does not satisfy Phase 8 real staging acceptance.

## Documentation reconciliation scope

This close-out updates the authoritative README, documentation index, current state, executive status, production roadmap, source connection matrix and release notes so they no longer describe obsolete RC10 workspaces as the current product architecture.

## Acceptance criteria

RC12.6 may be marked `PASS` only when:

1. all files above agree that RC11 and RC12 repository-controlled programmes are complete through PR #147;
2. issue #125's required repository-controlled outcomes are represented as completed without claiming external staging or production readiness;
3. the exactly-one-next-priority statement is Phase 8 real staging deployment parity;
4. no documentation claims that CI/emulator/local Compose substitutes for genuine external acceptance;
5. the complete registered workflow matrix succeeds on one exact close-out head.

## Release decision

`PENDING_CI` — do not merge or close issue #125 until the complete exact-head workflow set is green.

# RC10.11 Unified Console Gate

## Decision

`PENDING_CI`

## Objective

Close the product-level UI fragmentation discovered after RC10.9/RC10.10 by making one DTMO application shell the canonical operator experience before Phase 8 real staging acceptance resumes.

## RC10.11.1 scope

- canonical `/` unified console and `/ui/console` compatibility entry;
- in-shell sections for Overview, Intelligence, Sources & Catalog, Visual Analytics, Administration and Governance;
- full curated source catalog visible instead of filtering planned/research entries out of the product;
- existing governed bootstrap and manual-run endpoints orchestrated from the same shell for currently executable sources;
- explicit adapter-unavailable status for `planned-parser` and research-only sources rather than false run affordances;
- graphical severity/source/connector views using the existing read-only dashboard summary endpoint with table alternatives;
- Administration source-registry and local test-identity context visible inside the same shell;
- RBAC, separation of duties, human review and separate external share approval remain authoritative.

## Not yet claimed

RC10.11.1 does not claim that every curated `planned-parser` source is executable. RC10.11.2 must implement and validate the governed adapters required for the operational catalog sources selected for v1.0. No unsupported source may be presented as successfully executable.

## Acceptance rule

This slice may move to `PASS` only after exact-head CI succeeds and browser/regression evidence proves the primary root resolves to the unified shell, all required product areas are reachable without navigating to separate product shells, executable catalog sources retain the governed run path, visual analytics use real backend data, and governance boundaries remain intact.

Phase 8 remains paused until the complete RC10.11 objective is closed.

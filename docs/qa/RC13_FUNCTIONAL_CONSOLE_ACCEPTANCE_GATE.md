# RC13 — Functional Console Acceptance Gate

Status: `BLOCKED_INTERNAL` — RC13.5 `PENDING_CI` and accountable project-owner functional retest.

## Trigger

A project-owner functional test of `http://localhost:8000/` on 2026-08-11 found that the repository-controlled product was not yet functionally usable despite the earlier RC12 documentation close-out. This gate supersedes the previous Phase 8 handoff claim until the repaired product journey is proven and retested.

## Required acceptance journey

A fresh local/dev deployment must support the following from the canonical console without using legacy UI routes as the primary workflow:

1. open the canonical console and view useful Overview statistics/graphics;
2. inspect canonical recent Intelligence independently of OpenSearch search availability;
3. inspect the connected source catalog and distinguish source execution states;
4. register, enable/configure and manually execute an eligible framework source;
5. see fetched/inserted/indexed results, connector health and newly ingested intelligence;
6. view native severity/source/connector/review analytics without a separate Grafana login prerequisite;
7. administer governed DTMO principal/role assignments without weakening token or service-account boundaries;
8. view repository-backed Governance framework coverage, mappings, provenance and authority boundaries;
9. retain RBAC, separation of duties, privacy, provenance, auditability, human review and separate external share approval.

## Accepted RC13 slices

- **RC13.1 — PASS.** PR #151 merged as `95c4a5b072d141f50a02d23f8bf9abb862d6f8e2` after complete exact-head success. Source register/enable/run → ingest/index → recent intelligence → Overview is browser-proven.
- **RC13.2 — PASS.** PR #152 merged as `b8c254c5d099cde5dca624aa85b17c320594847e`. Native analytics are canonical and normal product use makes no `/grafana/` request.
- **RC13.3 — PASS.** PR #153 merged as `2e1029a43f7b44d8525fb89197d0a10458a3e992`. Governed managed-principal/role administration, auditability and external IdP/token-reissue boundaries are accepted.
- **RC13.4 — PASS.** PR #154 merged as `21672aaf1cf097228699810660eaac167da842d6` after full exact-head success on `0a227cb9f3972504287a6f7f064d6df18b76fbed`, including RC4 Quality Gate #813, RC13 Governance Knowledge Surface Gate #3 and Open Source Governance Gate #278. Normenkader IBP and MITRE ATT&CK remain explicitly `UNMAPPED`, CVSS remains `CONTEXT_ONLY`, and internal DTMO mappings remain repository-backed.

## RC13.5 — complete functional browser acceptance

Status: `PENDING_CI` / current and only engineering priority.

RC13.5 adds `RC13 Full Functional Console Acceptance Gate`. One Chromium browser context must exercise the canonical console end to end on one exact PR head:

**Overview → Intelligence → Sources & Catalog → source register/enable/run → Intelligence state update → Visual analytics → Administration → Governance → Overview state confirmation.**

The journey must prove:

- the same canonical session remains usable across all six product areas;
- a source operation produces visible ingest/index feedback and updated Intelligence/Overview state;
- native analytics reflect the same resulting state without a Grafana request/login dependency;
- governed RBAC create/update/deactivate remains functional and request-correlated;
- Governance renders truthful framework coverage, repository provenance and publication/share authority boundaries;
- no synthetic fixture, source execution, analytics view, Administration mutation or Governance visibility grants publication authority.

The workflow records exact-head evidence and fails closed if the Chromium journey does not succeed.

## Owner acceptance boundary

RC13.5 CI is **synthetic repository-controlled evidence only**. It does not replace the project owner's earlier finding or manufacture a successful manual retest.

After RC13.5 exact-head CI is green and merged, the accountable project owner must functionally retest the repaired local canonical product. Only an explicit successful owner retest may close RC13 and restore Phase 8 from `PAUSED_PENDING_RC13` to an external-validation-ready state.

## Phase 8 boundary

Phase 8 external staging validation remains **`PAUSED_PENDING_RC13`** while either RC13.5 exact-head acceptance or the accountable owner functional retest is incomplete.

Repository CI, Docker Compose, staging emulators, successful builds or the existence of UI controls do not substitute for the owner-observed repaired product journey.

## Release rule

Do not claim `READY_FOR_EXTERNAL_VALIDATION`, production readiness, external staging acceptance or pentest readiness until RC13.5 exact-head acceptance and the accountable project-owner functional retest are both complete.

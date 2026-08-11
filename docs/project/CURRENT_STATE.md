# DTMO Current Project State

Last reconciled: **2026-08-11**

## Executive summary

DTMO `16.0.0rc12` has completed the repository-controlled engineering programme through Phase 7. Project-owner functional testing on 2026-08-11 demonstrated that the canonical console required product-level remediation before external staging, so RC13 remains the active blocking programme.

Accepted RC13 slices:

- **RC13.1** — PR #151 merged as `95c4a5b072d141f50a02d23f8bf9abb862d6f8e2`; exact-head source → ingest → intelligence → Overview browser evidence passed.
- **RC13.2** — PR #152 merged as `b8c254c5d099cde5dca624aa85b17c320594847e`; exact-head native single-session analytics evidence passed.
- **RC13.3** — PR #153 merged as `2e1029a43f7b44d8525fb89197d0a10458a3e992`; exact-head governed Administration/RBAC evidence passed.
- **RC13.4** — PR #154 merged as `21672aaf1cf097228699810660eaac167da842d6`; exact-head Governance knowledge evidence passed on head `0a227cb9f3972504287a6f7f064d6df18b76fbed`, including RC4 Quality Gate #813, RC13 Governance Knowledge Surface Gate #3 and Open Source Governance Gate #278.

**RC13.5 — complete functional browser acceptance** is the only current engineering priority. DTMO remains **not production ready** and Phase 8 remains `PAUSED_PENDING_RC13` until RC13.5 exact-head CI and accountable project-owner functional retest are both complete.

## Phase status

| Phase | Status |
|---|---|
| 1. CI and workflow integrity | `PASS` |
| 2. Application security and identity | `PASS` |
| 3. Data integrity and recovery | `PASS` |
| 4. Connector reliability and provenance | `PASS` |
| 5. Performance and scalability | `PASS` |
| 6. Accessibility and operational UX | `PASS` — project-owner manual/external acceptance on 2026-08-11 |
| 7. Observability and incident operations | `PASS` |
| RC13. Functional unified-console acceptance | `BLOCKED_INTERNAL` — RC13.1–RC13.4 accepted; RC13.5 `PENDING_CI` |
| 8. Real staging acceptance | `PAUSED_PENDING_RC13` |
| 9. Independent external assurance | `NOT COMPLETE` |
| 10. Production go/no-go | `NOT STARTED` |

## Accepted RC13 product state

### RC13.1 — source-to-intelligence

The canonical console truthfully represents framework source state, supports register/enable/configure/run operations, processes results through canonical ingestion/indexing, shows fetched/inserted/indexed feedback, renders recent PostgreSQL-backed intelligence and refreshes Overview statistics.

### RC13.2 — visual analytics

Native severity, source, connector-health and review-status analytics are the canonical user-facing product surface. Normal analytics navigation performs no `/grafana/` request. Grafana remains separately authenticated for advanced/operations use.

### RC13.3 — Administration/RBAC

Managed principals/role assignments, immutable built-in roles, human-admin authorization, strict service-account isolation, self-management blocking, final-admin protection, tamper-evident auditing and explicit IdP/token-reissue semantics are accepted. DTMO does not mint or silently rewrite active production bearer-token claims.

### RC13.4 — Governance knowledge

The canonical Governance area exposes repository-backed framework coverage, mappings, provenance and authority boundaries. Normenkader IBP and MITRE ATT&CK are explicitly `UNMAPPED`; CVSS is `CONTEXT_ONLY`; internal DTMO governance mappings are `MAPPED_INTERNAL`. Missing mappings are not inferred.

## RC13.5 — complete functional browser acceptance

Status: `PENDING_CI`.

`RC13 Full Functional Console Acceptance Gate` must prove one Chromium browser context across:

**Overview → Intelligence → Sources & Catalog → source register/enable/run → Intelligence update → Visual analytics → Administration → Governance → Overview state confirmation.**

The exact-head browser evidence must prove that the repaired product slices work together in one canonical session and that no Grafana second login, RBAC shortcut or Governance visibility creates new authority.

This CI evidence remains synthetic. After exact-head success and merge, the accountable project owner must retest the repaired local product before RC13 can close.

## Source, identity and governance boundaries

The operational source adapters remain governed by `docs/qa/SOURCE_CONNECTION_MATRIX.md`. Credentialed integrations continue to use logical secret references only.

Production bearer tokens are externally issued and cryptographically validated. Managed RBAC assignments do not rewrite issued tokens; production role changes require identity-provider reconciliation or token reissue.

RBAC, least privilege, separation of duties, privacy, provenance, auditability, human review and separate external share approval remain authoritative. Source execution, analytics, Administration, Governance, CI or staging access cannot authorize publication.

## Exactly one current priority

**RC13.5 — exact-head accept the complete canonical-console Chromium journey, then obtain accountable project-owner functional retest.** Phase 8 remains paused until both are complete.

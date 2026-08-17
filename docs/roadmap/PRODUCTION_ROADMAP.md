# DTMO Roadmap — Production Readiness and Product Evolution

Last updated: **2026-08-17**

## Purpose

This roadmap separates production authorization from product evolution and platform industrialisation. Repository engineering, accountable acceptance, deployment-bound validation, independent assurance and production authorization remain distinct evidence classes.

## Current position

| Stage | Scope | Status |
|---|---|---|
| Phases 1–7 | Repository-controlled engineering baseline | `PASS` |
| RC13 + owner retest | Unified-console functional acceptance | `PASS / OWNER_ACCEPTED` |
| E8.1–E8.10 | Vulnerability & CTI ecosystem integrations | `PASS / REPOSITORY_COMPLETE` |
| Phase 8 | Production-equivalent validation | `PASS / OWNER_ACCEPTED` — historical candidate |
| Phase 9 | Independent external assurance | `PASS / EXTERNAL_ASSURANCE_ACCEPTED` — historical candidate |
| Phase 10 | Formal production go/no-go | `NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED` |
| Phase 11.1–11.7b | Accepted service/integration boundaries | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.8a | Governed Kubernetes/Helm/GitOps runtime foundation | `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED` |
| Phase 11.9 | Migration and compatibility | `NOT STARTED` |
| Phase 11.10 | New production-equivalent validation | `NOT STARTED` |
| Phase 11.11 | New independent external assurance | `NOT STARTED` |
| Phase 12 | New formal production go/no-go | `NOT STARTED` |

DTMO remains **not production authorized**. Phase 11 is `IN PROGRESS / ACTIVE` and remains the highest-priority programme.

## Historical readiness evidence

Phase 8 remains `PASS / OWNER_ACCEPTED` and Phase 9 remains `PASS / EXTERNAL_ASSURANCE_ACCEPTED` for the earlier candidate they actually covered. Those claims are historical and are not transferred to the materially changed Phase 11 platform.

## Phase 11 platform industrialisation

The authoritative detailed programme is `docs/roadmap/PLATFORM_INDUSTRIALISATION_ROADMAP.md`. The controlled order is Taranis → IntelOwl → OpenCTI → MISP → TheHive → Cortex historical decision / later owner-required connector → integrated runtime → migration/compatibility → new validation → new assurance.

### Phase 11.1–11.7b — accepted repository baseline

**Status:** `PASS / REPOSITORY_COMPLETE`

Accepted repository evidence covers Taranis collection/assessment and canonical adaptation, IntelOwl bounded enrichment, OpenCTI graph integration, MISP governed exchange, TheHive human-authorized case handoff and the later owner-required Cortex analyzer connector. These are repository engineering boundaries only.

The original Phase 11.7 no-adoption decision is preserved as historical evidence for its then-current requirements rather than rewritten after the later owner requirement.

### Phase 11.8 — integrated runtime industrialisation

**Status:** `IN PROGRESS / ACTIVE`

#### 11.8a Runtime foundation

**Status:** `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`

Current bounded repository scope:

- Helm chart and GitOps-owned environment configuration;
- immutable image digest enforcement;
- existing-secret consumption with no secret material stored in Git;
- non-root/read-only workload hardening and dropped capabilities;
- disabled automatic service-account token mounting;
- explicit probes and resources;
- application PodDisruptionBudget;
- fail-closed NetworkPolicy with explicit external CIDR allowlisting.

```mermaid
flowchart LR
    G[Reviewed Git revision] --> H[Helm render]
    H --> K[Kubernetes API]
    I[Immutable image digest] --> K
    S[External secret process] --> X[Existing Secret]
    X --> K
    K --> P[DTMO pod]
    N[Default-deny NetworkPolicy] -. restricts .-> P
```

The foundation does not prove live cluster admission/CNI behavior, cloud workload identity, external-secret provider integration, ingress/TLS, stateful/multi-zone HA, centralized observability, backup/recovery objectives, SBOM/scanning/signing/attestation, capacity or exercised upgrade/rollback. Those remain later bounded Phase 11.8 slices.

Taranis AI, IntelOwl, Cortex, OpenCTI, MISP and TheHive remain separate service/licensing/identity boundaries. Kubernetes placement does not grant publication/share authority, case-handoff authority or local-compromise proof.

### Phase 11.9 — Migration and compatibility

**Status:** `NOT STARTED`

Migration work begins only after the required bounded Phase 11.8 hardening slices are accepted. It must preserve canonical intelligence, provenance, classification/governance state and accepted service identity/reconciliation semantics with explicit rollback paths.

### Phase 11.10 — New production-equivalent validation

**Status:** `NOT STARTED`

Run fresh production-equivalent validation against one immutable integrated deployment identity. Historical Phase 8 evidence cannot satisfy this gate.

### Phase 11.11 — New independent external assurance

**Status:** `NOT STARTED`

Run fresh independent assurance against the same immutable integrated candidate after Phase 11.10 acceptance. Historical Phase 9 evidence cannot satisfy this gate.

## Phase 12 — Formal production GO/NO-GO

**Status:** `NOT STARTED`

Phase 12 starts only after accepted Phase 11.10/11.11 evidence plus required production ownership, IAM/secrets/network/recovery/monitoring/privacy/legal/change approvals for the same release identity.

## Product and platform boundary

DTMO remains the education-sector CTI and decision-support layer. Generic collection, enrichment, graph, exchange and case-management capabilities remain separate mature services. Provenance, RBAC, human publication/share authority, separate case-handoff authority and fail-closed evidence rules remain authoritative across the integrated runtime.

## Delivery and documentation discipline

Each material change requires one bounded pull request with explicit acceptance criteria, exact-head CI, expected-head protection, architecture/security/licensing/evidence boundaries and synchronized professional documentation. A code/integration PR is not mergeable if affected current-state, architecture, integration, security, QA/evidence, roadmap or user/admin documentation is stale.
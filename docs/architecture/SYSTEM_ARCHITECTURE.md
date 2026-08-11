# DTMO System Architecture

Last updated: **2026-08-11**  
Current baseline: **16.0.0rc12**

## Purpose

DTMO is an education-focused Cyber Threat Intelligence platform that collects official threat/vulnerability intelligence, normalizes it with provenance, supports governed investigation and administration, and presents operational and intelligence analytics without collapsing human approval boundaries.

## Logical architecture

```mermaid
flowchart LR
    EXT[Official external intelligence sources] --> CF[Source adapter / connector framework]
    CF --> NP[Normalization & provenance]
    NP --> API[FastAPI application services]

    API --> PG[(PostgreSQL)]
    API --> OS[(OpenSearch)]
    API --> RD[(Redis)]
    API --> OBJ[(Object evidence storage)]

    USER[Analyst / Admin / CISO / Auditor] --> CONSOLE[Unified DTMO console]
    CONSOLE --> API
    CONSOLE --> NATIVE[Native DTMO analytics]
    CONSOLE --> RBAC[Governed principal / role administration]
    CONSOLE --> GKS[Governance knowledge surface]
    RBAC --> PG
    GKS --> REG[Repository-backed mapping registry]

    IDP[External identity provider / token issuer] --> TOKEN[Signed bearer token]
    TOKEN --> API
    RBAC -. reconciliation / token reissue .-> IDP

    API --> PM[Prometheus]
    PM --> GF[Grafana]
    PG -->|explicit reporting views| GF
    OPS[Authenticated operations/admin] --> GW[Nginx gateway]
    GW -->|/grafana/| GF

    API --> GOV[RBAC / audit / review / share-approval controls]
```

## Architecture layers

### 1. Source ingress

Provider-specific adapters operate through the governed source framework. Execution is bounded by explicit source identity, supported execution profiles, timeout/retry behavior, fail-closed parsing and provenance retention.

Credentialed sources use logical secret references; credential values are resolved at runtime and are not stored in the source catalog.

### 2. Normalization and provenance

Provider payloads are converted into canonical intelligence records while preserving source identity, raw evidence references, confidence and relevant publication metadata. Missing enrichment is not invented.

### 3. Application and API

The Python 3.12+/FastAPI application provides authenticated APIs, source operations, search/investigation, administration, metrics and governance workflows.

The canonical browser product is the **unified DTMO console**. Legacy role/workspace routes may remain for compatibility but are not separate intended product shells.

RC13.4 adds authenticated read-only `GET /api/v1/governance/knowledge`. It exposes only repository-backed governance state and does not add governance write paths.

### 4. Persistence and search

| Component | Responsibility |
|---|---|
| PostgreSQL 17 | relational application state, managed principal/role assignments, governance state and explicit Grafana reporting views |
| OpenSearch 2.19 | intelligence search/index state |
| Redis 8 | cache/queue and runtime coordination state |
| S3-compatible AIStor/MinIO interface | object/evidence storage |

RC13.3 added `managed_principals` and `managed_role_assignments` through migration `0009_managed_rbac_assignments`.

RC13.4 governance knowledge is intentionally repository-backed rather than mutable database state. `docs/governance/GOVERNANCE_MAPPING_REGISTRY.md` is the authority for the visible mapping/coverage contract.

### 5. Identity and RBAC administration

Production bearer tokens are externally issued and cryptographically validated for issuer, audience, signature, known role values, principal type and token state. DTMO does not operate an internal production token issuer in the current baseline.

Managed principal/role state and active bearer-token claims are separate. Changing managed assignment state does not silently rewrite an already issued token; a production role change requires identity-provider reconciliation or token reissue.

Built-in roles and permissions remain defined by `Role` and `ROLE_PERMISSIONS`. The browser cannot invent arbitrary custom token roles. Machine/service principals remain restricted to `service_account`, while human principals cannot use that role.

RBAC administration requires both `manage:users` and a human `admin` role. The current administrator cannot mutate their own managed assignment, and the last active managed administrator cannot be deactivated or stripped of the admin role. Allowed mutations are written to the persistent tamper-evident audit chain with request correlation.

### 6. Observability and analytics

Prometheus collects bounded application/operational metrics. Grafana provides authenticated DTMO Operations and DTMO Intelligence dashboards for operational/advanced deployment use.

Grafana intelligence access uses a dedicated least-privilege database reader restricted to explicit reporting views. Anonymous Grafana access and Grafana self-signup are disabled.

Normal product analytics are **native DTMO chart/table views** backed by application APIs. RC13.2 made those native views the canonical Visual analytics surface and removed the separately authenticated Grafana embed from normal console use.

### 7. Browser and gateway boundary

The canonical product browser boundary is the FastAPI/unified-console session and its server-side authorization model. Native Visual analytics, governed Administration and read-only Governance knowledge use that application boundary.

The Administration or Governance UI is not an authorization authority by itself. Server-side permission/role checks and governance claim rules remain authoritative.

Nginx remains available as a managed deployment gateway and can expose the authenticated Grafana operational surface. The gateway and presentation layer do not grant application authority, publication authority or a role upgrade.

### 8. Governance knowledge and approval

RC13.4 distinguishes **framework context** from **actual repository mappings**.

- Normenkader IBP is visible as `UNMAPPED` because no control-level repository crosswalk exists yet.
- MITRE ATT&CK is visible as `UNMAPPED` because no technique-level repository mapping dataset exists yet.
- CVSS is visible as `CONTEXT_ONLY` because canonical ingest has `severity` and free `metadata`, but no first-class CVSS vector/base-score field.
- DTMO internal security/release governance is `MAPPED_INTERNAL` to explicit sections of `docs/security/SECURITY_OVERVIEW.md` and `docs/traceability/TRACEABILITY_MATRIX.md`.

No semantic similarity creates a mapping. A future external framework crosswalk must be an explicit versioned dataset with provenance and review.

Security-sensitive authorities remain separated:

- source administration and execution;
- managed identity/role administration;
- intelligence analysis;
- human review;
- external share approval;
- audit/read-only access;
- CISO/security administration.

Technical execution, Administration access, Governance visibility, CI success, connector access, dashboard access or staging access cannot authorize publication or external sharing.

## Principal technology stack

- Python 3.12+
- FastAPI / Uvicorn
- SQLAlchemy / Alembic
- PostgreSQL 17
- Redis 8
- OpenSearch 2.19
- S3-compatible object evidence storage
- Prometheus 3
- Grafana 13
- Nginx
- Docker Compose reference topology

## Trust boundaries

Important trust boundaries are:

1. external provider networks → connector/source ingress;
2. external identity provider/token issuer → bearer-token trust validation;
3. unauthenticated client → authenticated application boundary;
4. authenticated role → privileged administration/review/share actions;
5. managed assignment state → external identity-provider reconciliation/token reissue;
6. application → database/search/cache/object services;
7. Grafana → explicit least-privilege reporting boundary;
8. canonical browser → FastAPI/unified-console native analytics, Administration and Governance boundary;
9. repository mapping registry → visible framework/mapping claims;
10. repository CI/emulator → real staging/production environment;
11. technical execution → human publication/share authority.

## CI and release architecture

The release process is exact-head gated. Pull requests pass registered quality, security, connector, recovery, performance, browser/accessibility, observability and functional-console workflows before expected-head protected merge.

RC13.4 adds `RC13 Governance Knowledge Surface Gate` with repository provenance/coverage contracts plus a Chromium canonical Governance journey. Synthetic supporting API fixtures do not replace owner-observed local/live acceptance or later external staging validation.

## Current acceptance boundary

Phases 1–7 are accepted. RC13 is `BLOCKED_INTERNAL`.

- RC13.1: accepted via PR #151.
- RC13.2: accepted via PR #152, merge `b8c254c5d099cde5dca624aa85b17c320594847e`.
- RC13.3: accepted via PR #153, merge `2e1029a43f7b44d8525fb89197d0a10458a3e992`.
- RC13.4: current `PENDING_CI` priority.
- RC13.5: pending.
- Phase 8: `PAUSED_PENDING_RC13`.

## Security invariants

- RBAC and least privilege;
- known code-controlled roles and permissions;
- strict human/service-account role separation;
- human-admin + `manage:users` required for managed assignment mutations;
- administrator self-management and final-admin lockout protections;
- identity-provider reconciliation for production bearer-token claim changes;
- no inferred external framework/control/technique mapping;
- separation of duties;
- human share approval separate from review and technical access;
- provenance and confidence preservation;
- privacy and data minimization;
- auditable state transitions and request correlation;
- no secret values in repository evidence;
- no automatic publication from CI, connectors, recovery, analytics, Administration, Governance or runtime success;
- no anonymous Grafana access or authentication bypass for convenience.

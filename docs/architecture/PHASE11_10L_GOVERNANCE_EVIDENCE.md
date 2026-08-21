# Phase 11.10l — Governance & Evidence

Phase 11.10l makes governance knowledge visible in the canonical DTMO workbench without creating synthetic compliance claims. The workspace consumes the existing DTMO-owned `GET /api/v1/governance/knowledge` API, which is protected by `read:intelligence` and returns only repository-backed framework state, mappings, provenance and authority boundaries.

## Trust and evidence boundary

```mermaid
flowchart LR
    U[Authorized human user] -->|same-origin session| W[Governance & Evidence workspace]
    W -->|GET /api/v1/governance/knowledge| A[DTMO governance API]
    A --> K[Repository-backed governance knowledge]
    K --> F[Framework coverage]
    K --> M[Mappings + provenance]
    K --> B[Authority boundaries]
    F -. no inferred crosswalk .-> X[External framework equivalence]
    M -. visibility does not grant .-> P[Review / share / publication authority]
```

Normenkader IBP and MITRE ATT&CK remain explicitly unmapped until a governed control-/technique-level crosswalk exists in the repository. CVSS is presented as context-only where no first-class score/vector mapping exists. DTMO internal governance mappings are shown only where explicit repository provenance exists.

The browser never turns missing, stale or inaccessible evidence into PASS, compliance, risk acceptance, external assurance, production readiness or production authorization. Governance visibility is read-only and does not alter review, case, connector, sharing, publication or administrative authority.

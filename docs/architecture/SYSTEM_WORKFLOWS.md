# DTMO System Workflows

**Status:** Authoritative visual workflow reference  
**Baseline:** post-E8 / Phase 8–9  
**Purpose:** explain the principal DTMO runtime, security, governance and acceptance flows without replacing detailed contracts or evidence.

> These diagrams describe intended/implemented system behavior. They are not, by themselves, staging evidence, penetration-test evidence, independent assurance or production authorization.

## WF-01 — Source-to-intelligence

```mermaid
flowchart LR
    A[Approved source profile] --> B{Source enabled and authorized?}
    B -- No --> X[Fail closed / no retrieval]
    B -- Yes --> C[Connector retrieval]
    C --> D[Raw payload + source provenance]
    D --> E[(S3-compatible raw evidence)]
    D --> F[Normalization]
    F --> G{Contract-valid canonical candidate?}
    G -- No --> H[Reject / record degraded or invalid state]
    G -- Yes --> I[Deduplication / idempotency]
    I --> J[Enrichment / correlation]
    J --> K[(PostgreSQL canonical state)]
    J --> L[(OpenSearch supporting index)]
    K --> M[Authenticated FastAPI services]
    L --> M
    M --> N[Unified DTMO console]
    N --> O[Analyst review]
    O --> P{Share/export requested?}
    P -- No --> Q[Retain as governed intelligence]
    P -- Yes --> R[Separate human approval / sharing authority]
```

### Key controls

- retrieval is allowed only for governed source profiles;
- raw source evidence and provenance are preserved separately from derived intelligence;
- missing source facts are not invented during normalization;
- PostgreSQL is canonical application truth; OpenSearch is a supporting index;
- technical ingestion never grants publication or sharing authority;
- failures and degraded upstream states remain visible rather than being silently converted into successful intelligence.

## WF-02 — Vulnerability prioritization

```mermaid
flowchart TD
    A[Vulnerability observation / CVE evidence] --> B[Preserve source provenance]
    B --> C[CVSS context]
    B --> D[EPSS probability context]
    B --> E[CISA KEV / exploited-in-the-wild context]
    B --> F[Vendor / product relevance]
    B --> G[Local analyst context]
    C --> H[Prioritization model]
    D --> H
    E --> H
    F --> H
    G --> H
    H --> I[Severity / priority classification]
    I --> J[Analytics, trends and filters]
    I --> K[Analyst investigation]
    K --> L{Decision / action outside DTMO?}
    L --> M[Human-owned remediation / risk process]
```

### Semantic boundaries

CVSS, EPSS and KEV are different signals and must not be collapsed into a single unsupported claim. DTMO may combine them for prioritization while preserving provenance and meaning. A CVE record, high CVSS value, EPSS probability or KEV membership does not by itself prove local exposure, exploitability, compromise or remediation status.

## WF-03 — Identity, bearer trust and RBAC

```mermaid
sequenceDiagram
    participant U as Human or service principal
    participant IdP as External identity provider
    participant API as DTMO API
    participant IAM as DTMO principal/RBAC state
    participant AUD as Audit/correlation

    U->>IdP: Authenticate / obtain bearer token
    IdP-->>U: Signed token
    U->>API: Request + bearer token
    API->>API: Validate signature, issuer, audience, expiry
    alt invalid or missing token
        API->>AUD: Record denied request without token leakage
        API-->>U: Deny
    else token valid
        API->>IAM: Resolve managed principal and permissions
        IAM-->>API: Effective server-side authorization
        alt action not authorized
            API->>AUD: Record attributable denial
            API-->>U: Deny
        else action authorized
            API->>AUD: Correlated attributable action
            API-->>U: Execute scoped action
        end
    end
```

### Trust rules

- externally issued tokens are cryptographically validated;
- client-supplied role/identity headers do not establish privilege;
- server-side RBAC is authoritative;
- human and service identities remain distinct;
- privileged Administration requires explicit permission and remains auditable;
- stale or revoked privilege must not silently remain effective.

## WF-04 — Privileged Administration

```mermaid
flowchart TD
    A[Authenticated principal] --> B{Privileged Administration permission?}
    B -- No --> X[Deny + audit]
    B -- Yes --> C[Open Administration capability]
    C --> D[Select principal / role / permission change]
    D --> E{Safety and scope checks pass?}
    E -- No --> X
    E -- Yes --> F[Explicit confirmation / governed action]
    F --> G[Persist canonical RBAC state]
    G --> H[Invalidate or constrain stale privilege where required]
    H --> I[Attributable audit + correlation record]
    I --> J[Updated Administration view]
```

## WF-05 — MISP governed read and export

```mermaid
flowchart LR
    A[Approved MISP source] --> B[Read-only governed retrieval]
    B --> C[Normalize + preserve MISP provenance]
    C --> D[Analyst review in DTMO]
    D --> E{Outbound MISP export requested?}
    E -- No --> F[No external mutation]
    E -- Yes --> G[Validate feature control + distribution restrictions]
    G --> H{Human share approval granted?}
    H -- No --> I[Block export]
    H -- Yes --> J[Prepare governed export]
    J --> K[Replay / duplicate protection]
    K --> L[MISP outbound action]
    L --> M[Audit result and external reference]
```

## WF-06 — AIL enrichment and correlation

```mermaid
flowchart LR
    A[Approved AIL integration] --> B[Read / enrichment retrieval]
    B --> C[Preserve source references]
    C --> D[Normalize supported entities/context]
    D --> E[Correlation workspace]
    E --> F[Link related intelligence / indicators]
    F --> G[Analyst review]
    G --> H[Canonical intelligence context]
    H --> I[API / UI / analytics]
```

AIL access does not grant autonomous crawler control, mutation authority or publication authority.

## WF-07 — Audit and correlation trace

```mermaid
flowchart LR
    A[Inbound request] --> B[Correlation/request ID]
    B --> C[Authenticated actor]
    C --> D[Authorization decision]
    D --> E[Application action]
    D --> F[Denied/failed action]
    E --> G[Canonical state transition]
    F --> H[Security/audit event]
    G --> H
    H --> I[Structured logs / audit records]
    I --> J[Operational investigation]
```

Audit records distinguish human and service actors and must not expose bearer tokens or raw secrets.

## WF-08 — Governance mapping and evidence

```mermaid
flowchart TD
    A[Canonical intelligence / system evidence] --> B[Governed evidence relationship]
    C[Versioned framework/control registry] --> B
    B --> D[Explicit mapping]
    D --> E[Governance UI / evidence view]
    E --> F[Analyst / CISO / auditor interpretation]
    F --> G{Claim supported by evidence scope?}
    G -- No --> H[Do not infer compliance / maturity / remediation]
    G -- Yes --> I[Use scoped mapping in review/reporting]
```

Framework mappings are relationships, not blanket compliance statements. MITRE ATT&CK, Normenkader IBP, NIST CSF, CVSS, EPSS, KEV, MISP and AIL retain their own semantic boundaries.

## WF-09 — Observability

```mermaid
flowchart LR
    A[API / connectors / storage / queues] --> B[Bounded Prometheus metrics]
    A --> C[Structured logs]
    A --> D[Audit/correlation events]
    B --> E[Prometheus]
    E --> F[Grafana]
    C --> G[Operational investigation]
    D --> G
    F --> G
    G --> H[Alert / runbook / operator action]
```

Grafana remains separately authenticated and is an operational/advanced dashboard surface rather than an alternate authentication path into DTMO.

## WF-10 — Backup, recovery and rollback

```mermaid
flowchart TD
    A[Failure / recovery exercise] --> B[Identify affected service/data plane]
    B --> C{Canonical PostgreSQL affected?}
    C -- Yes --> D[Restore / validate PostgreSQL integrity]
    C -- No --> E[Continue targeted recovery]
    E --> F{OpenSearch affected?}
    F -- Yes --> G[Recover or rebuild supporting index]
    F -- No --> H{Object evidence affected?}
    H -- Yes --> I[Restore / verify object integrity]
    H -- No --> J{Redis/cache/queue affected?}
    J -- Yes --> K[Recover ephemeral coordination safely]
    D --> L[Application readiness + state checks]
    G --> L
    I --> L
    K --> L
    L --> M{Rollback required?}
    M -- Yes --> N[Return to approved prior immutable release]
    M -- No --> O[Continue current release]
    N --> P[Verify migrations, IAM/secrets and observability]
    O --> P
    P --> Q[Record RTO/RPO observations and evidence]
```

## WF-11 — Deployment and immutable staging identity

```mermaid
flowchart LR
    A[Exact repository candidate] --> B[Build immutable application image]
    B --> C[Image digest]
    A --> D[Exact deployed commit/release]
    C --> E[Approved production-equivalent staging]
    D --> E
    F[Runtime inventory + configuration parity] --> E
    G[IAM/secrets/TLS/network controls] --> E
    E --> H[Immutable deployment identity fingerprint]
    H --> I[Phase 8.2 platform/identity evidence]
    H --> J[Phase 8.3 source-to-intelligence evidence]
    H --> K[Phase 8.4 operations/recovery evidence]
    I --> L[Phase 8.5 accountable staging acceptance]
    J --> L
    K --> L
```

Evidence from different deployment identities must not be combined to manufacture acceptance.

## WF-12 — Production-readiness acceptance lifecycle

```mermaid
flowchart LR
    A[Phases 1–7 engineering PASS] --> B[RC13 functional owner acceptance]
    B --> C[E8 repository-complete product evolution]
    C --> D[Post-E8 production-equivalent staging]
    D --> E[Phase 8.2 platform / identity]
    E --> F[Phase 8.3 source-to-intelligence]
    F --> G[Phase 8.4 operations / recovery]
    G --> H[Phase 8.5 accountable staging acceptance]
    H --> I[Phase 9 independent external assurance]
    I --> J{All release-blocking findings resolved or formally accepted?}
    J -- No --> K[Remediate / retest / rebind evidence as required]
    K --> I
    J -- Yes --> L[Phase 10 formal production go/no-go]
    L --> M{GO?}
    M -- No --> N[BLOCKED / return to required gate]
    M -- Yes --> O[Production authorization]
```

## Related authoritative documents

- `docs/architecture/SYSTEM_ARCHITECTURE.md`
- `docs/security/SECURITY_OVERVIEW.md`
- `docs/governance/GOVERNANCE_MAPPING_REGISTRY.md`
- `docs/evidence/EVIDENCE_INDEX.md`
- `docs/project/CURRENT_STATE.md`
- `docs/roadmap/PRODUCTION_ROADMAP.md`
- `docs/qa/QA_AND_RELEASE_GATES.md`
- `docs/visual/DOCUMENTATION_VISUAL_STANDARD.md`

# Phase 6 RC9.1 — Governed browser decision journey

RC9.1 introduces the first browser-level Phase-6 acceptance path. It intentionally covers one high-risk workflow only: review of candidate intelligence followed by separate approval for external sharing.

```mermaid
sequenceDiagram
    participant A as Alice (admin/reviewer)
    participant UI as Browser UI
    participant API as DTMO API
    participant DB as PostgreSQL
    participant B as Bob (publisher)

    A->>UI: Open governed decision page
    UI->>API: GET /api/v1/ui/session
    API-->>UI: Backend-derived review + share permissions
    A->>UI: Review candidate
    UI->>API: POST /review
    API->>DB: review_status=reviewed, reviewed_by=Alice
    API-->>UI: review accepted, share_approved=false
    A->>UI: Attempt share approval
    UI->>API: POST /share-approval
    API-->>UI: 409 different principal required
    B->>UI: Open page as publisher
    UI->>API: GET /api/v1/ui/session
    API-->>UI: Share permission, no review permission
    B->>UI: Approve sharing
    UI->>API: POST /share-approval
    API->>DB: share_approved=true, share_approved_by=Bob
    API-->>UI: approval accepted
```

A service-account browser context must expose neither review nor share-approval controls. The browser never grants authorization: UI visibility is derived from backend-resolved permissions, while the backend remains authoritative for RBAC and separation of duties.

RC9.1 does not claim keyboard-only operation, responsive acceptance, cross-browser support or WCAG 2.2 AA compliance. Those remain separate Phase-6 gates.

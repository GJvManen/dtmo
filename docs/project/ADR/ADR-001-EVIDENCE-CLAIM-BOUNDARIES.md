# ADR-001 — Evidence and Claim Boundaries

Status: Accepted

Date: 2026-08-10

## Context

DTMO production readiness spans repository-controlled engineering, real-environment validation and independent external assurance. These evidence classes have different strengths and cannot safely be substituted for one another.

## Decision

DTMO uses strict evidence claim boundaries:

1. Repository CI proves only what was executed on the exact evidenced commit.
2. Emulator configuration evidence proves configuration/topology contracts only.
3. Application-container runtime smoke proves only the bounded container/runtime behavior that was executed.
4. Real staging acceptance requires independently observable evidence from one approved immutable staging deployment identity.
5. External assurance requires attributable evidence from the relevant independent or accountable party.
6. Missing, stale, inaccessible, inferred, skipped, cancelled, failed or unexecuted evidence is never PASS.
7. Human share approval remains a separate human authority and cannot be inferred from technical access or successful execution.

## Consequences

- Documentation must state the exact scope of every PASS.
- Lifecycle-state regressions must not force accepted evidence back to pending states, but they must preserve the non-overclaim boundary.
- A successful repository gate cannot close an external acceptance checkbox unless the external evidence itself exists.
- Staging emulator evidence cannot close real deployment-parity requirements.
- Generic vulnerability or threat reviews cannot close deployment-time review requirements unless tied to the immutable target release/platform.

## Governance

RBAC, separation of duties, privacy, provenance, auditability, least privilege, secret-value exclusion and human share approval remain mandatory across all evidence classes.

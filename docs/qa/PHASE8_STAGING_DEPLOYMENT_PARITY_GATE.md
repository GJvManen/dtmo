# Phase 8 Staging Deployment-Parity Gate

## Decision

`READY_FOR_EXTERNAL_VALIDATION / PENDING_EXTERNAL_DEPLOYMENT_IDENTITY`

## Objective

Require independently observable, production-equivalent staging deployment evidence before staging acceptance can be declared.

RC13 is `PASS`. The project owner explicitly accepted the repaired canonical local product on 2026-08-12. Phase 8 may therefore begin, but no real staging deployment is yet evidenced by the repository.

## Entry condition

The RC13 entry condition is complete:

1. RC13.1 source-to-intelligence path — accepted;
2. RC13.2 single-session Visual analytics — accepted;
3. RC13.3 governed Administration/RBAC — accepted;
4. RC13.4 Governance knowledge surface — accepted;
5. RC13.5 complete canonical-console browser acceptance — accepted on exact head `56805ec4ead5a14e9a2f776f84df42eb772302a4` and merged via PR #155;
6. accountable project-owner functional retest — explicitly accepted on 2026-08-12 with `RC13 owner retest akkoord`.

Issue #150 is closed as completed.

## Phase 8.1 — external deployment identity

The first executable Phase 8 gate is to establish **one approved production-equivalent staging environment and immutable deployment identity**.

The authoritative intake record is `docs/staging/PHASE8_DEPLOYMENT_IDENTITY_RECORD.md`.

Until that record contains independently observable evidence, Phase 8.1 remains `PENDING_EXTERNAL_DEPLOYMENT_IDENTITY`. Local Docker Compose, GitHub Actions staging emulators and repository contracts may support preparation but are not a staging deployment identity.

## Required external evidence

All evidence must be tied to the **same immutable staging deployment identity**:

1. approved staging environment identifier and accountable owner;
2. reachable staging endpoint through the approved access path;
3. immutable deployed application/container image digests and release identity;
4. infrastructure/runtime versions and configuration-parity evidence;
5. approved secrets-manager/identity references and least-privilege staging identities, with no secret values committed;
6. TLS certificate/termination and network-restriction evidence;
7. production-equivalent data-class/sanitization statement and explicit no-production-credential confirmation;
8. deployment log/change record tied to the immutable release identity;
9. rollback target/procedure tied to the staged release;
10. deployment-time security/CVE/vendor-advisory review evidence.

## Current evidence state

The repository contains a staging-readiness contract and staging emulator, but those sources explicitly do not prove that a real staging environment exists. No repository evidence currently establishes the ten external evidence classes above against one real immutable deployment identity.

Therefore:

- Phase 8 is **open for execution**;
- Phase 8 is **not PASS**;
- Phase 8.1 is `PENDING_EXTERNAL_DEPLOYMENT_IDENTITY`;
- later staging acceptance suites must not be credited until the deployment identity is established.

## Acceptance rule

Phase 8 becomes `PASS` only when all required external evidence is reviewable and consistently tied to one immutable production-equivalent staging deployment identity, deployed-environment acceptance suites succeed, and the accountable project owner records the external staging acceptance decision.

Missing, stale, inaccessible, contradictory or inferred evidence blocks acceptance.

## Identity/RBAC staging requirement

The staging deployment must demonstrate that externally issued bearer-token roles reconcile with governed managed principal/role assignments and the accepted identity-provider process. Staging must not rely on development header-based identity or assume that a database assignment silently rewrites an active bearer token.

## Governance staging requirement

The canonical Governance surface must remain read-only and preserve the accepted mapping truth boundary. External framework/control/technique mappings may not be promoted from `UNMAPPED`/`CONTEXT_ONLY` without explicit versioned repository evidence and provenance.

## Governance and privacy

- RBAC and separation of duties remain unchanged.
- Human share approval remains a separate human authority.
- Staging access or Governance visibility does not grant publication authority.
- Secret values, tokens, credentials and unnecessary personal data are excluded from repository evidence.
- Provenance and immutable deployment identity are mandatory.

## Exactly one next priority

**Phase 8.1 — establish and record the approved production-equivalent staging environment and immutable deployment identity.**
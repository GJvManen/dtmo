# DTMO Decision Register

## Purpose

This register provides a stable index of material project decisions that affect architecture, governance, evidence interpretation or production-readiness progression. Detailed architectural decisions remain in ADRs; implementation chronology remains in Git history and development records.

| Decision | Status | Rationale / consequence | Authoritative detail |
|---|---|---|---|
| PostgreSQL is canonical application persistence for normalized intelligence | Accepted | Console and application state require one durable application truth; search and object storage are supporting stores | `docs/architecture/SYSTEM_ARCHITECTURE.md` |
| Canonical operator experience is the unified DTMO console | Accepted | Normal product journeys should not depend on fragmented legacy views | `docs/ux/FRONTEND_UX.md` |
| Human and service-account authority remain separated | Accepted | Automation must not silently acquire human review, administration or publication authority | `docs/security/SECURITY_OVERVIEW.md` |
| External sharing requires separate explicit approval | Accepted | Ingestion, analytics, CI, Administration and deployment access do not authorize publication | `docs/security/SECURITY_OVERVIEW.md` |
| Evidence and acceptance claims fail closed | Accepted | Missing or inapplicable evidence must not be represented as success | `docs/project/ADR/ADR-001-EVIDENCE-CLAIM-BOUNDARIES.md` |
| Exact-head CI is required for repository-controlled acceptance | Accepted | A new commit invalidates CI evidence for an earlier head | `docs/qa/QA_AND_RELEASE_GATES.md` |
| Local Compose and staging emulators do not constitute real Phase 8 staging evidence | Accepted | Production-equivalent staging requires an externally observable approved deployment identity | `docs/staging/PHASE8_DEPLOYMENT_IDENTITY_RECORD.md` |
| Framework mappings must be explicit and first-class | Accepted | Semantic similarity, tags or prose cannot manufacture compliance mappings | `docs/governance/GOVERNANCE_MAPPING_REGISTRY.md` |
| RC13 functional acceptance and production readiness are separate | Accepted | Functional product acceptance does not replace staging, independent assurance or production go/no-go | `docs/project/PRODUCTION_READINESS_REPORT.md` |
| Professional documentation and implementation chronology are separated | Accepted | Stable documentation must remain readable and decision-oriented while evidence history remains auditable | `docs/project/DOCUMENTATION_STANDARD.md` |

## Adding a decision

Add an entry when a decision materially changes how DTMO is built, governed, accepted, operated or interpreted. Create a dedicated ADR when the rationale, alternatives, consequences or reversibility require durable architectural treatment.

Do not use this register as a changelog. Routine implementation choices belong in pull requests, issues and development records.

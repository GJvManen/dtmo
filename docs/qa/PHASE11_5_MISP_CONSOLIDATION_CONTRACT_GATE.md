# Phase 11.5 MISP Consolidation Contract Gate

## Objective

Validate the bounded Phase 11.5 MISP consolidation authority/service/API/licensing contract before implementation changes.

## Required repository evidence

- MISP v2.5.44 upstream baseline is recorded.
- MISP remains a separate AGPL-3.0 service/API boundary; no source vendoring is authorized.
- Existing `events/restSearch` inbound and `events/add` governed outbound paths are identified as the capabilities to consolidate.
- Event/attribute/object UUID identity and DTMO canonical identity remain distinct.
- Distribution, sharing-group and TLP restrictions are preserved and cannot be broadened on re-export.
- Ingestion/import does not grant `share_approved`, publication authority or local-compromise proof.
- Outbound sharing requires attributable human DTMO review/share approval; service accounts cannot grant authority.
- Destination events remain unpublished; delivery success is not publication/federation approval.
- Replay reservations and uncertain-delivery behavior fail closed.
- MISP server synchronization and OpenCTI↔MISP automatic synchronization are excluded from this first consolidation boundary.
- Runtime credentials remain secret; production HTTPS and least-privilege identities are required.
- Current-state, roadmap, security, evidence and documentation portal references are synchronized.
- Repository CI is explicitly separated from live MISP/deployment/assurance/production evidence.

## Acceptance rule

The contract PR is repository-complete only when the exact final head passes the Phase 11 MISP Consolidation Contract Gate, Professional Documentation Gate and all required repository CI. Merge must use expected-head protection.

After protected merge, start exactly one bounded implementation PR for the reconciled MISP synchronization state/persistence and authority model. Phase 11.6 remains blocked until Phase 11.5 is repository-complete.

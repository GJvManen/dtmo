# Owner Functional Retest — 2026-08-26

## Decision

**REJECTED / FUNCTIONAL RECOVERY REOPENED**

The current canonical DTMO workbench is not accepted as a workable product. Candidate freeze and fresh Phase 11.10p production-equivalent validation must not proceed while owner-observed canonical functions remain unusable.

## Reported blocker

The owner reported that canonical **Administration still does not work** and requested a renewed functional test of all canonical pages and functions.

Repository inspection identified a concrete local-runtime mismatch: legacy operator pages send the existing non-production DTMO development identity context (`X-DTMO-Subject`, `X-DTMO-Roles`, `X-DTMO-API-Key`), while the React workbench previously sent only same-origin cookies. In the accepted non-production auth contract, absent headers resolve to the default `anonymous` / `executive` development principal. That can make canonical Administration appear unavailable even though the protected APIs exist.

## First bounded recovery change

The canonical workbench now preserves the existing local development identity context for **same-origin** fetches only. This does not bypass server-side RBAC and does not weaken production authentication:

- server-side permission checks remain authoritative;
- production still requires bearer authentication;
- existing Authorization headers are not replaced;
- no development headers are attached to cross-origin requests;
- credentials and integration secrets remain server-side;
- review, sharing, publication and responder authority remain separate governed permissions.

## Remaining acceptance work

This change addresses only the verified local canonical-auth mismatch. It does **not** constitute full functional acceptance. A renewed page-by-page canonical functional recovery must continue after exact-head CI, including Command Center, Threat Intelligence, IOC Explorer, Knowledge Graph, Exposure, Investigations, Analysis & Enrichment, Sharing & Exchange, Automation & Playbooks, Collection, Governance & Evidence, Operations and Administration.

No production-equivalent, staging, penetration-test, independent-assurance or production evidence is claimed by this record.

# AIL correlation workspace

## Scope

E8.9b exposes the E8.9a deterministic AIL correlation contract in DTMO's authenticated Threat Intelligence Workspace. The surface is analysis-only and requires the existing `READ_INTELLIGENCE` permission for correlation data.

For an AIL-derived indicator, DTMO may show exact canonical matches, MISP event/object attribute matches, vulnerability identifiers and bounded vendor/product context. AIL investigation context is limited to retained investigation identifiers.

## Privacy and data minimization

The workspace does not render AIL paste bodies, leak bodies, investigation titles or investigation notes. E8.8 already stores a data-minimized AIL projection; E8.9b consumes that projection and preserves the `raw_content_exposed=false` boundary.

MISP raw evidence is read only to recover the provenance-preserved `_dtmo_misp` projection required by the accepted E8.9a correlation contract. Failure to retrieve that evidence is surfaced as `degraded`; it is not represented as a complete result set.

## Correlation semantics

Matching remains deterministic and exact. No fuzzy matching, semantic similarity, inferred attribution, inferred compromise, inferred exposure or inferred affected-version presence is introduced by the workspace.

A correlation is analytical context only. It does not grant review, publication, MISP publication/synchronization, external sharing or remediation authority.

## UI states

- `ok`: one or more exact correlations are available and required evidence was readable;
- `empty`: the selected record is outside AIL scope or no exact correlations exist;
- `degraded`: required AIL/MISP projection evidence or the correlation API is unavailable or malformed.

The browser never silently converts a degraded result into an empty or successful state.

## Repository evidence boundary

The dedicated **E8 AIL Correlation Workspace Gate** executes contract checks and a Chromium journey using synthetic HTTP fixtures. This evidence proves repository behavior only. It does not prove live AIL or MISP connectivity, source completeness, collection/redistribution authority, production deployment, owner acceptance or penetration-test acceptance.

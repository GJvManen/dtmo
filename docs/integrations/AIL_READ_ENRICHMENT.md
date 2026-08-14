# AIL Project read/enrichment integration

## Scope

E8.8 adds a disabled-by-default, read-only DTMO connector for explicit AIL Project objects. It is an enrichment/import boundary, not a crawler controller. DTMO requests only object global IDs that an operator has deliberately configured and projects supported extracted indicators into canonical DTMO `indicator` intelligence.

The implementation follows AIL Framework's authenticated `GET api/v1/object?gid=...` route. AIL resolves a global object identifier into object metadata. DTMO does not call AIL crawler creation, crawler scheduling, import or mutation routes.

## Configuration

Runtime settings use the existing `DTMO_` prefix:

- `DTMO_FEATURE_AIL_CONNECTOR=false` by default;
- `DTMO_AIL_API_BASE` for the AIL API origin;
- `DTMO_AIL_API_KEY` as a runtime secret;
- `DTMO_AIL_OBJECT_GLOBAL_IDS` as a comma-separated set of explicit `type:subtype:id` targets;
- `DTMO_AIL_OBJECT_LIMIT` bounds the number of targets per run.

Production enables the connector only with HTTPS, a non-empty runtime API key and explicit object targets.

## Data minimisation

The connector allowlists AIL object types that DTMO treats as extracted security indicators: `domain`, `ip`, `cve`, `cryptocurrency` and `ssh-key`. General AIL `item`/paste content and other object classes are rejected by this slice.

DTMO does not persist the returned AIL object body. The canonical raw projection stores only:

- AIL global object ID;
- indicator type/subtype/value;
- investigation identifiers when AIL returns an investigation reference;
- read-only/data-minimisation/share-authority boundary flags.

Investigation titles, notes and raw paste/content fields are deliberately not copied. An investigation identifier is provenance/context only; it does not import AIL case ownership, case status or authorization into DTMO.

## Governance boundary

The connector cannot create, schedule or execute an AIL crawler. It cannot submit imports, mutate AIL objects or create an AIL investigation. Imported indicators remain subject to normal DTMO review, provenance and publication/share controls. Successful retrieval does not imply external-share approval.

## Evidence boundary

Repository tests use synthetic AIL objects and mocked HTTP transport. Green CI proves the repository contract only. It does not prove live AIL connectivity, completeness of AIL extraction, destination/source authorization, production deployment, owner acceptance, penetration-test acceptance or permission to redistribute source material.

## Upstream contract reference

The AIL Framework repository defines the authenticated `api/v1/object` GET route in `var/www/blueprints/api_rest.py`; it delegates global-ID lookup to `api_get_object_global_id`. The object library resolves global IDs as `type:subtype:id` and returns object metadata. Those upstream read semantics are the only AIL API capability used by this slice.

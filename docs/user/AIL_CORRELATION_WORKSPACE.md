# AIL Correlation in the Unified Operations Workbench

## Purpose

AIL is a first-class governed framework building block in DTMO for read-only correlation and enrichment context. It complements Taranis AI collection, IntelOwl/Cortex analysis, OpenCTI graph context, MISP exchange and TheHive case handoff without becoming DTMO canonical truth or receiving DTMO human authority.

The canonical operator experience remains **browser → same-origin DTMO API → governed AIL adapter → AIL**. The browser never calls AIL directly and never receives the AIL API key.

## Where operators encounter AIL

AIL-derived context is surfaced through the canonical Intelligence/investigation experience when an attributable DTMO record has supported AIL correlation. Operators use that context to inspect supported indicators and investigation references while preserving the originating DTMO record, provenance and evidence boundaries.

AIL is not a separate primary DTMO application. Legacy or upstream AIL interfaces may still exist for AIL-native administration, but they are not required for the supported DTMO read/correlation journey.

## Supported read boundary

DTMO's AIL connector is disabled by default and reads only explicitly configured AIL object global IDs. Supported canonical indicator projections are bounded to allowlisted object classes such as domain, IP, CVE, cryptocurrency and SSH-key context.

DTMO does **not** use this connector to:

- create or schedule AIL crawlers;
- submit imports;
- mutate AIL objects;
- create or administer AIL investigations;
- copy arbitrary paste/item bodies into DTMO;
- grant review, case, sharing or publication authority.

Raw AIL content remains minimized. An AIL investigation identifier is provenance/context only and does not import AIL case ownership, status or authorization into DTMO.

## Readiness and configuration

The connector remains fail-closed until the required server-side configuration is present. Relevant runtime settings include `DTMO_FEATURE_AIL_CONNECTOR`, `DTMO_AIL_API_BASE`, `DTMO_AIL_API_KEY`, explicit `DTMO_AIL_OBJECT_GLOBAL_IDS` and the bounded object limit.

Credentials remain server-side. An enabled switch without a valid endpoint, key and explicit target scope must not be presented as working connectivity. Operators should use the canonical Administration/readiness surfaces to distinguish configured, ready and blocked integration states.

## Operator interpretation

A successful AIL lookup proves only that DTMO recorded the bounded read/correlation result for the configured object. It does not prove:

- live-source completeness;
- local compromise or exposure;
- permission to redistribute source material;
- external-share approval;
- remediation success;
- production readiness or production authorization.

AIL-derived indicators remain subject to normal DTMO provenance, review and sharing controls.

## Related contracts

- `docs/architecture/SYSTEM_ARCHITECTURE.md` — AIL as a governed external service boundary.
- `docs/integrations/AIL_READ_ENRICHMENT.md` — API/read, configuration and data-minimisation contract.
- `docs/integrations/AIL_CORRELATION_EXPERIENCE.md` — canonical correlation experience and claim boundaries.
- `docs/visual/screenshots/ail-correlation-workspace.png` — governed documentation illustration only; synthetic fixture data does not prove live AIL connectivity.

## Evidence boundary

Repository CI and deterministic browser fixtures are repository-controlled engineering evidence only. They do not establish owner acceptance, production-equivalent validation, penetration-test acceptance, independent assurance or production authorization.
# DTMO

**Dutch Threat Monitoring for Education**

DTMO is een open, onderwijsgericht Cyber Threat Intelligence-platform voor historische incidenten, actuele intelligence, kwetsbaarheden, IOC's, leveranciersrisico en bestuurlijke rapportage.

## Huidige ontwikkelfase

De repository start met **RC4.1 — Platform Foundation**. Deze sprint richt zich op:

- een productiegerichte repositorystructuur;
- centrale configuratie en feature flags;
- Docker Compose voor backend, PostgreSQL, Redis, OpenSearch en MinIO;
- scheduler- en workerfundament;
- gestructureerde logging en metrics;
- automatische QA via GitHub Actions;
- GitHub Pages voor de project- en releasepagina.

## Repositorystructuur

```text
backend/
frontend/
connectors/
infrastructure/
database/
tests/
docs/
scripts/
releases/
```

## Veiligheids- en governancegrenzen

- Intelligence wordt niet automatisch extern gepubliceerd.
- `reviewed` is niet gelijk aan `share approved`.
- Open bronnen en OSINT behouden provenance, confidence en bronclassificatie.
- Productieacceptatie vereist onafhankelijke penetratietests, loadtests en deployment acceptance.

## GitHub Pages

De statische projectpagina staat in `docs/` en wordt gepubliceerd via `.github/workflows/pages.yml` zodra GitHub Pages is ingesteld op **GitHub Actions**.

## Status

RC4.1: in ontwikkeling.

# DTMO

**Dutch Threat Monitoring for Education**

DTMO is een open, onderwijsgericht Cyber Threat Intelligence-platform voor historische incidenten, actuele intelligence, kwetsbaarheden, IOC's, leveranciersrisico en bestuurlijke rapportage.

## RC4

De repository bevat nu de eerste volledige **RC4 platform foundation**:

- FastAPI-backend met health-, readiness-, connector- en metrics-endpoints;
- centrale configuratie voor development, test, staging en productie;
- gestructureerde JSON-logging en correlation IDs;
- live connectorframework met timeouts, retries en exponential backoff;
- een CISA KEV live connector;
- een asynchrone scheduler met overlapbeveiliging en misfire-behandeling;
- PostgreSQL, Redis, OpenSearch, MinIO en Prometheus via Docker Compose;
- read-only applicatiecontainer en securityheaders;
- GitHub Actions voor linting, typing, tests, coverage, dependency review en containersmoke-tests;
- een professionele GitHub Pages-projectpagina.

## Snel starten

```bash
cp .env.example .env
docker compose up --build
```

Daarna:

- API: `http://localhost:8000`
- Health: `http://localhost:8000/health`
- OpenAPI: `http://localhost:8000/docs`
- Metrics: `http://localhost:8000/metrics`
- MinIO Console: `http://localhost:9001`
- Prometheus: `http://localhost:9090`

Live connectoren staan standaard uit. Activeer ze alleen gecontroleerd:

```text
DTMO_FEATURE_LIVE_CONNECTORS=true
```

## Repositorystructuur

```text
backend/dtmo/                 applicatiecode
backend/tests/                geautomatiseerde tests
infrastructure/prometheus/    monitoring
.github/workflows/            CI en GitHub Pages
docs/                         projectpagina en documentatie
Dockerfile                    applicatiecontainer
docker-compose.yml            lokale platformstack
```

## Veiligheids- en governancegrenzen

- Intelligence wordt niet automatisch extern gepubliceerd.
- `reviewed` is niet gelijk aan `share approved`.
- Publicatie vereist menselijke goedkeuring.
- Open bronnen en OSINT behouden provenance, confidence en bronclassificatie.
- Secrets horen uitsluitend in environment variables of een secrets manager.
- Productieacceptatie vereist een onafhankelijke penetratietest, loadtest en deployment acceptance.

## Quality gates

De GitHub Actions-workflow controleert:

1. Ruff-linting;
2. strict MyPy typing;
3. Pytest met minimaal 80% dekking;
4. Python compile checks;
5. containerbuild;
6. containersmoke-test tegen `/health`;
7. dependency review bij pull requests.

## GitHub Pages

De statische projectpagina staat in `docs/` en wordt gepubliceerd via `.github/workflows/pages.yml`. Stel onder **Settings → Pages → Build and deployment** de bron in op **GitHub Actions**.

## Releasegrens

RC4 is een controleerbare platformbasis. De repository claimt niet dat alle connectors al live zijn of dat het platform zonder externe acceptatietests productierijp is.

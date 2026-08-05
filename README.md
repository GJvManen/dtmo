# DTMO

**Dutch Threat Monitoring for Education**

DTMO is een open, onderwijsgericht Cyber Threat Intelligence-platform voor historische incidenten, actuele intelligence, kwetsbaarheden, IOC's, leveranciersrisico en bestuurlijke rapportage.

## RC4.8 implementation

De repository bevat nu stapsgewijze implementaties van RC4.1 tot en met RC4.8:

- **RC4.1:** FastAPI-platformbasis, configuratie, logging, scheduler, metrics, Docker Compose en CI;
- **RC4.2:** PostgreSQL/SQLAlchemy-persistentiemodellen, provenance en gecontroleerde share approval;
- **RC4.3:** immutable Intelligence Lake met SHA-256-receipts en integriteitscontrole;
- **RC4.4:** beheerde connectorcatalogus, reliabilityvalidatie en health snapshots;
- **RC4.5:** evidence-backed Knowledge Graph en begrensde attack-pathqueries;
- **RC4.6:** responsieve SOC/CTI-workspace voor intelligence, CVE's, IOC's, graph en hunting;
- **RC4.7:** RBAC, scheiding van review en share approval, evidence-gated reporting en exports;
- **RC4.8:** geïntegreerde cross-sprinttests en formele QA/releasegrenzen.

## Huidige status

**CI VALIDATION PENDING**

De code en tests zijn gecommit. RC4.8 wordt pas `RC_READY` nadat de nieuwste GitHub Actions-workflow aantoonbaar succesvol is afgerond. Een ontbrekende status wordt niet als pass behandeld.

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

Live connectoren staan standaard uit. Activeer deze alleen gecontroleerd:

```text
DTMO_FEATURE_LIVE_CONNECTORS=true
```

## Repositorystructuur

```text
backend/dtmo/                 API, connectors, persistence, lake, graph, auth en reporting
backend/tests/                unit- en regressietests
frontend/                     professionele SOC/CTI-workspace
infrastructure/prometheus/    monitoring
.github/workflows/            CI en GitHub Pages
docs/                         projectpagina en documentatie
releases/RC4.8/               release notes en QA-rapport
Dockerfile                    applicatiecontainer
docker-compose.yml            lokale platformstack
```

## Veiligheids- en governancegrenzen

- Intelligence wordt niet automatisch extern gepubliceerd.
- `reviewed` is niet gelijk aan `share approved`.
- Publicatie vereist een afzonderlijke bevoegdheid en menselijke goedkeuring.
- Open bronnen en OSINT behouden provenance, confidence en bronclassificatie.
- Rapportages zonder evidence worden geweigerd.
- Secrets horen uitsluitend in environment variables of een secrets manager.
- Productieacceptatie vereist onafhankelijke pentest, loadtest, hersteltest en deployment acceptance.

## Quality gates

GitHub Actions controleert onder meer:

1. Ruff-linting;
2. strict MyPy typing;
3. Pytest met coverage-drempel;
4. cross-sprinttests voor lake, graph, RBAC en reporting;
5. Python compile checks;
6. containerbuild;
7. containersmoke-test tegen `/health`;
8. dependency review bij pull requests.

## GitHub Pages

De statische projectpagina staat in `docs/` en wordt gepubliceerd via `.github/workflows/pages.yml`. Stel onder **Settings → Pages → Build and deployment** de bron in op **GitHub Actions**.

## Externe productiegates

De openstaande externe acceptatiepunten worden bijgehouden in issue **#1**. De repository claimt niet dat deze externe controles al zijn uitgevoerd.

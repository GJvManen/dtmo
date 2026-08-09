# DTMO

**Dutch Threat Monitoring for Education**

DTMO is een open, onderwijsgericht Cyber Threat Intelligence-platform voor historische incidenten, actuele intelligence, kwetsbaarheden, IOC's, leveranciersrisico en bestuurlijke rapportage.

## Actuele implementatiestatus

DTMO bevindt zich in **Phase 5 — performance en schaalbaarheid** van de productie-roadmap.

### Afgerond en evidenced

- Phase 1 — CI en workflow-integriteit: `PASS`;
- Phase 2 — applicatiebeveiliging en identity: `PASS`;
- Phase 3 — data-integriteit, backup en recovery: `PASS`;
- Phase 4 — live connectorbetrouwbaarheid en provenance: `PASS`;
- RC8.1 performance workload profile: `PASS`;
- RC8.2 API-read performance: `PASS`;
- RC8.3 OpenSearch search-read performance: `PASS`;
- RC8.4 ingestion-throughput performance: `PASS`;
- RC8.5 queue pressure en connector burst: `PASS` via RUN-20260809-083 / PR #42;
- Apache-2.0/open-source-governance baseline: `PASS` via RUN-20260809-080 / PR #44.

### Actieve roadmapstatus

Phase 5 blijft `IN PROGRESS`. RC8.5 is nu op `main`; de volgende nog niet geëvidenceerde interne Phase-5-gate is degraded-dependency correctness/performance. De onafhankelijke representative load/stress-gate in issue #1 blijft afzonderlijk open.

## Roadmapstatus

| Fase | Status |
|---|---|
| 1. CI en workflow-integriteit | `PASS` |
| 2. Applicatiebeveiliging en identity | `PASS` |
| 3. Data-integriteit, backup en recovery | `PASS` |
| 4. Live connectorbetrouwbaarheid en provenance | `PASS` |
| 5. Performance en schaalbaarheid | `IN PROGRESS` — RC8.1 t/m RC8.5 PASS; degraded-dependency gate open |
| 6. Frontend accessibility en operationele UX | `NOT ACCEPTED` |
| 7. Observability en incident operations | `NOT ACCEPTED` |
| 8. Staging acceptance | `NOT ACCEPTED` |
| 9. External assurance | `NOT ACCEPTED` |
| 10. Production go/no-go | `BLOCKED` |

## Architectuur, workflows en grafieken

De actuele runtime-, governance-, roadmap- en CI-grafieken staan in:

- `docs/project/CURRENT_STATE.md`

Op `main` zijn onder andere de volgende Phase-5-workflows aanwezig:

- `.github/workflows/api-read-performance.yml`;
- `.github/workflows/search-read-performance.yml`;
- `.github/workflows/ingestion-performance.yml`;
- `.github/workflows/queue-burst-performance.yml`;
- `.github/workflows/open-source-governance.yml`.

## Governance-invarianten

- ingestion maakt uitsluitend candidate intelligence;
- review en share approval blijven afzonderlijke menselijke beslissingen;
- dezelfde principal mag niet reviewen en share approval uitvoeren;
- serviceaccounts en connectors mogen niet reviewen of delen goedkeuren;
- connector-, replay-, retry-, timeout-, recovery- of performance-success mag nooit automatisch publiceren;
- raw evidence, provenance en confidence mogen niet stilzwijgend verdwijnen;
- ontbrekende, queued, cancelled of unexecuted CI-evidence blokkeert releaseacceptatie.

## Open-source licentie en projectgovernance

DTMO is gelicenseerd onder de **Apache License, Version 2.0** (`Apache-2.0`). De volledige voorwaarden staan in `LICENSE`; distributie-attributie staat in `NOTICE`.

Apache-2.0 geldt voor project-eigen broncode en documentatie tenzij expliciet anders vermeld. Externe dependencies, container images, API's, databronnen, dreigingsinformatie en trademarks behouden hun eigen licenties en gebruiksvoorwaarden en worden niet door DTMO opnieuw gelicenseerd.

Belangrijke governancebestanden:

- `LICENSE` — volledige Apache License 2.0;
- `NOTICE` — project- en distributienotices;
- `SECURITY.md` — responsible-disclosure- en securitybeleid;
- `CONTRIBUTING.md` — bijdrage-, evidence- en governancevereisten;
- `CODE_OF_CONDUCT.md` — samenwerkings- en gedragsregels;
- `SUPPORTED_VERSIONS.md` — security support policy;
- `docs/legal/LICENSING.md` — licentiebeleid en releasecontroles;
- `docs/legal/THIRD_PARTY.md` — third-party software/data/terms policy.

## Snel starten

```bash
git clone https://github.com/GJvManen/dtmo.git
cd dtmo
cp .env.example .env
docker compose up --build
```

Belangrijke endpoints:

- API: `http://localhost:8000`
- OpenAPI: `http://localhost:8000/docs`
- Health: `http://localhost:8000/health`
- Metrics: `http://localhost:8000/metrics`
- MinIO Console: `http://localhost:9001`
- Prometheus: `http://localhost:9090`

## Documentatie en evidence

- `docs/project/CURRENT_STATE.md`
- `docs/roadmap/PRODUCTION_ROADMAP.md`
- `docs/development/RUN_LOG.md`
- `docs/development/runs/`
- `docs/qa/`
- `docs/legal/LICENSING.md`
- `docs/legal/THIRD_PARTY.md`
- GitHub issues #1, #2 en #3

## Productiestatus

DTMO is nog niet productiegereed. Phase 5 is nog actief en Phases 6–10 plus resterende externe gates vereisen aanvullende objectieve evidence.

**Precies één volgende prioriteit:** implementeer één begrensde RC8.6 degraded-dependency performance/correctness gate die nul dataverlies en fail-closed governance bewijst wanneer een representatieve interne dependency unavailable of impaired is. Combineer dit niet met de externe load/stress-gate of Phase 6.

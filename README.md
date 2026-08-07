# DTMO

**Dutch Threat Monitoring for Education**

DTMO is een open, onderwijsgericht Cyber Threat Intelligence-platform voor historische incidenten, actuele intelligence, kwetsbaarheden, IOC's, leveranciersrisico en bestuurlijke rapportage.

## Actuele implementatiestatus

DTMO is ontwikkeld van RC4.1 tot en met RC7.2.

### Afgerond en evidenced

- RC4-platformbasis: API, persistence, immutable Intelligence Lake, connectorcatalogus, Knowledge Graph, SOC/CTI-workspace, RBAC, migraties, MinIO en OpenSearch;
- RC5.1 tot en met RC5.12 en Phase 2: `PASS`;
- RC6.1 tot en met RC6.4 en Phase 3: `PASS`;
- RC7.1 governed live connector canary: `PASS` via Canary Gate #3 en Quality Gate #270.

### Actieve run: RC7.2

**Persistent connector state and failure isolation: `CI_VALIDATION_PENDING`.**

De branch bevat:

- PostgreSQL-backed connector-runstate;
- append-only source-health history per connector en run-ID;
- connector-scoped failure isolation na een begrensde foutdrempel;
- automatische reset van isolatie na een succesvolle run;
- persistente quarantaine met raw-evidence SHA-256;
- human-reviewed recovery naar uitsluitend `released_to_candidate` of `rejected`;
- databaseconstraints die automatische publicatie uitsluiten;
- reversibele migratie `0005_connector_state`;
- onafhankelijke `RC7 Connector State Gate` met retained evidence en fail-closed aggregate gate.

RC7.2 wordt pas `PASS` nadat de exacte branch-head aantoonbaar groen is in zowel de reguliere Quality Gate als de Connector State Gate, met retained `connector-state-evidence`.

## Roadmapstatus

| Fase | Status |
|---|---|
| 1. CI en workflow-integriteit | `PASS` |
| 2. Applicatiebeveiliging, identity en privacy | `PASS` |
| 3. Data-integriteit, backup en recovery | `PASS` |
| 4. Live connectorbetrouwbaarheid en provenance | `IN PROGRESS` — RC7.2 wacht op exact-head evidence |
| 5. Performance en schaalbaarheid | `NOT STARTED` |
| 6. Frontend accessibility en operationele UX | `NOT STARTED` |
| 7. Observability en incident operations | `NOT STARTED` |
| 8. Staging acceptance | `NOT STARTED` |
| 9. External assurance | `NOT STARTED` |
| 10. Production go/no-go | `BLOCKED` |

**Precies één volgende prioriteit:** inspecteer de exacte RC7 Connector State Gate en herstel uitsluitend de eerste deterministische fout, of merge na volledige groene evidence.

## Governance-invarianten

- ingestion maakt uitsluitend candidate intelligence;
- review en share approval blijven afzonderlijke menselijke beslissingen;
- dezelfde principal mag niet reviewen en share approval uitvoeren;
- serviceaccounts en connectors mogen niet reviewen of delen goedkeuren;
- connector success of quarantine recovery mag nooit automatisch publiceren;
- raw evidence, provenance en confidence mogen niet stilzwijgend verdwijnen;
- ontbrekende CI-, recovery- of connector-evidence blokkeert releaseacceptatie.

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

- `docs/roadmap/PRODUCTION_ROADMAP.md`
- `docs/development/RUN_LOG.md`
- `docs/development/runs/RUN-20260806-045.md`
- `docs/qa/QA_AND_RELEASE_GATES.md`
- GitHub issues #2 en #3

## Productiestatus

DTMO is nog niet productiegereed. Productie blijft geblokkeerd totdat Phase 4 volledig is afgerond en performance, accessibility, observability, staging en externe assurance aantoonbaar zijn afgerond.

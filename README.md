# DTMO

**Dutch Threat Monitoring for Education**

DTMO is een open, onderwijsgericht Cyber Threat Intelligence-platform voor historische incidenten, actuele intelligence, kwetsbaarheden, IOC's, leveranciersrisico en bestuurlijke rapportage.

## Actuele implementatiestatus

DTMO is ontwikkeld van RC4.1 tot en met RC7.1.

### Afgerond en evidenced

- RC4-platformbasis: API, persistence, immutable Intelligence Lake, connectorcatalogus, Knowledge Graph, SOC/CTI-workspace, RBAC, migraties, MinIO en OpenSearch;
- RC5.1 tot en met RC5.12: canonieke intelligence, least-privilege RBAC, functiescheiding, trusted JWT-principals, JWKS-keyrotatie, revocation/replaybescherming, tamper-evidente persistente auditing, privacy-minimalisatie, retention, legal hold en bounded purge;
- Phase 2 — application security, identity en privacy: `PASS`;
- RC6.1 — clean-target PostgreSQL backup en restore: `PASS` via Quality Gate #229 en PR #22;
- RC6.2 — geïsoleerde MinIO objectbackup en clean-target restore: `PASS` via Quality Gate #243 en PR #24;
- RC6.3 — clean OpenSearch reconstruction: `PASS` via OpenSearch Recovery Gate #5, RC4 Quality Gate #253 en PR #25;
- RC6.4 — gecombineerde multi-store recovery acceptance: `PASS` via Multi-store Recovery Gate #4, RC4 Quality Gate #262, OpenSearch Recovery Gate #14 en PR #26;
- Phase 3 — data-integriteit, backup en recovery: `PASS`.

### Actieve run: RC7.1

**Governed live connector canary: `CI_VALIDATION_PENDING`.**

De branch bevat:

- een gecontroleerde CISA KEV live canary op een HTTPS-bron;
- verplichte licence- en terms-metadata;
- expliciete timeout en maximaal drie pogingen;
- begrensde exponentiële retry/backoff en minimum request interval;
- deduplicatie en quarantaine van malformed en duplicate records;
- behoud van source URL, timestamp, confidence en raw-evidence SHA-256;
- machine-readable retained canary evidence;
- `publish_approved: false` als fail-closed invariant;
- een onafhankelijke `always()` canarygate die ontbrekende of gefaalde evidence blokkeert.

RC7.1 wordt pas `PASS` nadat de exacte branch-head aantoonbaar groen is in zowel de reguliere Quality Gate als `RC7 Live Connector Canary Gate`, met retained `live-connector-canary-evidence`.

## Roadmapstatus

| Fase | Status |
|---|---|
| 1. CI en workflow-integriteit | `PASS` |
| 2. Applicatiebeveiliging, identity en privacy | `PASS` |
| 3. Data-integriteit, backup en recovery | `PASS` |
| 4. Live connectorbetrouwbaarheid en provenance | `IN PROGRESS` — RC7.1 wacht op exact-head live-canary evidence |
| 5. Performance en schaalbaarheid | `NOT STARTED` |
| 6. Frontend accessibility en operationele UX | `NOT STARTED` |
| 7. Observability en incident operations | `NOT STARTED` |
| 8. Staging acceptance | `NOT STARTED` |
| 9. External assurance | `NOT STARTED` |
| 10. Production go/no-go | `BLOCKED` |

**Precies één volgende prioriteit:** inspecteer de exacte RC7 Live Connector Canary Gate en herstel uitsluitend de eerste deterministische fout, of merge na volledige groene evidence.

## Governance-invarianten

- ingestion maakt uitsluitend candidate intelligence;
- review en share approval blijven afzonderlijke menselijke beslissingen;
- dezelfde principal mag niet reviewen en share approval uitvoeren;
- serviceaccounts en connectors mogen niet reviewen of delen goedkeuren;
- live canary-ingestion mag nooit automatisch publiceren;
- raw evidence, provenance en confidence mogen niet stilzwijgend verdwijnen;
- immutable bronauditrecords mogen niet door privacy-purge worden verwijderd;
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
- `docs/development/runs/RUN-20260806-040.md`
- `docs/development/runs/RUN-20260806-041.md`
- `docs/development/runs/RUN-20260806-042.md`
- `docs/development/runs/RUN-20260806-043.md`
- `docs/development/runs/RUN-20260806-044.md`
- `docs/qa/QA_AND_RELEASE_GATES.md`
- GitHub issues #2 en #3

## Productiestatus

DTMO is nog niet productiegereed. Productie blijft geblokkeerd totdat connectorreliability, performance, accessibility, observability, staging en externe assurance aantoonbaar zijn afgerond.

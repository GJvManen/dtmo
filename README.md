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
- Phase 3 — data-integriteit, backup en recovery: `PASS`;
- RC7.1 — governed live connector canary: `PASS` via RC7 Live Connector Canary Gate #3, RC4 Quality Gate #270, OpenSearch Recovery Gate #22 en Multi-store Recovery Gate #12;
- PR #28 is gemerged als `aeeb0709a26ecb1f20620d7ac21f823fec35e98f`.

### RC7.1 evidence

Exacte head `c82e20c110354c1163b58ac8b9820756f829a4ae` is volledig groen. De evidence omvat:

- gecontroleerde CISA KEV live canary via HTTPS;
- verplichte licence- en terms-metadata;
- expliciete timeout, maximaal drie pogingen en begrensde exponentiële retry/backoff;
- minimum request interval en uitgeschakelde redirects;
- deduplicatie en quarantaine van malformed, duplicate en overflow-records;
- behoud van source URL, timestamp, confidence en raw-evidence SHA-256;
- machine-readable retained canary evidence;
- `publish_approved: false` als harde fail-closed invariant;
- retained `live-connector-canary-evidence` artifact `8973407243`, digest `sha256:437b09bf13746fecf4e929921e1a63ac74bdbba1f1ecb08e0d04b99f763a3f53`.

## Roadmapstatus

| Fase | Status |
|---|---|
| 1. CI en workflow-integriteit | `PASS` |
| 2. Applicatiebeveiliging, identity en privacy | `PASS` |
| 3. Data-integriteit, backup en recovery | `PASS` |
| 4. Live connectorbetrouwbaarheid en provenance | `IN PROGRESS` — eerste governed live canary bewezen |
| 5. Performance en schaalbaarheid | `NOT STARTED` |
| 6. Frontend accessibility en operationele UX | `NOT STARTED` |
| 7. Observability en incident operations | `NOT STARTED` |
| 8. Staging acceptance | `NOT STARTED` |
| 9. External assurance | `NOT STARTED` |
| 10. Production go/no-go | `BLOCKED` |

**Precies één volgende prioriteit:** RC7.2 — persistente connector-runstate, source-health history en failure isolation met aantoonbare quarantine/recovery zonder automatische publicatie.

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

DTMO is nog niet productiegereed. Productie blijft geblokkeerd totdat Phase 4 volledig is afgerond en performance, accessibility, observability, staging en externe assurance aantoonbaar zijn afgerond.

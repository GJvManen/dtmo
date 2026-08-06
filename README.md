# DTMO

**Dutch Threat Monitoring for Education**

DTMO is een open, onderwijsgericht Cyber Threat Intelligence-platform voor historische incidenten, actuele intelligence, kwetsbaarheden, IOC's, leveranciersrisico en bestuurlijke rapportage.

## Actuele implementatiestatus

DTMO is ontwikkeld van RC4.1 tot en met RC6.3.

### Afgerond en evidenced

- RC4-platformbasis: API, persistence, immutable Intelligence Lake, connectorcatalogus, Knowledge Graph, SOC/CTI-workspace, RBAC, migraties, MinIO en OpenSearch;
- RC5.1 tot en met RC5.12: canonieke intelligence, least-privilege RBAC, functiescheiding, trusted JWT-principals, JWKS-keyrotatie, revocation/replaybescherming, tamper-evidente persistente auditing, privacy-minimalisatie, retention, legal hold en bounded purge;
- Phase 2 — application security, identity en privacy: `PASS`;
- RC6.1 — clean-target PostgreSQL backup en restore: `PASS` via Quality Gate #229 en PR #22;
- RC6.2 — geïsoleerde MinIO objectbackup en clean-target restore: `PASS` via Quality Gate #243 en PR #24;
- RC6.3 — clean OpenSearch reconstruction vanuit canonieke PostgreSQL-data met strikte provenance-mapping en deterministische manifestverificatie: `PASS` via OpenSearch Recovery Gate #5, RC4 Quality Gate #253 en PR #25.

### RC6.3 evidence

Exacte head `fbe3924d202d81ab59ebbcd10889a9a75b146941` is volledig groen. De evidence omvat:

- een niet-bestaande target-index vóór reconstructie;
- expliciete root- en provenance-submapping met `dynamic: strict`;
- behoud van content hashes, review/share-status en provenance-references;
- deterministische bron- en targetmanifesten met identieke SHA-256;
- exacte documentaantalcontrole;
- gemeten reconstructieduur en quiesced-source RPO-basis;
- retained `opensearch-reconstruction-evidence` artifact `8971961873`;
- fail-closed recoverygate en volledige aggregate Quality Gate.

PR #25 is gemerged naar `main` als `4b08640e612801898307b065f7f2413c34a090c2`.

## Roadmapstatus

| Fase | Status |
|---|---|
| 1. CI en workflow-integriteit | `PASS` |
| 2. Applicatiebeveiliging, identity en privacy | `PASS` |
| 3. Data-integriteit, backup en recovery | `IN PROGRESS` — PostgreSQL, MinIO en OpenSearch afzonderlijk bewezen; gecombineerde multi-store recovery acceptance ontbreekt nog |
| 4. Live connectorbetrouwbaarheid en provenance | `NOT STARTED` |
| 5. Performance en schaalbaarheid | `NOT STARTED` |
| 6. Frontend accessibility en operationele UX | `NOT STARTED` |
| 7. Observability en incident operations | `NOT STARTED` |
| 8. Staging acceptance | `NOT STARTED` |
| 9. External assurance | `NOT STARTED` |
| 10. Production go/no-go | `BLOCKED` |

**Precies één volgende prioriteit:** gecombineerde multi-store recovery acceptance voor PostgreSQL, MinIO en OpenSearch met één consistente recovery point, cross-store provenance-integriteit en gemeten end-to-end RTO/RPO.

## Governance-invarianten

- ingestion maakt uitsluitend candidate intelligence;
- review en share approval blijven afzonderlijke menselijke beslissingen;
- dezelfde principal mag niet reviewen en share approval uitvoeren;
- serviceaccounts mogen niet reviewen, delen goedkeuren of tokens intrekken;
- raw evidence, provenance en confidence mogen niet stilzwijgend verdwijnen;
- immutable bronauditrecords mogen niet door privacy-purge worden verwijderd;
- ontbrekende CI-, backup-, reconstructie- of restore-evidence blokkeert releaseacceptatie.

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
- `docs/qa/QA_AND_RELEASE_GATES.md`
- GitHub issues #2 en #3

## Productiestatus

DTMO is nog niet productiegereed. Productie blijft geblokkeerd totdat recovery, connectorreliability, performance, accessibility, observability, staging en externe assurance aantoonbaar zijn afgerond.

# DTMO

**Dutch Threat Monitoring for Education**

DTMO is een open, onderwijsgericht Cyber Threat Intelligence-platform voor historische incidenten, actuele intelligence, kwetsbaarheden, IOC's, leveranciersrisico en bestuurlijke rapportage.

## Actuele implementatiestatus

DTMO is ontwikkeld van RC4.1 tot en met RC6.4.

### Afgerond en evidenced

- RC4-platformbasis: API, persistence, immutable Intelligence Lake, connectorcatalogus, Knowledge Graph, SOC/CTI-workspace, RBAC, migraties, MinIO en OpenSearch;
- RC5.1 tot en met RC5.12: canonieke intelligence, least-privilege RBAC, functiescheiding, trusted JWT-principals, JWKS-keyrotatie, revocation/replaybescherming, tamper-evidente persistente auditing, privacy-minimalisatie, retention, legal hold en bounded purge;
- Phase 2 — application security, identity en privacy: `PASS`;
- RC6.1 — clean-target PostgreSQL backup en restore: `PASS` via Quality Gate #229 en PR #22;
- RC6.2 — geïsoleerde MinIO objectbackup en clean-target restore: `PASS` via Quality Gate #243 en PR #24;
- RC6.3 — clean OpenSearch reconstruction vanuit canonieke PostgreSQL-data: `PASS` via OpenSearch Recovery Gate #5, RC4 Quality Gate #253 en PR #25.

### Actieve run: RC6.4

**Combined multi-store recovery acceptance: `CI_VALIDATION_PENDING`.**

De branch bevat:

- één recovery-point-ID gebonden aan de exacte commit;
- clean-target recovery voor PostgreSQL, MinIO en OpenSearch in één workflow;
- verificatie van auditketen, provenance, objectdigests en source/targetmanifesten;
- deterministische SHA-256-binding over alle drie store-evidences;
- gemeten componenttijden, end-to-end RTO en effectieve maximale RPO;
- retained `multistore-recovery-evidence` met alle componentevidence;
- een afzonderlijke fail-closed recovery-acceptance gate;
- regressietests voor ontbrekende provenancecontrole en onbegrensde RPO.

RC6.4 wordt pas `PASS` nadat GitHub Actions op de exacte branch-head volledig groen is en het vereiste artifact aantoonbaar is retained.

## Roadmapstatus

| Fase | Status |
|---|---|
| 1. CI en workflow-integriteit | `PASS` |
| 2. Applicatiebeveiliging, identity en privacy | `PASS` |
| 3. Data-integriteit, backup en recovery | `IN PROGRESS` — afzonderlijke stores bewezen; gecombineerde RC6.4 acceptance wacht op exact-head evidence |
| 4. Live connectorbetrouwbaarheid en provenance | `NOT STARTED` |
| 5. Performance en schaalbaarheid | `NOT STARTED` |
| 6. Frontend accessibility en operationele UX | `NOT STARTED` |
| 7. Observability en incident operations | `NOT STARTED` |
| 8. Staging acceptance | `NOT STARTED` |
| 9. External assurance | `NOT STARTED` |
| 10. Production go/no-go | `BLOCKED` |

**Precies één volgende prioriteit:** inspecteer de exacte-head RC6 Multi-Store Recovery Gate en herstel uitsluitend de eerste deterministische fout, of merge na volledige groene evidence.

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
- `docs/development/runs/RUN-20260806-043.md`
- `docs/qa/QA_AND_RELEASE_GATES.md`
- GitHub issues #1, #2 en #3

## Productiestatus

DTMO is nog niet productiegereed. Productie blijft geblokkeerd totdat recovery, connectorreliability, performance, accessibility, observability, staging en externe assurance aantoonbaar zijn afgerond.

# DTMO

**Dutch Threat Monitoring for Education**

DTMO is een open, onderwijsgericht Cyber Threat Intelligence-platform voor historische incidenten, actuele intelligence, kwetsbaarheden, IOC's, leveranciersrisico en bestuurlijke rapportage.

## Actuele implementatiestatus — 2026-08-09

DTMO bevindt zich in **Phase 7 — observability en incident operations** van de productie-roadmap.

### Afgerond en evidenced

- Phase 1 — CI en workflow-integriteit: `PASS`;
- Phase 2 — applicatiebeveiliging en identity: `PASS` voor de interne roadmap-gates;
- Phase 3 — data-integriteit en recovery: `PASS` voor de interne roadmap-gates;
- Phase 4 — live connectorbetrouwbaarheid en provenance: `PASS` voor de interne roadmap-gates;
- Phase 5 — performance en schaalbaarheid: `PASS` voor de interne roadmap-gates;
- RC9.1–RC9.15 — browser/accessibility critical-journey evidence: geaccepteerd binnen de beschreven bounded scopes;
- RC10.1 — request observability: `PASS`;
- RC10.2 — controlled connector-failure alerting: `PASS`;
- RUN-20260809-126 — authoritative documentation reconciliation: `PASS` in de final merged state;
- Apache-2.0/open-source-governance baseline: `PASS`.

### Open en geblokkeerd

- Phase 6 — frontend accessibility en operationele UX: `BLOCKED_EXTERNAL` uitsluitend voor genuine VoiceOver/NVDA behavior op ondersteunde echte host/browser/screen-reader combinaties. Browser/DOM automation geldt niet als vervanging voor echte assistive-technology evidence.
- Phase 7 — observability en incident operations: `IN PROGRESS`.
- Phase 8 — staging acceptance: `NOT STARTED`.
- Phase 9 — external assurance: `NOT COMPLETE`.
- Phase 10 — production go/no-go: `NOT STARTED`.
- Issue #1 blijft de source of truth voor de resterende externe productieacceptatie-gates.

## Laatste Phase-7 evidence

### RC10.1 — request observability

PR #80 exact head `01a175e12da7c8af8566178a2d7e6b34a57d58bc` passeerde 34/34 workflows. Retained artifact `9040196394` (`sha256:6792020994d94b0484cb84140d202433303eceb82565f8598ffd5937940531d6`) bewijst safe correlation-ID handling, structured request-log context, bounded route-template metrics, latency en in-flight metrics. JUnit: 5/5. Merge: `1675d88bb24dcd50e20545f49b26dd7cc2810d97`.

### RC10.2 — connector-failure alerting

PR #82 exact head `b38aeae44588e39e35339f4c4d9667947804b243` passeerde 35/35 workflows. Retained artifact `9040485255` (`sha256:96883158cfd790c3c6b21c2db819acbcbc03d431d4dd79bb32038b6ff258de25`) bewijst terminal failure signaling, Prometheus metric/rule, structured correlation evidence, actionable operator guidance, raw-error exclusion, repeat-raise suppression en recovery/clear behavior. JUnit: 4/4. Merge: `f6680423860389288d9feced34592294d774bf4a`.

RC10.2 configureert of certificeert geen pager/e-mail/chat delivery. Queue-, storage-, API-error- en search-health alerting blijven afzonderlijke Phase-7 objectives.

## Roadmapstatus

| Fase | Status |
|---|---|
| 1. CI en workflow-integriteit | `PASS` |
| 2. Applicatiebeveiliging en identity | `PASS` intern |
| 3. Data-integriteit en recovery | `PASS` intern |
| 4. Connectorbetrouwbaarheid en provenance | `PASS` intern |
| 5. Performance en schaalbaarheid | `PASS` intern |
| 6. Frontend accessibility en operationele UX | `BLOCKED_EXTERNAL` — genuine VoiceOver/NVDA evidence open |
| 7. Observability en incident operations | `IN PROGRESS` — RC10.1 en RC10.2 PASS |
| 8. Staging acceptance | `NOT STARTED` |
| 9. External assurance | `NOT COMPLETE` |
| 10. Production go/no-go | `NOT STARTED` |

## Architectuur, workflows en grafieken

De actuele runtime-, governance-, roadmap- en CI-grafieken staan in `docs/project/CURRENT_STATE.md`.

Belangrijke observability-workflows op `main`:

- `.github/workflows/request-observability.yml`;
- `.github/workflows/connector-alerting.yml`.

De bestaande RC4/RC6/RC7/RC8/RC9 workflows blijven regressiebescherming leveren. De aanwezigheid van een workflow is geen PASS; exact-head uitvoering en retained evidence blijven vereist.

## Governance-invarianten

- ingestion maakt uitsluitend candidate intelligence;
- review en share approval blijven afzonderlijke menselijke beslissingen;
- dezelfde principal mag niet reviewen en share approval uitvoeren;
- serviceaccounts en connectors mogen niet reviewen of delen goedkeuren;
- connector-, replay-, retry-, timeout-, recovery-, performance- of observability-success mag nooit automatisch publiceren;
- raw evidence, provenance en confidence mogen niet stilzwijgend verdwijnen;
- ontbrekende, queued, cancelled, failed of unexecuted CI-evidence blokkeert de bijbehorende acceptatieclaim.

## Open-source licentie en projectgovernance

DTMO is gelicenseerd onder de **Apache License, Version 2.0** (`Apache-2.0`). Zie `LICENSE`, `NOTICE`, `SECURITY.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SUPPORTED_VERSIONS.md`, `docs/legal/LICENSING.md` en `docs/legal/THIRD_PARTY.md`.

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
- GitHub issues #1, #2 en #3

## Productiestatus

DTMO is nog niet productiegereed. Phase 6 heeft een expliciete externe assistive-technology blocker, Phase 7 is nog in uitvoering, en Phases 8–10 plus issue #1 vereisen aanvullende evidence.

**Precies één volgende prioriteit:** RC10.3 — bounded queue-backlog alerting met expliciete threshold semantics, actionable correlation evidence en controlled breach/recovery behavior. Storage-integrity, API-error en search-health alerting blijven latere Phase-7 objectives.

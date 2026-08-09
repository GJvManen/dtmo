# DTMO

**Dutch Threat Monitoring for Education**

DTMO is een open, onderwijsgericht Cyber Threat Intelligence-platform voor historische incidenten, actuele intelligence, kwetsbaarheden, IOC's, leveranciersrisico en bestuurlijke rapportage.

## Actuele implementatiestatus — 2026-08-09

DTMO bevindt zich in **Phase 7 — observability en incident operations** van de productie-roadmap.

### Afgerond en evidenced

- Phase 1–5: `PASS` voor de interne roadmap-gates;
- RC9.1–RC9.15: geaccepteerde bounded browser/accessibility critical-journey evidence;
- RC10.1 request observability: `PASS`;
- RC10.2 controlled connector-failure alerting: `PASS`;
- RC10.3 bounded queue-backlog alerting: `PASS`;
- RUN-20260809-128 documentation reconciliation: `PASS` only in the final protected merged state after final exact-head 36/36 validation;
- Apache-2.0/open-source-governance baseline: `PASS`.

### Open en geblokkeerd

- Phase 6: `BLOCKED_EXTERNAL` uitsluitend voor genuine VoiceOver/NVDA behavior op ondersteunde echte host/browser/screen-reader combinaties;
- Phase 7: `IN PROGRESS`;
- Phase 8: `NOT STARTED`;
- Phase 9: `NOT COMPLETE`;
- Phase 10: `NOT STARTED`;
- Issue #1 blijft de source of truth voor resterende externe productieacceptatie-gates.

## Laatste Phase-7 evidence

### RC10.1 — request observability
PR #80 exact head `01a175e12da7c8af8566178a2d7e6b34a57d58bc`; 34/34 workflows; artifact `9040196394` (`sha256:6792020994d94b0484cb84140d202433303eceb82565f8598ffd5937940531d6`); JUnit 5/5; merge `1675d88bb24dcd50e20545f49b26dd7cc2810d97`.

### RC10.2 — connector-failure alerting
PR #82 exact head `b38aeae44588e39e35339f4c4d9667947804b243`; 35/35 workflows; artifact `9040485255` (`sha256:96883158cfd790c3c6b21c2db819acbcbc03d431d4dd79bb32038b6ff258de25`); JUnit 4/4; merge `f6680423860389288d9feced34592294d774bf4a`.

### RC10.3 — queue-backlog alerting
PR #84 exact head `8058b476298eee4bcd2942d9cca54384ec12aa74`; 36/36 workflows; artifact `9040996591` (`sha256:42aaad1424d7c1ad40accd056b4746ea6fb328a561b24df5ebc293c0425b1910`); bounded queue metrics, 80% raise/50% clear hysteresis, correlated actionable evidence and RC8 queue-pressure reuse; JUnit 5/5; merge `42ccbe04cbc1081f93e4a155243627b5a3038573`.

RC10.2/RC10.3 configureren of certificeren geen pager/e-mail/chat delivery. RC10.3 claimt geen aparte deployed durable queue service. Storage-integrity, API-error en search-health alerting blijven afzonderlijke Phase-7 objectives.

## Roadmapstatus

| Fase | Status |
|---|---|
| 1–5 | `PASS` intern |
| 6. Frontend accessibility en operationele UX | `BLOCKED_EXTERNAL` — genuine VoiceOver/NVDA evidence open |
| 7. Observability en incident operations | `IN PROGRESS` — RC10.1, RC10.2 en RC10.3 PASS |
| 8. Staging acceptance | `NOT STARTED` |
| 9. External assurance | `NOT COMPLETE` |
| 10. Production go/no-go | `NOT STARTED` |

## Architectuur, workflows en grafieken

Zie `docs/project/CURRENT_STATE.md` voor actuele runtime-, governance-, roadmap- en CI-grafieken.

Belangrijke observability-workflows:
- `.github/workflows/request-observability.yml`;
- `.github/workflows/connector-alerting.yml`;
- `.github/workflows/queue-backlog-alerting.yml`.

Workflow presence is not PASS: exact-head uitvoering en retained evidence blijven vereist.

## Governance-invarianten

- ingestion maakt uitsluitend candidate intelligence;
- review en share approval blijven afzonderlijke menselijke beslissingen;
- dezelfde principal mag niet reviewen en share approval uitvoeren;
- serviceaccounts en connectors mogen niet reviewen of delen goedkeuren;
- connector-, queue-, replay-, retry-, timeout-, recovery-, performance- of observability-success mag nooit automatisch publiceren;
- raw evidence, provenance en confidence mogen niet stilzwijgend verdwijnen;
- ontbrekende, queued, cancelled, failed of unexecuted CI-evidence blokkeert de bijbehorende acceptatieclaim.

## Open-source licentie en projectgovernance

DTMO is Apache-2.0 gelicenseerd. Zie `LICENSE`, `NOTICE`, `SECURITY.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SUPPORTED_VERSIONS.md`, `docs/legal/LICENSING.md` en `docs/legal/THIRD_PARTY.md`.

## Snel starten

```bash
git clone https://github.com/GJvManen/dtmo.git
cd dtmo
cp .env.example .env
docker compose up --build
```

Belangrijke endpoints: API `:8000`, OpenAPI `/docs`, Health `/health`, Metrics `/metrics`, MinIO Console `:9001`, Prometheus `:9090`.

## Productiestatus

DTMO is nog niet productiegereed. Phase 6 heeft een expliciete externe assistive-technology blocker, Phase 7 is nog in uitvoering, en Phases 8–10 plus issue #1 vereisen aanvullende evidence.

**Precies één volgende prioriteit:** RC10.4 — bounded storage-integrity alerting met controlled integrity-failure/recovery evidence, actionable correlation, geen raw sensitive payload leakage en retained exact-head evidence. API-error en search-health alerting blijven latere Phase-7 objectives.

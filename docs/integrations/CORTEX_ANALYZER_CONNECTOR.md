# Cortex Analyzer Connector

State: **`IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`**

DTMO now contains a bounded analyzer-only Cortex adapter in `backend/dtmo/integrations/cortex.py`.

## Configuration

- `DTMO_CORTEX_API_BASE`
- `DTMO_CORTEX_API_TOKEN`
- `DTMO_CORTEX_ALLOWED_OBSERVABLE_TYPES`
- `DTMO_CORTEX_ALLOWED_ANALYZERS`
- `DTMO_CORTEX_WAIT_SECONDS`
- `DTMO_CORTEX_MAX_RESULT_BYTES`
- `DTMO_FEATURE_CORTEX_ANALYSIS`

The feature is disabled by default. Production configuration requires HTTPS, a non-empty runtime API token and an explicit analyzer allowlist.

## Runtime path

1. Validate observable datatype, value, analyzer ID and TLP before network I/O.
2. Submit to `POST /api/analyzer/{ANALYZER_ID}/run` using `Authorization: Bearer ...`.
3. Require a stable Cortex job ID.
4. Retrieve the bounded result from `GET /api/job/{JOB_ID}/waitreport`.
5. Require stable job identity and matching analyzer identity when returned.
6. Mark imported report metadata `external_share_authorized=false` and `local_compromise_proven=false`.

Responders, files/attachments, Cortex administration, automatic analyzer discovery, automatic fallback from IntelOwl and external side-effect actions are outside this slice.

## Handling

The connector accepts explicit Cortex TLP values 0 through 3. Source restrictions remain authoritative; callers must not use this adapter to downgrade a stricter upstream handling policy. Personal-data observable classes are intentionally excluded from the bounded baseline.

Repository CI is synthetic engineering evidence only and does not prove live Cortex/provider authorization.

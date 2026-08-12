# DTMO Analytics Trends

Status: `IMPLEMENTED_PENDING_CI`

## Purpose

E4 extends the canonical DTMO console with severity-aware trend analysis without turning visualisation into an inferred risk decision.

## Product behaviour

The Overview and Visual analytics views expose the same selectable trend state:

- 24 hours, bucketed per hour;
- 7 days, bucketed per rolling day;
- 30 days, bucketed per rolling day.

The active shared severity filter from E1/E2 is applied to the trend endpoint and therefore to both visual surfaces.

## Statistics

Each window reports:

- current-period intelligence volume;
- immediately preceding equal-period volume;
- absolute volume delta;
- percentage volume change where a valid non-zero baseline exists;
- current and previous high/critical count;
- current and previous high/critical share;
- high/critical share change in percentage points.

A zero previous-period baseline does not produce an invented percentage increase. The API returns `null` for percentage volume change when the current period is non-zero and the previous period is zero.

## Visual model

Trend columns are stacked by the canonical DTMO severity model. Severity colour remains supplementary to textual labels and the table alternative:

- informational: grey;
- low: green;
- medium: orange;
- high: red;
- critical: distinct dark red.

The table exposes every bucket with total, per-severity counts and high/critical share.

## Governance boundary

DTMO deliberately separates volume change from severity-mix change. A larger number of records does not automatically mean higher risk, and this feature does not generate an autonomous risk score.

E4 does not create Normenkader IBP, MITRE ATT&CK, CVSS, NIST CSF or other framework mappings. Framework mappings remain explicit, provenance-backed governance data and are delivered in the E5/E7 slice.

## API

`GET /api/v1/console/trends`

Query parameters:

- `window=24h|7d|30d`;
- repeatable `severity=informational|low|medium|high|critical`.

Unknown window values fail FastAPI validation. Unknown severity values fail closed through the E1/E2 canonical severity parser.

## QA

Repository-controlled validation is defined in `.github/workflows/e4-analytics-trends.yml` and includes the dedicated trend calculation/UI tests plus preserved E1/E2 and RC13 console contracts.

## Dependency

This is a stacked enhancement on E1/E2. Until PR #175 is merged, the E4 pull request targets `enhancement/e1-e2-severity-experience`. After #175 is accepted, E4 can be retargeted to `main` and must receive fresh exact-head CI evidence before merge.

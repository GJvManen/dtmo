# DTMO Installation Guide

## Purpose and support boundary

This is the single authoritative installation guide for the DTMO repository-controlled local/reference deployment. It covers prerequisites, clean startup, generated local credentials, external licensed prerequisites, service entry points, first administration checks, first-data workflow, health verification and troubleshooting.

DTMO remains **not production authorized**. A successful local installation is installation evidence only; it is not staging acceptance, it is not production-equivalent validation, it is not penetration-test evidence, and it is not independent assurance or production authorization.

## 1. Prerequisites

Required:

- Git;
- Python 3.12 or newer for the bootstrap helper;
- Docker Desktop or Docker Engine with Docker Compose v2;
- sufficient local resources for PostgreSQL, Redis, OpenSearch, AIStor-compatible object storage, Prometheus, Grafana and the DTMO API;
- a vendor-supported AIStor image reference pinned by digest;
- a valid AIStor license file available outside the repository.

External CTI platforms such as MISP, AIL, Taranis AI, IntelOwl, Cortex, OpenCTI and TheHive are separate governed service boundaries. They are **not** blindly enabled by the default installation. Configure them only when endpoint identity, required credentials, allowlists/scopes and organizational approval are available.

## 2. Clean checkout

For a clean installation or owner retest, use a new directory and record the exact Git commit being evaluated.

```bash
git clone https://github.com/GJvManen/dtmo.git
cd dtmo
git rev-parse HEAD
```

Do not copy a previous `.env`, database volume, object-store volume or browser state into a clean-install acceptance run.

## 3. Prepare local configuration

Run the supported bootstrap helper:

```bash
python3 tools/bootstrap_local.py
```

The helper:

- verifies Docker is installed and the daemon is running;
- starts from `.env.example` when no `.env` exists;
- generates development-only values for OpenSearch, Grafana and local object-store credentials where safe;
- keeps PostgreSQL credentials internally consistent;
- writes `.env` with restrictive permissions where supported;
- validates `docker compose config`;
- fails closed when required external AIStor image/license inputs are not real and usable.

The helper does **not** manufacture external licenses, production credentials or upstream service authorization.

### AIStor image

Set `AISTOR_IMAGE` in `.env` to a vendor-supported image reference, preferably pinned by SHA-256 digest. Placeholder values from `.env.example` are documentation only and intentionally fail preflight.

### AIStor license

Set `AISTOR_LICENSE_FILE` to a valid local license file outside source control. If a valid file is intentionally placed at repository root as `AISTOR_LICENSE_FILE`, the bootstrap helper can resolve that local path. Never commit the license or copy it into test evidence.

## 4. Start DTMO

After bootstrap reports `Local preflight PASS`:

```bash
docker compose up --build
```

The reference topology starts migration, Grafana reporting-role provisioning and the following runtime services:

- DTMO API/workbench;
- PostgreSQL;
- Redis;
- OpenSearch;
- AIStor-compatible object storage;
- Prometheus;
- Grafana;
- NGINX gateway.

Schema migration must complete before the API is considered ready. Grafana's reporting role is deliberately read-only and does not receive direct access to unrestricted application tables.

## 5. Service entry points

Default local ports from `docker-compose.yml` are:

| Service | Local entry point | Purpose |
| --- | --- | --- |
| DTMO API/workbench | `http://localhost:8000/` | Direct DTMO application/API access. |
| Unified gateway | `http://localhost:8080/` | Supported combined DTMO/Grafana gateway path. |
| Grafana | `http://localhost:3000/` | Direct Grafana administrative/debug access. |
| Prometheus | `http://localhost:9090/` | Direct Prometheus operational/debug access. |
| AIStor console | `http://localhost:9001/` | Local object-store administration. |

Prefer the supported product/gateway path for normal operator use. Direct infrastructure ports are administrative/debug surfaces and do not grant DTMO application authority.

## 6. First health checks

Confirm container state:

```bash
docker compose ps
```

Then verify DTMO health:

```bash
curl --fail http://localhost:8000/health
```

If the gateway is being used, open `http://localhost:8080/` in the browser and confirm the canonical workbench loads without requiring a `/ui/*` legacy-primary path.

In the application, Operations should distinguish configured capability from attributable runtime evidence. Missing telemetry or unavailable dependencies must remain unavailable/degraded rather than becoming synthetic zero/healthy claims.

## 7. First administration workflow

Open canonical Administration and verify:

1. integration readiness is visible;
2. bundled/core service state is understandable;
3. external integrations without complete configuration show actionable blockers;
4. credentials are never rendered back in plaintext;
5. a permitted configuration change survives page reload;
6. server-side RBAC remains authoritative regardless of which controls are visible in the browser.

Do not enable external integrations merely to remove a warning. Required endpoint identity, credentials, analyzer/entity allowlists and scopes must exist first.

## 8. First-data workflow

Use **Sources & Collection** in the canonical workbench. The supported operator sequence is:

1. inspect/bootstrap supported sources;
2. register or select an attributable source;
3. inspect validation/readiness;
4. activate only when configuration and authority allow it;
5. run the supported collection action;
6. inspect durable source/connector runtime state;
7. open the resulting canonical intelligence and verify source identity and provenance;
8. reload/revisit to confirm the result is persisted rather than transient UI state.

Repository-controlled sample/bootstrap content must remain visibly labelled. It is useful local data, not proof of live upstream truth.

## 9. External framework configuration

MISP, AIL, Taranis AI, IntelOwl, Cortex, OpenCTI and TheHive remain separate trust and deployment boundaries. Use canonical Administration and the integration-specific administrator/runbook documentation to configure them.

Security requirements remain non-negotiable:

- credentials stay server-side;
- least privilege applies to service identities;
- missing required state fails closed;
- external sharing/publication requires the applicable human authority;
- analyzer/entity allowlists and handling restrictions remain enforced;
- connector success does not prove upstream truth, compromise or remediation.

## 10. Stop and restart

Normal stop:

```bash
docker compose down
```

Normal restart while preserving named volumes:

```bash
docker compose up --build
```

Do not add `-v` when the purpose is to verify persistence. For a deliberately clean installation, remove prior volumes explicitly only after confirming no evidence or data must be retained.

## 11. Troubleshooting

### Bootstrap says Docker is unavailable

Install/start Docker Desktop or Docker Engine and retry after `docker info` succeeds.

### Bootstrap stops on `AISTOR_IMAGE`

Replace the placeholder with a real vendor-supported image identity. Do not bypass this check with an invented digest.

### Bootstrap cannot find the AIStor license

Set `AISTOR_LICENSE_FILE` to the actual local file. Keep the license outside source control.

### `docker compose config` fails

Resolve the exact missing/invalid environment value printed by Compose. Do not replace required secrets or license values with repository placeholders.

### API does not become healthy

Inspect:

```bash
docker compose ps
docker compose logs migrate
docker compose logs api
docker compose logs postgres
docker compose logs redis
docker compose logs opensearch
docker compose logs minio
```

Fix the concrete dependency or migration failure before continuing. Do not treat an unhealthy dependency as an empty but successful application state.

### Grafana is not usable through the product path

Check `grafana-db-provision`, `grafana`, `prometheus` and `gateway` container logs. Grafana requires its generated/local administrative credentials and dedicated database-reader password. Anonymous access is disabled by design.

### External integration remains unavailable

Use Administration to inspect its readiness blockers. Confirm endpoint identity, credential presence and any required allowlists/scopes. Do not expose credentials in screenshots, issue comments or repository evidence.

## 12. Clean-install owner retest

After the repository-controlled installation itself is healthy, use `docs/operations/CLEAN_INSTALL_OWNER_RETEST_RUNBOOK.md` for the full whole-product owner functional retest. Candidate freeze remains blocked until that external retest is explicitly accepted.

A green repository CI run or successful installation cannot substitute for that owner decision or for later production-equivalent and independent-assurance evidence.
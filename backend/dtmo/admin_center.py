from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, SecretStr

from dtmo.auth.dependencies import require_permission
from dtmo.auth.policy import Permission, Principal
from dtmo.config import get_settings
from dtmo.integration_readiness import integration_readiness

router = APIRouter()
settings = get_settings()
_DEFAULT_RUNTIME_DIRECTORY = Path("/var/lib/dtmo") if settings.environment in {"staging", "production"} else Path(".dtmo/runtime")
_RUNTIME_DIRECTORY = Path(os.environ.get("DTMO_RUNTIME_INTEGRATION_DIR", str(_DEFAULT_RUNTIME_DIRECTORY)))
_RUNTIME_CONFIG_PATH = _RUNTIME_DIRECTORY / "runtime-integration-settings.json"
_RUNTIME_SECRET_PATH = _RUNTIME_DIRECTORY / "runtime-integration-secrets.json"

_INTEGRATIONS = {
    "misp": ("MISP", "feature_misp_connector", "misp_api_base", "misp_api_key"),
    "ail": ("AIL", "feature_ail_connector", "ail_api_base", "ail_api_key"),
    "taranis": ("Taranis AI", "feature_taranis_connector", "taranis_api_base", "taranis_api_token"),
    "intelowl": ("IntelOwl", "feature_intelowl_enrichment", "intelowl_api_base", "intelowl_api_token"),
    "cortex": ("Cortex", "feature_cortex_analysis", "cortex_api_base", "cortex_api_token"),
    "opencti": ("OpenCTI", "feature_opencti_read", "opencti_api_base", "opencti_api_token"),
    "thehive": ("TheHive", "feature_thehive_handoff", "thehive_api_base", "thehive_api_token"),
}


class IntegrationPatch(BaseModel):
    enabled: bool | None = None
    api_base: str | None = None
    credential: SecretStr | None = None
    ail_object_global_ids: str | None = None
    intelowl_allowed_analyzers: str | None = None
    cortex_allowed_analyzers: str | None = None
    opencti_allowed_entity_types: str | None = None
    opencti_checkpoint_path: str | None = None
    thehive_organization: str | None = None


def _secret_present(value: object) -> bool:
    getter = getattr(value, "get_secret_value", None)
    raw = getter() if callable(getter) else value
    return bool(str(raw or "").strip())


def _read_json_object(path: Path) -> dict[str, object]:
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, OSError, json.JSONDecodeError):
        return {}
    return document if isinstance(document, dict) else {}


def _normalize_csv(value: str) -> str:
    return ",".join(item.strip() for item in value.split(",") if item.strip())


def _apply_persisted_runtime_configuration() -> None:
    document = _read_json_object(_RUNTIME_CONFIG_PATH)
    for integration_id, values in document.items():
        spec = _INTEGRATIONS.get(integration_id)
        if spec is None or not isinstance(values, dict):
            continue
        _, enabled_attr, api_attr, _ = spec
        if isinstance(values.get("enabled"), bool):
            setattr(settings, enabled_attr, values["enabled"])
        if isinstance(values.get("api_base"), str):
            setattr(settings, api_attr, values["api_base"].strip())
        if integration_id == "ail" and isinstance(values.get("ail_object_global_ids"), str):
            settings.ail_object_global_ids = _normalize_csv(values["ail_object_global_ids"])
        if integration_id == "intelowl" and isinstance(values.get("intelowl_allowed_analyzers"), str):
            settings.intelowl_allowed_analyzers = _normalize_csv(values["intelowl_allowed_analyzers"])
        if integration_id == "cortex" and isinstance(values.get("cortex_allowed_analyzers"), str):
            settings.cortex_allowed_analyzers = _normalize_csv(values["cortex_allowed_analyzers"])
        if integration_id == "opencti":
            if isinstance(values.get("opencti_allowed_entity_types"), str):
                settings.opencti_allowed_entity_types = _normalize_csv(values["opencti_allowed_entity_types"])
            if isinstance(values.get("opencti_checkpoint_path"), str):
                settings.opencti_checkpoint_path = values["opencti_checkpoint_path"].strip()
        if integration_id == "thehive" and isinstance(values.get("thehive_organization"), str):
            settings.thehive_organization = values["thehive_organization"].strip()

    secrets = _read_json_object(_RUNTIME_SECRET_PATH)
    for integration_id, value in secrets.items():
        spec = _INTEGRATIONS.get(integration_id)
        if spec is None or not isinstance(value, str) or not value.strip():
            continue
        _, _, _, secret_attr = spec
        setattr(settings, secret_attr, SecretStr(value))


def _persist_runtime_configuration() -> None:
    document: dict[str, dict[str, object]] = {}
    for integration_id, (_, enabled_attr, api_attr, _) in _INTEGRATIONS.items():
        values: dict[str, object] = {
            "enabled": bool(getattr(settings, enabled_attr)),
            "api_base": str(getattr(settings, api_attr)),
        }
        if integration_id == "ail":
            values["ail_object_global_ids"] = settings.ail_object_global_ids
        if integration_id == "intelowl":
            values["intelowl_allowed_analyzers"] = settings.intelowl_allowed_analyzers
        if integration_id == "cortex":
            values["cortex_allowed_analyzers"] = settings.cortex_allowed_analyzers
        if integration_id == "opencti":
            values["opencti_allowed_entity_types"] = settings.opencti_allowed_entity_types
            values["opencti_checkpoint_path"] = settings.opencti_checkpoint_path
        if integration_id == "thehive":
            values["thehive_organization"] = settings.thehive_organization
        document[integration_id] = values
    try:
        _RUNTIME_CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        temporary = _RUNTIME_CONFIG_PATH.with_suffix(".tmp")
        temporary.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        temporary.replace(_RUNTIME_CONFIG_PATH)
    except OSError as exc:
        raise HTTPException(status_code=503, detail=f"runtime configuration could not be persisted: {exc}") from exc


def _persist_runtime_credential(integration_id: str, credential: str) -> None:
    document = _read_json_object(_RUNTIME_SECRET_PATH)
    document[integration_id] = credential
    try:
        _RUNTIME_SECRET_PATH.parent.mkdir(parents=True, exist_ok=True)
        temporary = _RUNTIME_SECRET_PATH.with_suffix(".tmp")
        temporary.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        temporary.chmod(0o600)
        temporary.replace(_RUNTIME_SECRET_PATH)
        _RUNTIME_SECRET_PATH.chmod(0o600)
    except OSError as exc:
        raise HTTPException(status_code=503, detail="runtime credential could not be persisted") from exc


def _integration_row(integration_id: str) -> dict[str, object]:
    name, enabled_attr, api_attr, secret_attr = _INTEGRATIONS[integration_id]
    enabled = bool(getattr(settings, enabled_attr))
    api_base = str(getattr(settings, api_attr)).strip()
    credential_configured = _secret_present(getattr(settings, secret_attr))
    activation_blockers: list[str] = []
    if enabled and api_base and credential_configured:
        state = "ready"
    elif enabled and api_base:
        state = "credential-required"
    elif enabled:
        state = "configuration-required"
    else:
        state = "disabled"

    if integration_id in {"ail", "intelowl", "cortex", "opencti", "thehive"}:
        readiness = next(row for row in integration_readiness(settings) if row.id == integration_id)
        state = readiness.state
        activation_blockers = list(readiness.activation_blockers)
        can_activate = readiness.can_activate
    else:
        can_activate = bool(api_base and credential_configured)

    return {
        "id": integration_id,
        "name": name,
        "enabled": enabled,
        "api_base": api_base,
        "credential_configured": credential_configured,
        "state": state,
        "can_activate": can_activate,
        "activation_blockers": activation_blockers,
        "ail_object_global_ids": settings.ail_object_global_ids if integration_id == "ail" else "",
        "intelowl_allowed_analyzers": settings.intelowl_allowed_analyzers if integration_id == "intelowl" else "",
        "cortex_allowed_analyzers": settings.cortex_allowed_analyzers if integration_id == "cortex" else "",
        "opencti_allowed_entity_types": settings.opencti_allowed_entity_types if integration_id == "opencti" else "",
        "opencti_checkpoint_path": settings.opencti_checkpoint_path if integration_id == "opencti" else "",
        "thehive_organization": settings.thehive_organization if integration_id == "thehive" else "",
        "credential_boundary": "Credentials remain server-side and are never returned by this API.",
    }


_apply_persisted_runtime_configuration()


@router.get("/api/v1/admin/integrations")
def list_integrations(
    principal: Annotated[Principal, Depends(require_permission(Permission.MANAGE_CONNECTORS))],
) -> list[dict[str, object]]:
    del principal
    return [_integration_row(integration_id) for integration_id in _INTEGRATIONS]


@router.patch("/api/v1/admin/integrations/{integration_id}")
def update_integration(
    integration_id: str,
    payload: IntegrationPatch,
    principal: Annotated[Principal, Depends(require_permission(Permission.MANAGE_CONNECTORS))],
) -> dict[str, object]:
    del principal
    spec = _INTEGRATIONS.get(integration_id)
    if spec is None:
        raise HTTPException(status_code=404, detail="unknown integration")
    _, enabled_attr, api_attr, secret_attr = spec
    if payload.api_base is not None:
        api_base = payload.api_base.strip().rstrip("/")
        if api_base and not api_base.startswith(("http://", "https://")):
            raise HTTPException(status_code=422, detail="API base must be an absolute HTTP(S) URL")
        if settings.production and api_base and not api_base.startswith("https://"):
            raise HTTPException(status_code=422, detail="production integration endpoints require HTTPS")
        setattr(settings, api_attr, api_base)
    if payload.credential is not None:
        credential = payload.credential.get_secret_value().strip()
        if not credential:
            raise HTTPException(status_code=422, detail="credential must not be empty")
        _persist_runtime_credential(integration_id, credential)
        setattr(settings, secret_attr, SecretStr(credential))
    if payload.ail_object_global_ids is not None:
        if integration_id != "ail":
            raise HTTPException(status_code=422, detail="AIL object scope is only valid for the AIL integration")
        settings.ail_object_global_ids = _normalize_csv(payload.ail_object_global_ids)
    if payload.intelowl_allowed_analyzers is not None:
        if integration_id != "intelowl":
            raise HTTPException(status_code=422, detail="IntelOwl analyzer allowlist is only valid for the IntelOwl integration")
        settings.intelowl_allowed_analyzers = _normalize_csv(payload.intelowl_allowed_analyzers)
    if payload.cortex_allowed_analyzers is not None:
        if integration_id != "cortex":
            raise HTTPException(status_code=422, detail="Cortex analyzer allowlist is only valid for the Cortex integration")
        settings.cortex_allowed_analyzers = _normalize_csv(payload.cortex_allowed_analyzers)
    if payload.opencti_allowed_entity_types is not None:
        if integration_id != "opencti":
            raise HTTPException(status_code=422, detail="OpenCTI entity-type allowlist is only valid for the OpenCTI integration")
        settings.opencti_allowed_entity_types = _normalize_csv(payload.opencti_allowed_entity_types)
    if payload.opencti_checkpoint_path is not None:
        if integration_id != "opencti":
            raise HTTPException(status_code=422, detail="OpenCTI checkpoint path is only valid for the OpenCTI integration")
        settings.opencti_checkpoint_path = payload.opencti_checkpoint_path.strip()
    if payload.thehive_organization is not None:
        if integration_id != "thehive":
            raise HTTPException(status_code=422, detail="TheHive organization scope is only valid for the TheHive integration")
        settings.thehive_organization = payload.thehive_organization.strip()
    if payload.enabled is not None:
        setattr(settings, enabled_attr, payload.enabled)
    _persist_runtime_configuration()
    return _integration_row(integration_id)


_PAGE = """<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>DTMO — Administration Center</title><link rel="stylesheet" href="/ui/design-system.css">
</head>
<body><a class="skip-link" href="#content">Ga naar hoofdinhoud</a>
<main id="content" class="workspace">
<header class="page-heading"><div><p class="eyebrow">Functional recovery · Administration</p><h1>Administration Center</h1><p>Beheer integration enablement en endpoints via de DTMO control plane. Credentials blijven uitsluitend server-side.</p></div><a class="button ghost" href="/">Operations Workbench</a></header>
<section class="surface"><div class="page-heading"><div><p class="eyebrow">Framework integrations</p><h2>Runtime configuration</h2></div><button id="integration-refresh" class="button secondary" type="button">Vernieuwen</button></div><div id="integration-status" class="status" role="status">Integraties laden…</div><div id="integration-list" class="cards"></div><p class="muted">Endpoint/enablement-wijzigingen worden persistent opgeslagen in de DTMO runtime configuration. Secretwaarden worden niet getoond of door deze pagina opgeslagen.</p></section>
<section class="content-grid equal" aria-label="Beheergebieden">
<article class="surface"><p class="eyebrow">Sources</p><h2>Source administration</h2><p>Bootstrap, registratie, bronvalidatie, connectiviteitstest en handmatige collection runs.</p><div class="header-actions"><a class="button primary" href="/ui/admin-sources">Bronconfiguratie</a><a class="button secondary" href="/ui/source-center">Source status</a></div></article>
<article class="surface"><p class="eyebrow">Identity</p><h2>Users & roles</h2><p>Governed RBAC principal- en roltoewijzingen blijven server-authorized en auditbaar.</p><a class="button secondary" href="/ui/console#administration">RBAC administration</a></article>
<article class="surface"><p class="eyebrow">Security</p><h2>Security administration</h2><p>Token revocation blijft een afzonderlijke privileged CISO-actie.</p><a class="button danger" href="/ui/ciso-security">Security controls</a></article>
<article class="surface"><p class="eyebrow">Assurance</p><h2>Audit</h2><p>Audit blijft read-only en gescheiden van operationele mutations.</p><a class="button secondary" href="/ui/auditor">Audit workspace</a></article>
</section>
<section class="surface"><h2>Separation-of-duties boundary</h2><p>De beheerconsole kan enablement en endpoints wijzigen, maar verleent geen review-, share-, publication- of external-assurance authority. Credentials blijven deployment/server-side secrets.</p></section>
</main>
<script>
(() => {
  const storage = {subject: () => sessionStorage.getItem('dtmo.subject') || 'admin-tester', roles: () => sessionStorage.getItem('dtmo.roles') || 'admin', apiKey: () => sessionStorage.getItem('dtmo.apiKey') || ''};
  const esc = (value) => String(value ?? '').replace(/[&<>"']/g, (char) => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
  async function api(url, options = {}) {
    const headers = {'X-DTMO-Subject': storage.subject(), 'X-DTMO-Roles': storage.roles(), 'X-DTMO-API-Key': storage.apiKey(), 'Accept':'application/json', ...(options.headers || {})};
    const response = await fetch(url, {...options, headers});
    const payload = await response.json().catch(() => ({}));
    if (!response.ok) throw new Error(payload.detail || `HTTP ${response.status}`);
    return payload;
  }
  function card(row) {
    return `<article class="surface" data-integration="${esc(row.id)}"><div class="page-heading"><div><p class="eyebrow">${esc(row.id)}</p><h2>${esc(row.name)}</h2></div><span class="status ${row.enabled ? 'ready' : 'muted'}">${row.enabled ? 'enabled' : 'disabled'} · ${esc(row.state)}</span></div><label>API endpoint<input type="url" data-field="api_base" value="${esc(row.api_base)}" placeholder="https://platform.example/api"></label><label>Credential (write-only)<input type="password" data-field="credential" value="" placeholder="Enter credential" autocomplete="new-password"></label><label><input type="checkbox" data-field="enabled" ${row.enabled ? 'checked' : ''}> Enabled</label><p class="muted">Credential: ${row.credential_configured ? 'configured' : 'not configured'}. Submitted values are write-only, cleared from this form after save and never returned by the API. ${esc(row.credential_boundary)}</p><button class="button primary" type="button" data-save="${esc(row.id)}">Opslaan</button></article>`;
  }
  async function load() {
    const status = document.getElementById('integration-status');
    const list = document.getElementById('integration-list');
    status.textContent = 'Integraties laden…';
    try {
      const rows = await api('/api/v1/admin/integrations');
      list.innerHTML = rows.map(card).join('');
      status.textContent = `${rows.length} integraties geladen. Configuratiewijzigingen zijn server-authorized.`;
    } catch (error) {
      list.innerHTML = '';
      status.textContent = `Integraties konden niet worden geladen: ${error.message}`;
    }
  }
  document.getElementById('integration-refresh').addEventListener('click', load);
  document.getElementById('integration-list').addEventListener('click', async (event) => {
    const button = event.target.closest('[data-save]'); if (!button) return;
    const id = button.dataset.save; const cardNode = button.closest('[data-integration]');
    const apiBase = cardNode.querySelector('[data-field="api_base"]').value;
    const credential = cardNode.querySelector('[data-field="credential"]').value;
    const enabled = cardNode.querySelector('[data-field="enabled"]').checked;
    const payload = {api_base: apiBase, enabled}; if (credential) payload.credential = credential;
    button.disabled = true;
    try { await api(`/api/v1/admin/integrations/${encodeURIComponent(id)}`, {method:'PATCH', headers:{'Content-Type':'application/json'}, body:JSON.stringify(payload)}); await load(); }
    catch (error) { alert(`Opslaan mislukt: ${error.message}`); button.disabled = false; }
  });
  load();
})();
</script></body></html>"""


@router.get("/ui/administration", response_class=HTMLResponse)
def administration_page() -> HTMLResponse:
    return HTMLResponse(_PAGE)

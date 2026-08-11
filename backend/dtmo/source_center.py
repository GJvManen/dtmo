from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dtmo.api.routes import get_session
from dtmo.auth.dependencies import require_permission
from dtmo.auth.policy import Permission, Principal, Role
from dtmo.config import get_settings
from dtmo.connectors.state import ConnectorRuntimeState
from dtmo.source_catalog import SOURCE_CATALOG
from dtmo.sources import SourceRegistry

router = APIRouter()
settings = get_settings()


@router.get("/api/v1/source-center/status")
async def source_center_status(
    principal: Annotated[Principal, Depends(require_permission(Permission.MANAGE_CONNECTORS))],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> list[dict[str, object]]:
    """Return executable catalog and registered-source status without exposing secrets."""
    if principal.is_service_account or Role.ADMIN not in principal.roles:
        return []

    states = {
        state.connector_id: state
        for state in (await session.scalars(select(ConnectorRuntimeState))).all()
    }
    registered = {source.id: source for source in await SourceRegistry(session).list()}
    result: list[dict[str, object]] = []

    for entry in SOURCE_CATALOG:
        if entry.execution_status not in {"supported", "supported-built-in"}:
            continue
        source = registered.get(entry.id)
        state = states.get(entry.id)
        built_in = entry.execution_status == "supported-built-in"
        enabled = settings.feature_live_connectors if built_in else bool(source and source.enabled)
        result.append(
            {
                "id": entry.id,
                "name": entry.name,
                "category": entry.category,
                "source_type": "cisa-kev" if built_in else "json-feed",
                "execution_profile": entry.execution_profile,
                "execution_status": entry.execution_status,
                "registered": built_in or source is not None,
                "enabled": enabled,
                "interval_seconds": (
                    settings.connector_poll_seconds
                    if built_in
                    else source.interval_seconds if source is not None else entry.recommended_interval_seconds
                ),
                "reliability": source.reliability if source is not None else entry.reliability,
                "health_status": state.health_status if state is not None else "unknown",
                "last_success_at": (
                    state.last_success_at.isoformat()
                    if state is not None and state.last_success_at is not None
                    else None
                ),
                "last_failure_at": (
                    state.last_failure_at.isoformat()
                    if state is not None and state.last_failure_at is not None
                    else None
                ),
                "consecutive_failures": state.consecutive_failures if state is not None else 0,
                "isolated_until": (
                    state.circuit_open_until.isoformat()
                    if state is not None and state.circuit_open_until is not None
                    else None
                ),
                "manual_run_available": (
                    (not settings.production or settings.feature_live_connectors)
                    if built_in
                    else source is not None and source.enabled
                ),
                "provenance": {
                    "endpoint": source.endpoint_url if source is not None else entry.endpoint_url,
                    "configured_reliability": source.reliability if source is not None else entry.reliability,
                    "note": entry.provenance_note,
                },
            }
        )
    return result


_PAGE = """<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>DTMO — Source Center</title>
<link rel="stylesheet" href="/ui/design-system.css">
<style>
.feed-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:1rem}.feed-card{display:flex;flex-direction:column;gap:.7rem}.feed-actions{display:flex;flex-wrap:wrap;gap:.5rem}.feed-meta{margin:0}.run-result{padding:.75rem;border:1px solid currentColor;border-radius:.5rem}.status-pill.ok{font-weight:700}.status-pill.warn{font-weight:700}.status-pill.blocked{font-weight:700}.metric-row{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:.5rem}.metric{padding:.6rem;border:1px solid rgba(127,127,127,.35);border-radius:.5rem}.metric strong{display:block;font-size:1.15rem}
</style>
</head>
<body>
<a class="skip-link" href="#content">Ga naar hoofdinhoud</a>
<main id="content" class="workspace">
<header class="page-heading"><div><p class="eyebrow">RC10.9 feed operations</p><h1>Source Center</h1><p>Registreer, activeer en start ondersteunde intelligencefeeds vanuit één beheerde operatorflow. Ingestie verleent nooit publicatierechten.</p></div><a class="button secondary" href="/ui/admin-sources">Geavanceerde bronconfiguratie</a></header>
<section class="surface" aria-labelledby="feed-heading">
<div class="surface-header"><div><p class="eyebrow">Framework feeds</p><h2 id="feed-heading">Beschikbare en geregistreerde feeds</h2></div><div class="feed-actions"><button id="bootstrap" class="button secondary">Registreer ondersteunde feeds</button><button id="refresh" class="button secondary">Vernieuwen</button></div></div>
<div id="status" role="status" aria-live="polite">Nog niet geladen.</div>
<div id="summary" class="metric-row" aria-label="Feed summary"></div>
<div id="sources" class="feed-grid"></div>
</section>
<section class="surface"><h2>Governance boundary</h2><p>Handmatige runs vereisen een menselijke admin met <code>manage:connectors</code>. Broncredentials en raw evidence worden niet in deze workspace getoond. Ingestie geeft geen review- of share approval-recht; review en externe share approval blijven afzonderlijke bevoegdheden.</p></section>
</main>
<script>
const e=s=>String(s??'').replace(/[&<>\"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;',"'":'&#39;'}[c]));
const h=(write=false)=>{const headers={'X-DTMO-Subject':sessionStorage.getItem('dtmo.subject')||'admin-tester','X-DTMO-Roles':sessionStorage.getItem('dtmo.roles')||'admin','X-DTMO-API-Key':sessionStorage.getItem('dtmo.apiKey')||''};if(write)headers['X-Request-ID']=crypto.randomUUID();return headers};
const statusEl=document.getElementById('status');const sourcesEl=document.getElementById('sources');const summaryEl=document.getElementById('summary');
function pill(s){const v=String(s||'unknown');const cls=['healthy','completed'].includes(v)?'ok':['failed','isolated'].includes(v)?'blocked':'warn';return `<span class="status-pill ${cls}">${e(v)}</span>`}
async function jsonRequest(url,options={}){const r=await fetch(url,options);let body={};try{body=await r.json()}catch{}if(!r.ok)throw new Error(body.detail||body.reason||`HTTP ${r.status}`);return body}
function runUrl(s){return s.execution_status==='supported-built-in'?`/connectors/${encodeURIComponent(s.id)}/run`:`/api/v1/admin/sources/${encodeURIComponent(s.id)}/run`}
function actions(s){if(!s.registered)return '<button class="button secondary" data-action="bootstrap">Registreren</button>';let html='';if(s.execution_status!=='supported-built-in')html+=`<button class="button secondary" data-action="toggle" data-id="${e(s.id)}" data-enabled="${s.enabled?'true':'false'}">${s.enabled?'Uitschakelen':'Inschakelen'}</button>`;html+=`<button class="button" data-action="run" data-id="${e(s.id)}" data-run-url="${e(runUrl(s))}" ${s.manual_run_available?'':'disabled'}>Feed nu laden</button>`;return html}
function render(d){const registered=d.filter(x=>x.registered).length,enabled=d.filter(x=>x.enabled).length,healthy=d.filter(x=>x.health_status==='healthy').length;summaryEl.innerHTML=`<div class="metric"><span>Framework feeds</span><strong>${d.length}</strong></div><div class="metric"><span>Geregistreerd</span><strong>${registered}</strong></div><div class="metric"><span>Actief</span><strong>${enabled}</strong></div><div class="metric"><span>Healthy</span><strong>${healthy}</strong></div>`;sourcesEl.innerHTML=d.map(s=>`<article class="surface feed-card" data-source-id="${e(s.id)}"><div><strong>${e(s.name)}</strong> ${pill(s.health_status)}</div><p class="feed-meta">${e(s.id)} · ${e(s.category)} · ${s.registered?'geregistreerd':'beschikbaar'} · ${s.enabled?'actief':'uit'}</p><p class="feed-meta">Iedere ${e(s.interval_seconds)}s · reliability ${e(s.reliability)} · profiel ${e(s.execution_profile)}</p><p class="feed-meta">Laatste succes: ${e(s.last_success_at||'—')} · laatste fout: ${e(s.last_failure_at||'—')} · failures: ${e(s.consecutive_failures)}</p><p class="feed-meta">Provenance: ${e(s.provenance.endpoint)}</p><div class="feed-actions">${actions(s)}</div><div class="run-result" data-result hidden></div></article>`).join('')}
async function load(){statusEl.textContent='Feeds laden…';try{const d=await jsonRequest('/api/v1/source-center/status',{headers:h()});render(d);statusEl.textContent=`${d.length} uitvoerbare frameworkfeeds geladen.`}catch(err){statusEl.textContent=`Feedstatus niet beschikbaar: ${err.message}`}}
async function bootstrap(){statusEl.textContent='Ondersteunde feeds registreren…';try{const d=await jsonRequest('/api/v1/admin/sources/catalog/bootstrap',{method:'POST',headers:h(true)});statusEl.textContent=`${d.length} ondersteunde feeds geregistreerd of reeds aanwezig.`;await load()}catch(err){statusEl.textContent=`Registratie mislukt: ${err.message}`}}
async function toggle(id,enabled){statusEl.textContent=`${id} ${enabled?'uitschakelen':'inschakelen'}…`;try{await jsonRequest(`/api/v1/admin/sources/${encodeURIComponent(id)}`,{method:'PATCH',headers:{...h(true),'Content-Type':'application/json'},body:JSON.stringify({enabled:!enabled})});await load()}catch(err){statusEl.textContent=`Wijziging mislukt: ${err.message}`}}
async function run(button){const card=button.closest('[data-source-id]');const result=card.querySelector('[data-result]');button.disabled=true;result.hidden=false;result.textContent='Feedrun gestart…';statusEl.textContent=`${button.dataset.id} laden…`;try{const data=await jsonRequest(button.dataset.runUrl,{method:'POST',headers:h(true)});result.innerHTML=`<strong>Run ${e(data.status)}</strong><br>Records: ${e(data.records??0)} · inserted: ${e(data.inserted??0)} · indexed: ${e(data.indexed??0)}${data.error?`<br>Fout: ${e(data.error)}`:''}<br>Publication gate: ${e(data.publication_gate||'human-approval-required')}`;statusEl.textContent=`${button.dataset.id}: ${data.status}.`;await load()}catch(err){result.textContent=`Run geblokkeerd/mislukt: ${err.message}`;statusEl.textContent=`${button.dataset.id}: ${err.message}`}finally{button.disabled=false}}
document.getElementById('refresh').addEventListener('click',load);document.getElementById('bootstrap').addEventListener('click',bootstrap);sourcesEl.addEventListener('click',ev=>{const b=ev.target.closest('button[data-action]');if(!b)return;if(b.dataset.action==='bootstrap')bootstrap();if(b.dataset.action==='toggle')toggle(b.dataset.id,b.dataset.enabled==='true');if(b.dataset.action==='run')run(b)});load();
</script>
</body></html>"""


@router.get("/ui/source-center", response_class=HTMLResponse)
def source_center() -> HTMLResponse:
    return HTMLResponse(_PAGE)

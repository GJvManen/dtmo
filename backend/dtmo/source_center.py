from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dtmo.api.routes import get_session
from dtmo.auth.dependencies import require_permission
from dtmo.auth.policy import Permission, Principal, Role
from dtmo.connectors.state import ConnectorRuntimeState
from dtmo.sources import SourceRegistry

router = APIRouter()


@router.get("/api/v1/source-center/status")
async def source_center_status(
    principal: Annotated[Principal, Depends(require_permission(Permission.MANAGE_CONNECTORS))],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> list[dict[str, object]]:
    """Return bounded operational source status without exposing secrets or raw evidence."""
    if principal.is_service_account or Role.ADMIN not in principal.roles:
        return []
    states = {
        state.connector_id: state
        for state in (await session.scalars(select(ConnectorRuntimeState))).all()
    }
    sources = await SourceRegistry(session).list()
    return [
        {
            "id": source.id,
            "name": source.name,
            "source_type": source.source_type,
            "enabled": source.enabled,
            "interval_seconds": source.interval_seconds,
            "reliability": source.reliability,
            "health_status": states[source.id].health_status if source.id in states else "unknown",
            "last_success_at": states[source.id].last_success_at.isoformat() if source.id in states and states[source.id].last_success_at else None,
            "last_failure_at": states[source.id].last_failure_at.isoformat() if source.id in states and states[source.id].last_failure_at else None,
            "consecutive_failures": states[source.id].consecutive_failures if source.id in states else 0,
            "isolated_until": states[source.id].circuit_open_until.isoformat() if source.id in states and states[source.id].circuit_open_until else None,
            "provenance": {"endpoint": source.endpoint_url, "configured_reliability": source.reliability},
        }
        for source in sources
    ]


_PAGE = """<!doctype html><html lang="nl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>DTMO — Source Center</title><link rel="stylesheet" href="/ui/design-system.css"></head><body><a class="skip-link" href="#content">Ga naar hoofdinhoud</a><main id="content" class="workspace"><header class="page-heading"><div><p class="eyebrow">RC10.4 unified workspace</p><h1>Source Center</h1><p>Operationele bronstatus, planning en provenance in één begrensde beheerweergave. Publicatie blijft buiten deze workspace.</p></div><a class="button secondary" href="/ui/admin-sources">Bronconfiguratie</a></header><section class="surface"><div class="surface-header"><div><p class="eyebrow">Execution health</p><h2>Geregistreerde bronnen</h2></div><button id="refresh" class="button secondary">Vernieuwen</button></div><div id="status" role="status" aria-live="polite">Nog niet geladen.</div><div id="sources"></div></section><section class="surface"><h2>Governance boundary</h2><p>Deze weergave toont geen secret references, raw evidence of request bodies. Wijzigingen en handmatige runs blijven uitsluitend beschikbaar via de bestaande menselijke admin + <code>manage:connectors</code> control plane. Ingestie verleent geen review- of share approval-recht.</p></section></main><script>const e=s=>String(s??'').replace(/[&<>\"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;',"'":'&#39;'}[c]));const h=()=>({'X-DTMO-Subject':sessionStorage.getItem('dtmo.subject')||'admin-tester','X-DTMO-Roles':sessionStorage.getItem('dtmo.roles')||'admin','X-DTMO-API-Key':sessionStorage.getItem('dtmo.apiKey')||''});async function load(){status.textContent='Laden…';const r=await fetch('/api/v1/source-center/status',{headers:h()});if(!r.ok){status.textContent='Bronstatus niet beschikbaar.';return}const d=await r.json();status.textContent=`${d.length} bronnen`;sources.innerHTML=d.map(s=>`<article class="surface"><strong>${e(s.name)}</strong> <span class="status-pill neutral">${e(s.health_status)}</span><p>${e(s.id)} · ${s.enabled?'actief':'uit'} · iedere ${e(s.interval_seconds)}s · reliability ${e(s.reliability)}</p><p>Laatste succes: ${e(s.last_success_at||'—')} · laatste fout: ${e(s.last_failure_at||'—')} · failures: ${e(s.consecutive_failures)}</p><p>Provenance endpoint: ${e(s.provenance.endpoint)}</p></article>`).join('')}refresh.addEventListener('click',load);load();</script></body></html>"""


@router.get("/ui/source-center", response_class=HTMLResponse)
def source_center() -> HTMLResponse:
    return HTMLResponse(_PAGE)

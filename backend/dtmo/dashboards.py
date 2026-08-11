from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from dtmo.api.routes import get_session
from dtmo.auth.dependencies import require_permission
from dtmo.auth.policy import Permission, Principal
from dtmo.connectors.state import ConnectorRuntimeState
from dtmo.persistence.models import IntelligenceItem

router = APIRouter()


async def _group_counts(session: AsyncSession, column) -> dict[str, int]:  # type: ignore[no-untyped-def]
    rows = (await session.execute(select(column, func.count()).group_by(column))).all()
    return {str(value.value if hasattr(value, "value") else value): int(count) for value, count in rows}


@router.get("/api/v1/dashboards/summary")
async def dashboard_summary(
    principal: Annotated[Principal, Depends(require_permission(Permission.READ_INTELLIGENCE))],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> dict[str, object]:
    del principal
    total = int((await session.scalar(select(func.count(IntelligenceItem.id)))) or 0)
    recent_cutoff = datetime.now(UTC) - timedelta(hours=24)
    recent = int(
        (
            await session.scalar(
                select(func.count(IntelligenceItem.id)).where(IntelligenceItem.discovered_at >= recent_cutoff)
            )
        )
        or 0
    )
    average_confidence = float(
        (await session.scalar(select(func.avg(IntelligenceItem.confidence_score)))) or 0.0
    )
    severity = await _group_counts(session, IntelligenceItem.severity)
    review_status = await _group_counts(session, IntelligenceItem.review_status)
    source = await _group_counts(session, IntelligenceItem.source_id)
    connector_health = await _group_counts(session, ConnectorRuntimeState.health_status)
    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "total_intelligence": total,
        "new_last_24h": recent,
        "average_confidence": round(average_confidence, 1),
        "severity": severity,
        "review_status": review_status,
        "sources": source,
        "connector_health": connector_health,
        "publication_boundary": "human-review-and-separate-share-approval-required",
    }


_PAGE = """<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>DTMO — Intelligence dashboards</title>
<link rel="stylesheet" href="/ui/design-system.css">
<style>
.dashboard-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:1rem}.kpi-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:1rem}.kpi{padding:1rem;border:1px solid rgba(127,127,127,.35);border-radius:.75rem}.kpi strong{display:block;font-size:1.8rem}.chart{min-height:280px}.chart svg{width:100%;height:220px;overflow:visible}.chart text{fill:currentColor;font-size:12px}.chart rect{fill:currentColor;opacity:.72}.chart line{stroke:currentColor;opacity:.25}.chart-table{width:100%;border-collapse:collapse;margin-top:1rem}.chart-table th,.chart-table td{text-align:left;padding:.45rem;border-bottom:1px solid rgba(127,127,127,.25)}.chart-table td:last-child,.chart-table th:last-child{text-align:right}.dashboard-actions{display:flex;gap:.5rem;flex-wrap:wrap}.muted{opacity:.75}
</style>
</head>
<body>
<a class="skip-link" href="#content">Ga naar hoofdinhoud</a>
<main id="content" class="workspace">
<header class="page-heading"><div><p class="eyebrow">RC10.10 graphical dashboards</p><h1>Intelligence & Operations Dashboards</h1><p>Grafische management- en operatorweergaven op basis van echte DTMO intelligence- en connectorstate. Iedere grafiek heeft een tabelalternatief.</p></div><div class="dashboard-actions"><a class="button secondary" href="/ui/source-center">Source Center</a><a class="button secondary" href="/ui/operations">Operations</a><button id="refresh" class="button">Vernieuwen</button></div></header>
<div id="status" role="status" aria-live="polite">Dashboard wordt geladen…</div>
<section class="surface"><h2>Kernindicatoren</h2><div class="kpi-grid"><article class="kpi"><span>Intelligence items</span><strong id="kpi-total">—</strong></article><article class="kpi"><span>Nieuw in 24 uur</span><strong id="kpi-recent">—</strong></article><article class="kpi"><span>Gem. confidence</span><strong id="kpi-confidence">—</strong></article><article class="kpi"><span>Actieve bronnen</span><strong id="kpi-sources">—</strong></article></div></section>
<section class="dashboard-grid" aria-label="Grafische dashboards">
<article class="surface chart"><h2>Severity-verdeling</h2><div id="severity-chart"></div><div id="severity-table"></div></article>
<article class="surface chart"><h2>Reviewstatus</h2><div id="review-chart"></div><div id="review-table"></div></article>
<article class="surface chart"><h2>Top intelligencebronnen</h2><div id="source-chart"></div><div id="source-table"></div></article>
<article class="surface chart"><h2>Connector health</h2><div id="health-chart"></div><div id="health-table"></div></article>
</section>
<section class="surface"><h2>Governance boundary</h2><p class="muted">Deze dashboards zijn read-only. Visualisatie, sortering of aggregatie verleent geen review- of publicatiebevoegdheid. Externe sharing blijft afhankelijk van afzonderlijke menselijke goedkeuring.</p></section>
</main>
<script>
const statusEl=document.getElementById('status');
const h=()=>({'X-DTMO-Subject':sessionStorage.getItem('dtmo.subject')||'analyst-tester','X-DTMO-Roles':sessionStorage.getItem('dtmo.roles')||'analyst','X-DTMO-API-Key':sessionStorage.getItem('dtmo.apiKey')||''});
const esc=s=>String(s??'').replace(/[&<>\"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;',"'":'&#39;'}[c]));
function entries(obj,limit=8){return Object.entries(obj||{}).sort((a,b)=>Number(b[1])-Number(a[1])).slice(0,limit)}
function table(target,data,label){const rows=entries(data);document.getElementById(target).innerHTML=`<table class="chart-table"><thead><tr><th scope="col">${esc(label)}</th><th scope="col">Aantal</th></tr></thead><tbody>${rows.map(([k,v])=>`<tr><td>${esc(k)}</td><td>${esc(v)}</td></tr>`).join('')||'<tr><td>Geen data</td><td>0</td></tr>'}</tbody></table>`}
function bars(target,data){const rows=entries(data);const width=520,height=210,left=130,right=30,top=10,rowH=24;const max=Math.max(1,...rows.map(([,v])=>Number(v)));const usable=width-left-right;const body=rows.map(([label,value],i)=>{const y=top+i*rowH;const w=Math.max(0,Number(value)/max*usable);return `<text x="0" y="${y+15}">${esc(label.slice(0,18))}</text><rect x="${left}" y="${y+3}" width="${w}" height="15" rx="3"></rect><text x="${left+w+6}" y="${y+15}">${esc(value)}</text>`}).join('');document.getElementById(target).innerHTML=`<svg viewBox="0 0 ${width} ${height}" role="img" aria-label="Staafdiagram"><line x1="${left}" x2="${left}" y1="0" y2="${height}"></line>${body}</svg>`}
async function load(){statusEl.textContent='Dashboard laden…';try{const r=await fetch('/api/v1/dashboards/summary',{headers:h()});if(!r.ok)throw new Error(`HTTP ${r.status}`);const d=await r.json();document.getElementById('kpi-total').textContent=d.total_intelligence;document.getElementById('kpi-recent').textContent=d.new_last_24h;document.getElementById('kpi-confidence').textContent=`${d.average_confidence}%`;document.getElementById('kpi-sources').textContent=Object.keys(d.sources||{}).length;bars('severity-chart',d.severity);table('severity-table',d.severity,'Severity');bars('review-chart',d.review_status);table('review-table',d.review_status,'Reviewstatus');bars('source-chart',d.sources);table('source-table',d.sources,'Bron');bars('health-chart',d.connector_health);table('health-table',d.connector_health,'Health');statusEl.textContent=`Dashboard bijgewerkt: ${new Date(d.generated_at).toLocaleString()}.`}catch(err){statusEl.textContent=`Dashboard niet beschikbaar: ${err.message}`}}
document.getElementById('refresh').addEventListener('click',load);load();
</script>
</body></html>"""


@router.get("/ui/dashboards", response_class=HTMLResponse)
def dashboards_page() -> HTMLResponse:
    return HTMLResponse(_PAGE)

from __future__ import annotations

import re
from typing import Annotated, Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dtmo.api.routes import get_session
from dtmo.auth.dependencies import require_permission
from dtmo.auth.policy import Permission, Principal
from dtmo.persistence.models import IntelligenceItem, ProvenanceRecord

router = APIRouter()

_CVE_RE = re.compile(r"\bCVE-\d{4}-\d{4,7}\b", re.IGNORECASE)


def _enum_value(value: object) -> object:
    return getattr(value, "value", value)


@router.get("/api/v1/intelligence/{item_id}/workspace")
async def intelligence_workspace_detail(
    item_id: UUID,
    principal: Annotated[Principal, Depends(require_permission(Permission.READ_INTELLIGENCE))],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> dict[str, object]:
    del principal
    item = await session.get(IntelligenceItem, item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="intelligence item not found")

    provenance = list(
        (
            await session.scalars(
                select(ProvenanceRecord)
                .where(ProvenanceRecord.item_id == item.id)
                .order_by(ProvenanceRecord.retrieved_at.asc())
            )
        ).all()
    )
    cve_text = " ".join([item.title, item.summary, *item.tags])
    cve_ids = sorted({match.upper() for match in _CVE_RE.findall(cve_text)})
    vendor = item.metadata_json.get("vendor")
    product = item.metadata_json.get("product")
    safe_metadata = {
        key: item.metadata_json[key]
        for key in ("source_reliability", "connector_managed")
        if key in item.metadata_json
    }
    return {
        "id": str(item.id),
        "source_id": item.source_id,
        "external_id": item.external_id,
        "item_type": _enum_value(item.item_type),
        "title": item.title,
        "summary": item.summary,
        "canonical_url": item.canonical_url,
        "published_at": item.published_at.isoformat() if item.published_at else None,
        "discovered_at": item.discovered_at.isoformat(),
        "severity": _enum_value(item.severity),
        "confidence_score": item.confidence_score,
        "confidence_level": _enum_value(item.confidence_level),
        "confidence_rationale": item.confidence_rationale,
        "education_relevance": item.education_relevance,
        "review_status": item.review_status,
        "share_approved": item.share_approved,
        "tags": item.tags,
        "context": {
            "cve_ids": cve_ids,
            "known_exploited": item.source_id == "cisa-kev",
            "vendor": vendor if isinstance(vendor, str) else None,
            "product": product if isinstance(product, str) else None,
        },
        "metadata": safe_metadata,
        "provenance": [
            {
                "source_url": record.source_url,
                "source_title": record.source_title,
                "publisher": record.publisher,
                "retrieved_at": record.retrieved_at.isoformat(),
                "source_reliability": _enum_value(record.source_reliability),
                "is_primary_source": record.is_primary_source,
                "content_integrity_verified": record.content_integrity_verified,
                "confidence_score": record.confidence_score,
            }
            for record in provenance
        ],
    }


_PAGE = """<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>DTMO — Threat Intelligence Workspace</title>
<link rel="stylesheet" href="/ui/design-system.css"><link rel="stylesheet" href="/ui/threat-workspace.css">
</head>
<body>
<a class="skip-link" href="#workspace">Ga naar hoofdinhoud</a>
<div class="ti-shell">
<aside class="ti-sidebar" aria-label="Threat intelligence navigatie">
<div class="ti-brand"><span>D</span><div><strong>DTMO</strong><small>Threat Intelligence</small></div></div>
<nav><a href="/ui/operations">Operations</a><a class="active" href="/ui/intelligence-workspace">Intelligence workspace</a><a href="/ui/admin-sources">Sources</a><a href="/ui/share-approval">Share approval</a><a href="/ui/auditor">Audit</a></nav>
<div class="ti-boundary"><strong>Governed analysis</strong><p>Zoeken en onderzoeken verleent geen review- of share approval-recht.</p></div>
</aside>
<main id="workspace" class="ti-main">
<header><div><p class="eyebrow">RC10.3 investigation workspace</p><h1>Threat Intelligence Workspace</h1><p>Doorzoek opgeslagen intelligence, open één canonical item en beoordeel context, confidence en provenance zonder publication authority te wijzigen.</p></div><span id="session-status" class="status-pill neutral">Sessie controleren</span></header>
<section class="ti-search surface">
<form id="search-form"><label for="query">Zoekopdracht</label><div class="ti-search-row"><input id="query" minlength="2" required placeholder="CVE, leverancier, ransomware, campagne…"><select id="severity" aria-label="Severity filter"><option value="">Alle severity</option><option>critical</option><option>high</option><option>medium</option><option>low</option><option>informational</option></select><input id="relevance" type="number" min="0" max="100" value="0" aria-label="Minimum onderwijsrelevantie"><button class="button primary" type="submit">Zoeken</button></div></form>
<div id="search-status" class="inline-status" role="status" aria-live="polite">Voer minimaal twee tekens in.</div>
</section>
<section class="ti-grid">
<article class="surface ti-results"><div class="surface-header"><div><p class="eyebrow">Resultaten</p><h2>Intelligence</h2></div><span id="result-count" class="status-pill neutral">0</span></div><div id="results" class="ti-result-list"><p class="muted">Nog geen zoekopdracht uitgevoerd.</p></div></article>
<article class="surface ti-detail"><div class="surface-header"><div><p class="eyebrow">Investigation</p><h2>Canonical detail</h2></div><a id="canonical-link" href="#" hidden target="_blank" rel="noreferrer">Primaire bron ↗</a></div><div id="detail"><p class="muted">Selecteer een resultaat om context en provenance te bekijken.</p></div></article>
</section>
<section class="surface ti-identity"><div class="surface-header"><div><p class="eyebrow">Local/dev/staging</p><h2>Testidentiteit</h2></div></div><div class="ti-id-grid"><label>Subject<input id="subject" value="external-tester"></label><label>Rollen<input id="roles" value="analyst"></label><label>API key<input id="api-key" type="password"></label><button id="save-identity" class="button secondary" type="button">Identiteit toepassen</button></div><p class="muted">Waarden blijven alleen in deze browsertab via <code>sessionStorage</code>. Productie gebruikt de geconfigureerde bearer-token/identity-provider route.</p></section>
</main></div><script src="/ui/threat-workspace.js" defer></script></body></html>"""

_CSS = """
body{margin:0;background:#07111c}.ti-shell{min-height:100vh;display:grid;grid-template-columns:250px minmax(0,1fr)}.ti-sidebar{height:100vh;position:sticky;top:0;padding:1.25rem;background:#081522;border-right:1px solid #183047;display:flex;flex-direction:column;gap:1.25rem}.ti-brand{display:flex;gap:.7rem;align-items:center}.ti-brand>span{display:grid;place-items:center;width:38px;height:38px;border-radius:10px;background:#168ee0;font-weight:800}.ti-brand div{display:grid}.ti-brand small,.muted{color:#91a5bd}.ti-sidebar nav{display:grid;gap:.35rem}.ti-sidebar nav a{padding:.7rem .75rem;border-radius:9px;text-decoration:none;color:#cbd8e5}.ti-sidebar nav a.active,.ti-sidebar nav a:hover{background:#11263a;color:#fff}.ti-boundary{margin-top:auto;padding:1rem;border:1px solid #24425d;border-radius:12px;background:#0d1a29}.ti-boundary p{color:#91a5bd;margin:.45rem 0 0;font-size:.85rem}.ti-main{padding:1.5rem;max-width:1650px;width:100%;margin:0 auto}.ti-main>header{display:flex;justify-content:space-between;gap:1.5rem;align-items:start;margin-bottom:1.25rem}.ti-main h1{margin:.2rem 0}.ti-main header p{max-width:850px;color:#91a5bd}.ti-search{margin-bottom:1rem}.ti-search-row{display:grid;grid-template-columns:minmax(260px,1fr) 170px 160px auto;gap:.65rem}.ti-search-row input,.ti-search-row select,.ti-id-grid input{background:#0a1724;color:#fff;border:1px solid #24425d;border-radius:9px;padding:.7rem}.ti-grid{display:grid;grid-template-columns:minmax(340px,.8fr) minmax(420px,1.2fr);gap:1rem}.ti-results,.ti-detail{min-height:540px}.ti-result-list{display:grid;gap:.65rem;max-height:72vh;overflow:auto}.ti-result{width:100%;text-align:left;border:1px solid #20384f;background:#0a1724;color:#eef5ff;border-radius:11px;padding:.85rem;display:grid;gap:.35rem}.ti-result:hover,.ti-result:focus-visible{border-color:#55b7ff}.ti-result-top{display:flex;justify-content:space-between;gap:.75rem}.ti-result small,.ti-meta span,.ti-provenance p{color:#91a5bd}.ti-meta{display:flex;gap:.45rem;flex-wrap:wrap}.ti-meta span{padding:.2rem .45rem;border:1px solid #24425d;border-radius:999px;font-size:.78rem}.ti-detail-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.7rem;margin:1rem 0}.ti-stat{padding:.75rem;background:#0a1724;border:1px solid #20384f;border-radius:10px}.ti-stat span{display:block;color:#91a5bd;font-size:.78rem}.ti-context,.ti-provenance{display:grid;gap:.6rem}.ti-provenance article{border-left:3px solid #2d648d;padding:.65rem .75rem;background:#0a1724}.ti-id-grid{display:grid;grid-template-columns:1fr 1fr 1fr auto;gap:.65rem;align-items:end}.ti-id-grid label{display:grid;gap:.3rem}@media(max-width:980px){.ti-grid{grid-template-columns:1fr}.ti-search-row{grid-template-columns:1fr 1fr}.ti-id-grid{grid-template-columns:1fr 1fr}}@media(max-width:720px){.ti-shell{display:block}.ti-sidebar{height:auto;position:static}.ti-boundary{display:none}.ti-main{padding:1rem}.ti-main>header{display:block}.ti-search-row,.ti-id-grid,.ti-detail-grid{grid-template-columns:1fr}.ti-results,.ti-detail{min-height:auto}}
"""

_JS = r"""
const byId=(id)=>document.getElementById(id);
const session={subject:sessionStorage.getItem('dtmo.subject')||'external-tester',roles:sessionStorage.getItem('dtmo.roles')||'analyst',apiKey:sessionStorage.getItem('dtmo.apiKey')||''};
function headers(){return {'X-DTMO-Subject':session.subject,'X-DTMO-Roles':session.roles,'X-DTMO-API-Key':session.apiKey,'X-Request-ID':crypto.randomUUID()}}
function esc(value){return String(value??'').replace(/[&<>'"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]))}
async function api(path){const response=await fetch(path,{headers:headers()});let payload={};try{payload=await response.json()}catch{}if(!response.ok)throw new Error(payload.detail||`HTTP ${response.status}`);return payload}
function setSession(){byId('session-status').textContent=session.apiKey?`${session.subject} · ${session.roles}`:'Geen API key';byId('session-status').className=`status-pill ${session.apiKey?'good':'neutral'}`;byId('subject').value=session.subject;byId('roles').value=session.roles;}
function renderResults(results){byId('result-count').textContent=String(results.length);byId('results').innerHTML=results.length?results.map(r=>`<button class="ti-result" type="button" data-id="${esc(r.id)}"><div class="ti-result-top"><strong>${esc(r.title)}</strong><span>${esc(r.severity||'—')}</span></div><small>${esc(r.source_id||'unknown source')} · relevance ${esc(r.education_relevance??0)} · confidence ${esc(r.confidence_score??'—')}</small><p>${esc((r.summary||'').slice(0,220))}</p></button>`).join(''):'<p class="muted">Geen resultaten.</p>';document.querySelectorAll('[data-id]').forEach(button=>button.addEventListener('click',()=>loadDetail(button.dataset.id)))}
async function search(){const q=byId('query').value.trim();if(q.length<2)return;const params=new URLSearchParams({q,minimum_relevance:byId('relevance').value||'0',size:'50'});if(byId('severity').value)params.set('severity',byId('severity').value);byId('search-status').textContent='Zoeken…';try{const data=await api(`/api/v1/intelligence/search?${params}`);renderResults(data.results);byId('search-status').textContent=`${data.count} resultaten voor “${data.query}”.`}catch(err){byId('search-status').textContent=`Zoeken mislukt: ${err.message}`;renderResults([])}}
async function loadDetail(id){byId('detail').innerHTML='<p class="muted">Detail laden…</p>';try{const d=await api(`/api/v1/intelligence/${encodeURIComponent(id)}/workspace`);const c=d.context||{};const provenance=d.provenance||[];byId('canonical-link').hidden=false;byId('canonical-link').href=d.canonical_url;byId('detail').innerHTML=`<h3>${esc(d.title)}</h3><p>${esc(d.summary)}</p><div class="ti-detail-grid"><div class="ti-stat"><span>Severity</span><strong>${esc(d.severity)}</strong></div><div class="ti-stat"><span>Confidence</span><strong>${esc(d.confidence_score)} · ${esc(d.confidence_level)}</strong></div><div class="ti-stat"><span>Education relevance</span><strong>${esc(d.education_relevance)}</strong></div><div class="ti-stat"><span>Review</span><strong>${esc(d.review_status)}</strong></div><div class="ti-stat"><span>Share approval</span><strong>${d.share_approved?'Approved':'Not approved'}</strong></div><div class="ti-stat"><span>Source</span><strong>${esc(d.source_id)}</strong></div></div><section class="ti-context"><h4>Context</h4><p><strong>CVE:</strong> ${c.cve_ids?.length?c.cve_ids.map(esc).join(', '):'geen expliciete CVE in opgeslagen record'}</p><p><strong>Known exploited:</strong> ${c.known_exploited?'Ja — CISA KEV bron':'Niet als KEV-bron gemarkeerd'}</p><p><strong>Vendor/product:</strong> ${esc(c.vendor||'—')} / ${esc(c.product||'—')}</p></section><section class="ti-provenance"><h4>Provenance (${provenance.length})</h4>${provenance.length?provenance.map(p=>`<article><strong>${esc(p.publisher||p.source_title||'Bron')}</strong><p><a href="${esc(p.source_url)}" target="_blank" rel="noreferrer">${esc(p.source_url)}</a></p><small>confidence ${esc(p.confidence_score)} · reliability ${esc(p.source_reliability)} · integrity ${p.content_integrity_verified?'verified':'not independently verified'}</small></article>`).join(''):'<p class="muted">Geen provenance-record gevonden.</p>'}</section>`;}catch(err){byId('detail').innerHTML=`<p class="inline-status">Detail laden mislukt: ${esc(err.message)}</p>`}}
byId('search-form').addEventListener('submit',event=>{event.preventDefault();search()});byId('save-identity').addEventListener('click',()=>{session.subject=byId('subject').value.trim();session.roles=byId('roles').value.trim();session.apiKey=byId('api-key').value;sessionStorage.setItem('dtmo.subject',session.subject);sessionStorage.setItem('dtmo.roles',session.roles);sessionStorage.setItem('dtmo.apiKey',session.apiKey);setSession()});setSession();
"""


@router.get("/ui/intelligence-workspace", response_class=HTMLResponse)
def threat_intelligence_workspace() -> HTMLResponse:
    return HTMLResponse(_PAGE)


@router.get("/ui/threat-workspace.css")
def threat_workspace_css() -> Response:
    return Response(_CSS, media_type="text/css")


@router.get("/ui/threat-workspace.js")
def threat_workspace_js() -> Response:
    return Response(_JS, media_type="application/javascript")

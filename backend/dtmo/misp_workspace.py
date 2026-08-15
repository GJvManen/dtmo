from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import HTMLResponse, Response

router = APIRouter()

_PAGE = r'''<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>DTMO — MISP Workspace</title>
<link rel="stylesheet" href="/ui/design-system.css"><link rel="stylesheet" href="/ui/misp-workspace.css">
</head>
<body>
<a class="skip-link" href="#main">Ga naar hoofdinhoud</a>
<div class="misp-shell">
<aside class="misp-side"><div class="brand"><div class="brand-mark">D</div><div><strong>DTMO</strong><span>Threat Intelligence</span></div></div>
<nav><a href="/ui/intelligence-workspace">Intelligence</a><a class="active" href="/ui/misp-workspace">MISP</a><a href="/ui/share-approval">Share approval</a><a href="/ui/auditor">Audit</a></nav>
<div class="boundary"><strong>Governed sharing</strong><p>Deze workspace verleent geen review- of share approval-recht. Export vereist voorafgaande onafhankelijke menselijke review en share approval.</p></div></aside>
<main id="main" class="workspace"><header><div><p class="eyebrow">E8.6–E8.7 governed integration</p><h1>MISP Workspace</h1><p>Onderzoek MISP-origin intelligence en voer alleen reeds goedgekeurde intelligence gecontroleerd uit naar MISP.</p></div><span id="session" class="status-pill neutral">Sessie controleren…</span></header>
<section class="grid"><article class="surface"><div class="surface-header"><div><p class="eyebrow">Read path</p><h2>MISP intelligence</h2></div><span class="status-pill good">Read-only ingest</span></div><p>Zoek canonical DTMO-records die via de MISP read connector zijn opgeslagen. De UI maakt geen live-connectivityclaim.</p><form id="search-form" class="row"><input id="query" minlength="2" value="misp" aria-label="Zoek MISP intelligence"><button class="button primary" type="submit">Zoeken</button></form><div id="search-status" class="status" role="status"></div><div id="results" class="cards"></div></article>
<article class="surface"><div class="surface-header"><div><p class="eyebrow">Export path</p><h2>Governed export</h2></div><span class="status-pill neutral">Unpublished event</span></div><p>Export maakt een MISP-event met <strong>published=false</strong>. MISP-publicatie of synchronisatie blijft een afzonderlijke governed actie.</p><label>Canonical intelligence item ID<input id="item-id" placeholder="UUID"></label><div class="three"><label>Distribution<select id="distribution"><option value="0">0 — Your organisation only</option><option value="1">1 — This community only</option><option value="2">2 — Connected communities</option><option value="3">3 — All communities</option><option value="4">4 — Sharing group</option></select></label><label>TLP<select id="tlp"><option>tlp:amber</option><option>tlp:amber+strict</option><option>tlp:green</option><option>tlp:clear</option><option>tlp:red</option></select></label><label>Sharing group<input id="sharing-group" placeholder="alleen bij distribution 4"></label></div><button id="export" class="button danger" type="button">Export approved intelligence</button><div class="notice"><strong>Fail-closed:</strong> service accounts, ontbrekende review/share approval, ongeldige distributie, minder restrictieve authoritative TLP en replay worden server-side geweigerd.</div><pre id="export-status">Nog geen export uitgevoerd.</pre></article></section>
<section class="surface"><h2>Betekenisgrenzen</h2><div class="limits"><div><strong>MISP read</strong><span>Provenance-backed CTI context; geen bewijs van lokale exposure of compromise.</span></div><div><strong>Share approval</strong><span>Moet vooraf afzonderlijk door een bevoegde menselijke principal zijn vastgelegd.</span></div><div><strong>MISP export</strong><span>Technische overdracht naar een unpublished event; geen autonome externe publicatie.</span></div></div></section>
</main></div><script src="/ui/misp-workspace.js" defer></script></body></html>'''

_CSS = r'''
body{margin:0;background:#07111c}.misp-shell{min-height:100vh;display:grid;grid-template-columns:250px minmax(0,1fr)}.misp-side{height:100vh;position:sticky;top:0;padding:1.25rem;background:#081522;border-right:1px solid #183047;display:flex;flex-direction:column;gap:1.25rem}.misp-side nav{display:grid;gap:.35rem}.misp-side nav a{padding:.7rem .75rem;border-radius:9px;text-decoration:none;color:#cbd8e5}.misp-side nav a.active,.misp-side nav a:hover{background:#11263a;color:#fff}.boundary{margin-top:auto;padding:1rem;border:1px solid #24425d;border-radius:12px;background:#0d1a29}.boundary p{color:#91a5bd;font-size:.85rem}.workspace{padding:1.5rem;max-width:1600px;width:100%;margin:auto}.workspace>header{display:flex;justify-content:space-between;gap:1rem;align-items:start}.workspace>header p{color:#91a5bd;max-width:850px}.grid{display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin:1rem 0}.row{display:grid;grid-template-columns:1fr auto;gap:.6rem}.three{display:grid;grid-template-columns:repeat(3,1fr);gap:.6rem}.three label,label{display:grid;gap:.3rem}input,select{background:#0a1724;color:#fff;border:1px solid #24425d;border-radius:9px;padding:.7rem}.cards{display:grid;gap:.6rem;margin-top:.75rem}.result{border:1px solid #20384f;background:#0a1724;border-radius:10px;padding:.8rem}.result small{color:#91a5bd}.notice{margin-top:.8rem;padding:.75rem;border:1px solid #8c6b2c;border-radius:9px;background:#241e11}pre{white-space:pre-wrap;background:#06101a;border:1px solid #20384f;border-radius:9px;padding:.8rem}.limits{display:grid;grid-template-columns:repeat(3,1fr);gap:.75rem}.limits div{display:grid;gap:.3rem;padding:.8rem;background:#0a1724;border:1px solid #20384f;border-radius:10px}.limits span{color:#91a5bd}@media(max-width:900px){.misp-shell{display:block}.misp-side{position:relative;height:auto}.boundary{display:none}.grid,.limits,.three{grid-template-columns:1fr}}
'''

_JS = r'''
const $=id=>document.getElementById(id);const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
async function session(){const r=await fetch('/api/v1/ui/session',{credentials:'same-origin'});const b=await r.json();if(!r.ok)throw new Error(b.detail||`HTTP ${r.status}`);$('session').textContent=`${b.subject} · ${b.roles.join(', ')||'geen rollen'}`;$('session').className='status-pill good';$('export').hidden=!b.permissions.includes('approve:share')}
async function search(){const q=$('query').value.trim();if(q.length<2)return;$('search-status').textContent='Zoeken…';const r=await fetch(`/api/v1/intelligence/search?q=${encodeURIComponent(q)}&size=25`,{credentials:'same-origin'});const b=await r.json();if(!r.ok)throw new Error(b.detail||`HTTP ${r.status}`);const rows=(b.results||[]).filter(x=>x.source_id==='misp'||x.source==='misp');$('results').innerHTML=rows.length?rows.map(x=>`<article class="result"><strong>${esc(x.title)}</strong><p>${esc(x.summary)}</p><small>${esc(x.id)} · MISP provenance retained in canonical record</small></article>`).join(''):'<p>Geen MISP-origin intelligence in deze zoekset.</p>';$('search-status').textContent=`${rows.length} MISP-resultaten in canonical DTMO-data.`}
async function doExport(){const id=$('item-id').value.trim();if(!id){$('export-status').textContent='Vul eerst een canonical intelligence item ID in.';return}const p=new URLSearchParams({distribution:$('distribution').value,tlp:$('tlp').value});if($('sharing-group').value.trim())p.set('sharing_group_id',$('sharing-group').value.trim());$('export-status').textContent='Governed export wordt verwerkt…';const r=await fetch(`/api/v1/intelligence/${encodeURIComponent(id)}/misp-export?${p}`,{method:'POST',credentials:'same-origin',headers:{'X-Request-ID':crypto.randomUUID()}});let b={};try{b=await r.json()}catch{};$('export-status').textContent=JSON.stringify({status:r.status,...b},null,2)}
$('search-form').addEventListener('submit',e=>{e.preventDefault();search().catch(err=>$('search-status').textContent=`Zoeken mislukt: ${err.message}`)});$('export').addEventListener('click',()=>doExport().catch(err=>$('export-status').textContent=`Export mislukt: ${err.message}`));session().catch(err=>{$('session').textContent=`Sessiefout: ${err.message}`;$('session').className='status-pill error'});
'''

_HEADERS = {"Cache-Control": "no-store", "Content-Security-Policy": "default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self'; img-src 'self' data:; frame-ancestors 'none'; base-uri 'none'; form-action 'self'"}


@router.get("/ui/misp-workspace", response_class=HTMLResponse, include_in_schema=False)
def misp_workspace_page() -> HTMLResponse:
    return HTMLResponse(_PAGE, headers=_HEADERS)


@router.get("/ui/misp-workspace.css", include_in_schema=False)
def misp_workspace_css() -> Response:
    return Response(_CSS, media_type="text/css", headers={"Cache-Control": "no-store"})


@router.get("/ui/misp-workspace.js", include_in_schema=False)
def misp_workspace_js() -> Response:
    return Response(_JS, media_type="application/javascript", headers={"Cache-Control": "no-store"})

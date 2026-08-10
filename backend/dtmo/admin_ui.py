from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import HTMLResponse, Response

router = APIRouter()

_PAGE = """<!doctype html>
<html lang="nl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="dark">
  <title>DTMO — Admin Source Registry</title>
  <link rel="stylesheet" href="/ui/design-system.css">
  <link rel="stylesheet" href="/ui/admin-sources.css">
</head>
<body>
<a class="skip-link" href="#content">Ga naar hoofdinhoud</a>
<div class="admin-shell">
  <aside class="sidebar" aria-label="Admin navigatie">
    <div class="brand"><div class="brand-mark" aria-hidden="true">D</div><div><strong>DTMO</strong><span>Administration</span></div></div>
    <nav class="nav-list"><a class="nav-item" href="/">Threat console</a><a class="nav-item active" href="/ui/admin-sources">Bronnen & connectors</a><a class="nav-item" href="/docs">API-documentatie</a></nav>
    <div class="sidebar-footer"><span class="sidebar-label">Governance</span><p>Alle wijzigingen vereisen een menselijke <code>admin</code>-rol en worden persistent geaudit.</p></div>
  </aside>
  <div class="app-main">
    <header class="app-header"><div><p class="eyebrow">Configuration control plane</p><h1>Source Registry</h1></div><button id="refresh" class="button secondary">Vernieuwen</button></header>
    <main id="content" class="workspace">
      <section class="page-heading"><div><p class="eyebrow">Admin workspace</p><h2>Bronnen beheren</h2><p>Registreer en beheer toegestane intelligencebronnen zonder secrets in configuratie op te slaan.</p></div><span id="status" class="status-pill neutral" role="status" aria-live="polite">Niet verbonden</span></section>
      <section class="kpi-grid" aria-label="Bronstatus"><article class="kpi-card"><span class="kpi-label">Totaal</span><strong id="kpi-total">—</strong><small>Geregistreerde bronnen</small></article><article class="kpi-card"><span class="kpi-label">Actief</span><strong id="kpi-active">—</strong><small>Ingeschakelde definities</small></article><article class="kpi-card"><span class="kpi-label">Authoritative</span><strong id="kpi-authoritative">—</strong><small>Hoogste bronbetrouwbaarheid</small></article><article class="kpi-card"><span class="kpi-label">Secret refs</span><strong id="kpi-secrets">—</strong><small>Geen raw secrets</small></article></section>
      <div class="content-grid equal">
        <article class="surface">
          <div class="surface-header"><div><p class="eyebrow">Registry</p><h3>Bronnen</h3></div></div>
          <div id="source-list" class="source-list"><p class="muted">Nog niet geladen.</p></div>
        </article>
        <article class="surface">
          <div class="surface-header"><div><p class="eyebrow">Nieuwe bron</p><h3>Registreren</h3></div></div>
          <form id="source-form" class="form-grid">
            <label>Source ID<input id="source-id" required pattern="[a-z0-9_-]+" placeholder="vendor-feed"></label>
            <label>Naam<input id="source-name" required placeholder="Vendor advisory feed"></label>
            <label>Type<select id="source-type"><option value="json-feed">JSON feed</option><option value="cisa-kev">CISA KEV</option></select></label>
            <label>Betrouwbaarheid<select id="source-reliability"><option>authoritative</option><option>high</option><option selected>medium</option><option>low</option></select></label>
            <label class="span-2">HTTPS endpoint<input id="source-url" type="url" required placeholder="https://example.org/feed.json"></label>
            <label>Interval (sec)<input id="source-interval" type="number" min="60" max="86400" value="3600"></label>
            <label>Secret reference<input id="source-secret" placeholder="vault://dtmo/source/key"></label>
            <label class="toggle-row"><input id="source-enabled" type="checkbox"> Direct inschakelen</label>
            <button class="button primary" type="submit">Bron registreren</button>
          </form>
          <div class="sod-notice"><strong>SSRF & secrets</strong><span>Alleen HTTPS public-host configuratie. Local/internal hosts, embedded credentials en raw secrets worden geweigerd.</span></div>
        </article>
      </div>
      <article class="surface"><div class="surface-header"><div><p class="eyebrow">Identity</p><h3>Lokale testidentiteit</h3></div></div><div class="form-grid three"><label>Subject<input id="subject" value="admin-tester"></label><label>Rollen<input id="roles" value="admin"></label><label>API key<input id="api-key" type="password"></label><button id="save-identity" class="button secondary" type="button">Identiteit toepassen</button></div><p class="muted">Alleen local/dev/staging; waarden blijven in <code>sessionStorage</code>. Production vereist bearer-token authenticatie.</p></article>
    </main>
  </div>
</div>
<script src="/ui/admin-sources.js" defer></script>
</body></html>"""

_CSS = """
.admin-shell{min-height:100vh;display:grid;grid-template-columns:250px minmax(0,1fr)}.source-list{display:grid;gap:.75rem}.source-card{border:1px solid var(--line);border-radius:12px;padding:1rem;background:var(--surface-2)}.source-card header{display:flex;justify-content:space-between;gap:1rem;align-items:start}.source-meta{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.45rem;margin-top:.8rem}.source-meta span{color:var(--muted);font-size:.9rem}.source-actions{display:flex;gap:.5rem;flex-wrap:wrap;margin-top:.9rem}.muted{color:var(--muted)}select{background:var(--surface-2);color:var(--text);border:1px solid var(--line);border-radius:9px;padding:.68rem .75rem}.toggle-row{display:flex;align-items:center;gap:.55rem}.toggle-row input{width:auto}.sidebar-footer p{font-size:.82rem;color:var(--muted);line-height:1.45}.app-header{position:sticky;top:0;z-index:5}@media(max-width:850px){.admin-shell{display:block}.sidebar{position:relative;height:auto}.source-meta{grid-template-columns:1fr}}
"""

_JS = r"""
const byId=(id)=>document.getElementById(id);
const session={subject:sessionStorage.getItem('dtmo.subject')||'admin-tester',roles:sessionStorage.getItem('dtmo.roles')||'admin',apiKey:sessionStorage.getItem('dtmo.apiKey')||''};
function headers(json=false){const h={'X-DTMO-Subject':session.subject,'X-DTMO-Roles':session.roles,'X-DTMO-API-Key':session.apiKey,'X-Request-ID':crypto.randomUUID()};if(json)h['Content-Type']='application/json';return h}
function setStatus(text,kind='neutral'){const el=byId('status');el.textContent=text;el.className=`status-pill ${kind}`}
async function api(path,options={}){const response=await fetch(path,{...options,headers:{...headers(Boolean(options.body)),...(options.headers||{})}});let payload={};try{payload=await response.json()}catch{}if(!response.ok)throw new Error(payload.detail||`HTTP ${response.status}`);return payload}
function escapeHtml(value){return String(value).replace(/[&<>'"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]))}
async function load(){setStatus('Bronnen laden…','loading');try{const sources=await api('/api/v1/admin/sources');render(sources);setStatus('Admin registry verbonden','good')}catch(err){setStatus(`Laden mislukt: ${err.message}`,'bad');byId('source-list').innerHTML='<p class="muted">Geen registrydata beschikbaar.</p>'}}
function render(sources){byId('kpi-total').textContent=sources.length;byId('kpi-active').textContent=sources.filter(s=>s.enabled).length;byId('kpi-authoritative').textContent=sources.filter(s=>s.reliability==='authoritative').length;byId('kpi-secrets').textContent=sources.filter(s=>s.secret_ref).length;byId('source-list').innerHTML=sources.length?sources.map(s=>`<article class="source-card"><header><div><strong>${escapeHtml(s.name)}</strong><div class="muted">${escapeHtml(s.id)}</div></div><span class="status-pill ${s.enabled?'good':'neutral'}">${s.enabled?'Actief':'Uit'}</span></header><div class="source-meta"><span>Type: ${escapeHtml(s.source_type)}</span><span>Reliability: ${escapeHtml(s.reliability)}</span><span>Interval: ${s.interval_seconds}s</span><span>Secret: ${s.secret_ref?'reference configured':'geen'}</span><span style="grid-column:1/-1">${escapeHtml(s.endpoint_url)}</span></div><div class="source-actions"><button class="button secondary" data-validate="${escapeHtml(s.id)}">Valideren</button><button class="button ghost" data-toggle="${escapeHtml(s.id)}" data-enabled="${s.enabled}">${s.enabled?'Uitschakelen':'Inschakelen'}</button></div></article>`).join(''):'<p class="muted">Nog geen bronnen geregistreerd.</p>';document.querySelectorAll('[data-validate]').forEach(b=>b.addEventListener('click',()=>validateSource(b.dataset.validate)));document.querySelectorAll('[data-toggle]').forEach(b=>b.addEventListener('click',()=>toggleSource(b.dataset.toggle,b.dataset.enabled!=='true')))}
async function validateSource(id){try{const result=await api(`/api/v1/admin/sources/${encodeURIComponent(id)}/validate`,{method:'POST'});setStatus(result.valid?`${id}: configuratie geldig`:`${id}: ${result.reason}`,result.valid?'good':'bad')}catch(err){setStatus(`Validatie mislukt: ${err.message}`,'bad')}}
async function toggleSource(id,enabled){try{await api(`/api/v1/admin/sources/${encodeURIComponent(id)}`,{method:'PATCH',body:JSON.stringify({enabled})});await load()}catch(err){setStatus(`Wijzigen mislukt: ${err.message}`,'bad')}}
byId('source-form').addEventListener('submit',async e=>{e.preventDefault();const payload={id:byId('source-id').value.trim(),name:byId('source-name').value.trim(),source_type:byId('source-type').value,endpoint_url:byId('source-url').value.trim(),enabled:byId('source-enabled').checked,interval_seconds:Number(byId('source-interval').value),reliability:byId('source-reliability').value,secret_ref:byId('source-secret').value.trim()||null};try{await api('/api/v1/admin/sources',{method:'POST',body:JSON.stringify(payload)});e.target.reset();byId('source-interval').value='3600';setStatus('Bron geregistreerd','good');await load()}catch(err){setStatus(`Registratie mislukt: ${err.message}`,'bad')}});
byId('refresh').addEventListener('click',load);byId('save-identity').addEventListener('click',()=>{session.subject=byId('subject').value.trim();session.roles=byId('roles').value.trim();session.apiKey=byId('api-key').value;sessionStorage.setItem('dtmo.subject',session.subject);sessionStorage.setItem('dtmo.roles',session.roles);sessionStorage.setItem('dtmo.apiKey',session.apiKey);load()});byId('subject').value=session.subject;byId('roles').value=session.roles;byId('api-key').value=session.apiKey;load();
"""

@router.get("/ui/admin-sources", response_class=HTMLResponse)
def admin_sources_page() -> HTMLResponse:
    return HTMLResponse(_PAGE)

@router.get("/ui/admin-sources.css")
def admin_sources_css() -> Response:
    return Response(_CSS, media_type="text/css")

@router.get("/ui/admin-sources.js")
def admin_sources_js() -> Response:
    return Response(_JS, media_type="application/javascript")

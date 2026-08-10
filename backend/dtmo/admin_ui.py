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
    <div class="sidebar-footer"><span class="sidebar-label">Governance</span><p>Registrywijzigingen en handmatige source runs vereisen een menselijke <code>admin</code> met <code>manage:connectors</code>. Ingestie verleent nooit publicatierecht.</p></div>
  </aside>
  <div class="app-main">
    <header class="app-header"><div><p class="eyebrow">Configuration & ingestion control plane</p><h1>Source Registry</h1></div><div class="header-actions"><button id="load-catalog" class="button ghost" type="button">Broncatalogus</button><button id="bootstrap" class="button secondary" type="button">Supported bronnen toevoegen</button><button id="refresh" class="button secondary" type="button">Vernieuwen</button></div></header>
    <main id="content" class="workspace">
      <section class="page-heading"><div><p class="eyebrow">Admin workspace</p><h2>Bronnen beheren & uitvoeren</h2><p>Beheer intelligencebronnen, bootstrap code-reviewed feeds en voer ingeschakelde JSON-bronnen uit via de pinned-HTTPS egress boundary.</p></div><span id="status" class="status-pill neutral" role="status" aria-live="polite">Niet verbonden</span></section>
      <section class="kpi-grid" aria-label="Bronstatus"><article class="kpi-card"><span class="kpi-label">Registry</span><strong id="kpi-total">—</strong><small>Geregistreerde bronnen</small></article><article class="kpi-card"><span class="kpi-label">Actief</span><strong id="kpi-active">—</strong><small>Ingeschakelde definities</small></article><article class="kpi-card"><span class="kpi-label">Catalogus</span><strong id="kpi-catalog">—</strong><small>Gecureerde bronnen</small></article><article class="kpi-card"><span class="kpi-label">Direct ondersteund</span><strong id="kpi-supported">—</strong><small>Generic rc9 adapters</small></article></section>
      <div class="content-grid equal">
        <article class="surface">
          <div class="surface-header"><div><p class="eyebrow">Registry</p><h3>Operationele bronnen</h3></div></div>
          <div id="source-list" class="source-list"><p class="muted">Nog niet geladen.</p></div>
        </article>
        <article class="surface">
          <div class="surface-header"><div><p class="eyebrow">Catalogus</p><h3>Relevante intelligencebronnen</h3></div></div>
          <p class="muted">Catalog membership is geen trust- of publication approval. Alleen <em>supported</em> JSON-profielen zijn in rc9 direct uitvoerbaar; andere officiële bronnen staan klaar voor volgende parser-adapters.</p>
          <div id="catalog-list" class="catalog-list"><p class="muted">Klik op ‘Broncatalogus’ om de gecureerde inventaris te laden.</p></div>
        </article>
      </div>
      <div class="content-grid equal">
        <article class="surface">
          <div class="surface-header"><div><p class="eyebrow">Nieuwe bron</p><h3>Registreren</h3></div></div>
          <form id="source-form" class="form-grid">
            <label>Source ID<input id="source-id" required pattern="[a-z0-9_-]+" placeholder="sector-feed"></label>
            <label>Naam<input id="source-name" required placeholder="Sector advisory feed"></label>
            <label>Type<select id="source-type"><option value="json-feed">JSON feed</option><option value="cisa-kev">CISA KEV</option></select></label>
            <label>Betrouwbaarheid<select id="source-reliability"><option>authoritative</option><option>high</option><option selected>medium</option><option>low</option></select></label>
            <label class="span-2">HTTPS endpoint<input id="source-url" type="url" required placeholder="https://example.org/feed.json"></label>
            <label>Interval (sec)<input id="source-interval" type="number" min="60" max="86400" value="3600"></label>
            <label>Secret reference<input id="source-secret" placeholder="vault://dtmo/source/key"></label>
            <label class="toggle-row"><input id="source-enabled" type="checkbox"> Direct inschakelen</label>
            <button class="button primary" type="submit">Bron registreren</button>
          </form>
        </article>
        <article class="surface">
          <div class="surface-header"><div><p class="eyebrow">Runtime security</p><h3>Outbound source boundary</h3></div></div>
          <div class="governance-summary">
            <div class="governance-item"><span class="governance-icon">1</span><div><strong>DNS validation + pinning</strong><p>Elke run resolveert opnieuw; elk antwoord moet globaal routeerbaar zijn en de TLS-connectie wordt aan het gevalideerde IP gepind met originele hostname/SNI.</p></div></div>
            <div class="governance-item"><span class="governance-icon">2</span><div><strong>Geen redirects/proxies</strong><p>Alleen directe HTTPS:443 GET; redirects zijn fail-closed en het pad gebruikt geen environment proxy.</p></div></div>
            <div class="governance-item"><span class="governance-icon">3</span><div><strong>Bounded JSON</strong><p>Alleen JSON content en maximaal 5 MiB per response. Onbekende feeds moeten het DTMO JSON v1 contract volgen.</p></div></div>
            <div class="governance-item"><span class="governance-icon">4</span><div><strong>Health + governance</strong><p>Failures voeden isolation/alerting; records blijven candidates met aparte review en menselijke share approval.</p></div></div>
          </div>
        </article>
      </div>
      <article class="surface"><div class="surface-header"><div><p class="eyebrow">Identity</p><h3>Lokale testidentiteit</h3></div></div><div class="form-grid three"><label>Subject<input id="subject" value="admin-tester"></label><label>Rollen<input id="roles" value="admin"></label><label>API key<input id="api-key" type="password"></label><button id="save-identity" class="button secondary" type="button">Identiteit toepassen</button></div><p class="muted">Alleen local/dev/staging; waarden blijven in <code>sessionStorage</code>. Production vereist bearer-token authenticatie.</p></article>
    </main>
  </div>
</div>
<script src="/ui/admin-sources.js" defer></script>
</body></html>"""

_CSS = """
.admin-shell{min-height:100vh;display:grid;grid-template-columns:250px minmax(0,1fr)}.source-list,.catalog-list{display:grid;gap:.75rem}.source-card,.catalog-card{border:1px solid var(--line);border-radius:12px;padding:1rem;background:var(--surface-2)}.source-card header,.catalog-card header{display:flex;justify-content:space-between;gap:1rem;align-items:start}.source-meta,.catalog-meta{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.45rem;margin-top:.8rem}.source-meta span,.catalog-meta span{color:var(--muted);font-size:.9rem}.source-actions{display:flex;gap:.5rem;flex-wrap:wrap;margin-top:.9rem}.muted{color:var(--muted)}select{background:var(--surface-2);color:var(--text);border:1px solid var(--line);border-radius:9px;padding:.68rem .75rem}.toggle-row{display:flex;align-items:center;gap:.55rem}.toggle-row input{width:auto}.sidebar-footer p{font-size:.82rem;color:var(--muted);line-height:1.45}.header-actions{display:flex;gap:.5rem;flex-wrap:wrap}.app-header{position:sticky;top:0;z-index:5}.catalog-card p{margin:.65rem 0 0;color:var(--muted);line-height:1.45}@media(max-width:850px){.admin-shell{display:block}.sidebar{position:relative;height:auto}.source-meta,.catalog-meta{grid-template-columns:1fr}.header-actions{justify-content:flex-start}}
"""

_JS = r"""
const byId=(id)=>document.getElementById(id);
const session={subject:sessionStorage.getItem('dtmo.subject')||'admin-tester',roles:sessionStorage.getItem('dtmo.roles')||'admin',apiKey:sessionStorage.getItem('dtmo.apiKey')||''};
function headers(json=false){const h={'X-DTMO-Subject':session.subject,'X-DTMO-Roles':session.roles,'X-DTMO-API-Key':session.apiKey,'X-Request-ID':crypto.randomUUID()};if(json)h['Content-Type']='application/json';return h}
function setStatus(text,kind='neutral'){const el=byId('status');el.textContent=text;el.className=`status-pill ${kind}`}
async function api(path,options={}){const response=await fetch(path,{...options,headers:{...headers(Boolean(options.body)),...(options.headers||{})}});let payload={};try{payload=await response.json()}catch{}if(!response.ok)throw new Error(payload.detail||`HTTP ${response.status}`);return payload}
function escapeHtml(value){return String(value).replace(/[&<>'"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]))}
async function load(){setStatus('Bronnen laden…','loading');try{const sources=await api('/api/v1/admin/sources');render(sources);setStatus('Admin registry verbonden','good')}catch(err){setStatus(`Laden mislukt: ${err.message}`,'bad');byId('source-list').innerHTML='<p class="muted">Geen registrydata beschikbaar.</p>'}}
function render(sources){byId('kpi-total').textContent=sources.length;byId('kpi-active').textContent=sources.filter(s=>s.enabled).length;byId('source-list').innerHTML=sources.length?sources.map(s=>`<article class="source-card"><header><div><strong>${escapeHtml(s.name)}</strong><div class="muted">${escapeHtml(s.id)}</div></div><span class="status-pill ${s.enabled?'good':'neutral'}">${s.enabled?'Actief':'Uit'}</span></header><div class="source-meta"><span>Type: ${escapeHtml(s.source_type)}</span><span>Reliability: ${escapeHtml(s.reliability)}</span><span>Interval: ${s.interval_seconds}s</span><span>Secret: ${s.secret_ref?'reference configured':'geen'}</span><span style="grid-column:1/-1">${escapeHtml(s.endpoint_url)}</span></div><div class="source-actions"><button class="button secondary" data-validate="${escapeHtml(s.id)}">Valideren</button><button class="button secondary" data-run="${escapeHtml(s.id)}" ${!s.enabled||s.source_type==='cisa-kev'?'disabled':''}>Nu uitvoeren</button><button class="button ghost" data-toggle="${escapeHtml(s.id)}" data-enabled="${s.enabled}">${s.enabled?'Uitschakelen':'Inschakelen'}</button></div></article>`).join(''):'<p class="muted">Nog geen bronnen geregistreerd.</p>';document.querySelectorAll('[data-validate]').forEach(b=>b.addEventListener('click',()=>validateSource(b.dataset.validate)));document.querySelectorAll('[data-run]').forEach(b=>b.addEventListener('click',()=>runSource(b.dataset.run)));document.querySelectorAll('[data-toggle]').forEach(b=>b.addEventListener('click',()=>toggleSource(b.dataset.toggle,b.dataset.enabled!=='true')))}
async function loadCatalog(){setStatus('Catalogus laden…','loading');try{const sources=await api('/api/v1/admin/sources/catalog');byId('kpi-catalog').textContent=sources.length;byId('kpi-supported').textContent=sources.filter(s=>s.execution_status==='supported').length;byId('catalog-list').innerHTML=sources.map(s=>`<article class="catalog-card"><header><div><strong>${escapeHtml(s.name)}</strong><div class="muted">${escapeHtml(s.id)}</div></div><span class="status-pill ${s.execution_status==='supported'?'good':'neutral'}">${escapeHtml(s.execution_status)}</span></header><div class="catalog-meta"><span>${escapeHtml(s.category)}</span><span>${escapeHtml(s.reliability)}</span><span style="grid-column:1/-1">${escapeHtml(s.endpoint_url)}</span></div><p>${escapeHtml(s.provenance_note)}</p></article>`).join('');setStatus('Gecureerde broncatalogus geladen','good')}catch(err){setStatus(`Catalogus mislukt: ${err.message}`,'bad')}}
async function bootstrap(){try{const created=await api('/api/v1/admin/sources/catalog/bootstrap',{method:'POST'});setStatus(`${created.length} supported brondefinities beschikbaar`,'good');await load()}catch(err){setStatus(`Bootstrap mislukt: ${err.message}`,'bad')}}
async function validateSource(id){try{const result=await api(`/api/v1/admin/sources/${encodeURIComponent(id)}/validate`,{method:'POST'});setStatus(result.valid?`${id}: configuratie geldig`:`${id}: ${result.reason}`,result.valid?'good':'bad')}catch(err){setStatus(`Validatie mislukt: ${err.message}`,'bad')}}
async function runSource(id){setStatus(`${id}: ophalen en verwerken…`,'loading');try{const result=await api(`/api/v1/admin/sources/${encodeURIComponent(id)}/run`,{method:'POST'});setStatus(`${id}: ${result.status}; ${result.records} records, ${result.inserted} nieuw, ${result.indexed} geïndexeerd`,result.status==='completed'?'good':'bad')}catch(err){setStatus(`Run mislukt: ${err.message}`,'bad')}}
async function toggleSource(id,enabled){try{await api(`/api/v1/admin/sources/${encodeURIComponent(id)}`,{method:'PATCH',body:JSON.stringify({enabled})});await load()}catch(err){setStatus(`Wijzigen mislukt: ${err.message}`,'bad')}}
byId('source-form').addEventListener('submit',async e=>{e.preventDefault();const payload={id:byId('source-id').value.trim(),name:byId('source-name').value.trim(),source_type:byId('source-type').value,endpoint_url:byId('source-url').value.trim(),enabled:byId('source-enabled').checked,interval_seconds:Number(byId('source-interval').value),reliability:byId('source-reliability').value,secret_ref:byId('source-secret').value.trim()||null};try{await api('/api/v1/admin/sources',{method:'POST',body:JSON.stringify(payload)});e.target.reset();byId('source-interval').value='3600';setStatus('Bron geregistreerd','good');await load()}catch(err){setStatus(`Registratie mislukt: ${err.message}`,'bad')}});
byId('refresh').addEventListener('click',load);byId('load-catalog').addEventListener('click',loadCatalog);byId('bootstrap').addEventListener('click',bootstrap);byId('save-identity').addEventListener('click',()=>{session.subject=byId('subject').value.trim();session.roles=byId('roles').value.trim();session.apiKey=byId('api-key').value;sessionStorage.setItem('dtmo.subject',session.subject);sessionStorage.setItem('dtmo.roles',session.roles);sessionStorage.setItem('dtmo.apiKey',session.apiKey);load()});byId('subject').value=session.subject;byId('roles').value=session.roles;byId('api-key').value=session.apiKey;load();loadCatalog();
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

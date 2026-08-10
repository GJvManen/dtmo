from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import HTMLResponse, Response

router = APIRouter()

_PAGE = """<!doctype html>
<html lang="nl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#08131f">
  <title>DTMO — Operations Workspace</title>
  <link rel="stylesheet" href="/ui/design-system.css">
  <link rel="stylesheet" href="/ui/operations.css">
</head>
<body>
<a class="skip-link" href="#main">Ga naar hoofdinhoud</a>
<div class="ops-shell">
  <aside class="ops-sidebar" aria-label="Operations navigatie">
    <div class="ops-brand"><span class="ops-logo" aria-hidden="true">D</span><div><strong>DTMO</strong><small>Operations Workspace</small></div></div>
    <nav class="ops-nav">
      <a class="ops-nav-item active" href="/ui/operations"><span aria-hidden="true">◫</span>Command center</a>
      <a class="ops-nav-item" href="/#intelligence"><span aria-hidden="true">⌕</span>Intelligence</a>
      <a class="ops-nav-item" href="/ui/admin-sources"><span aria-hidden="true">◆</span>Sources</a>
      <a class="ops-nav-item" href="/#governance"><span aria-hidden="true">✓</span>Governance</a>
      <a class="ops-nav-item" href="/#audit"><span aria-hidden="true">≡</span>Audit</a>
    </nav>
    <div class="ops-sidebar-group">
      <span>Role workspaces</span>
      <a href="/ui/analyst-search">Analyst</a><a href="/ui/share-approval">Share approval</a><a href="/ui/auditor">Auditor</a><a href="/ui/ciso-security">CISO</a>
    </div>
    <div class="ops-sidebar-footer"><span class="ops-live-dot"></span><span id="sidebar-health">Runtime controleren…</span></div>
  </aside>

  <div class="ops-app">
    <header class="ops-header">
      <div><p class="ops-breadcrumb">Operations / Command center</p><h1>Security Operations</h1></div>
      <div class="ops-actions">
        <button id="command-button" class="ops-command" type="button" aria-haspopup="dialog"><span>⌘K</span> Command palette</button>
        <button id="refresh" class="button secondary" type="button">Vernieuwen</button>
        <button id="notifications" class="ops-icon-button" type="button" aria-label="Meldingen openen">●<span id="notification-count">0</span></button>
      </div>
    </header>

    <main id="main" class="ops-workspace">
      <section class="ops-hero" aria-labelledby="ops-title">
        <div><p class="eyebrow">Unified operational picture</p><h2 id="ops-title">Command center</h2><p>Een geconsolideerd beeld van runtime, connectors, ingestion, search en governance. RC10.1 introduceert het professionele workspace-framework; diepere dashboards volgen in afzonderlijke bounded runs.</p></div>
        <div class="ops-health" id="overall-health"><span class="ops-health-dot"></span><div><strong>Controleren</strong><small>Platform health</small></div></div>
      </section>

      <nav class="ops-tabs" aria-label="Command center views">
        <button class="ops-tab active" data-panel="overview" type="button">Overview</button>
        <button class="ops-tab" data-panel="intelligence" type="button">Intelligence</button>
        <button class="ops-tab" data-panel="connectors" type="button">Connectors</button>
        <button class="ops-tab" data-panel="governance" type="button">Governance</button>
      </nav>

      <section id="overview" class="ops-panel active" aria-label="Operations overview">
        <div class="ops-kpi-grid">
          <article class="ops-kpi"><span>API</span><strong id="kpi-api">—</strong><small id="kpi-version">Versie onbekend</small></article>
          <article class="ops-kpi"><span>Environment</span><strong id="kpi-environment">—</strong><small>Runtime context</small></article>
          <article class="ops-kpi"><span>Connectors</span><strong id="kpi-connectors">—</strong><small id="kpi-connectors-note">Status ophalen</small></article>
          <article class="ops-kpi"><span>Publication</span><strong>Human gate</strong><small>Review + share approval</small></article>
        </div>
        <div class="ops-grid ops-grid-2">
          <article class="ops-card"><div class="ops-card-head"><div><p class="eyebrow">Runtime</p><h3>Platform health</h3></div><span id="runtime-chip" class="status-pill loading">Loading</span></div><div id="runtime-list" class="ops-status-list"><div><span>API</span><strong>Controleren…</strong></div><div><span>Scheduler</span><strong>Controleren…</strong></div><div><span>Authentication</span><strong>Controleren…</strong></div></div></article>
          <article class="ops-card"><div class="ops-card-head"><div><p class="eyebrow">Governance</p><h3>Control boundaries</h3></div></div><div class="ops-timeline"><div><span>1</span><p><strong>Analyst review</strong><small>Inhoudelijke beoordeling</small></p></div><div><span>2</span><p><strong>Independent share approval</strong><small>Self-approval server-side geblokkeerd</small></p></div><div><span>3</span><p><strong>Audit evidence</strong><small>Append-only decision trail</small></p></div></div></article>
        </div>
        <div class="ops-grid ops-grid-3">
          <article class="ops-card ops-chart-card"><div class="ops-card-head"><div><p class="eyebrow">Ingestion</p><h3>Pipeline</h3></div><span class="ops-badge">RC10.2</span></div><div class="ops-placeholder-chart"><span style="height:36%"></span><span style="height:62%"></span><span style="height:50%"></span><span style="height:82%"></span><span style="height:70%"></span><span style="height:88%"></span><span style="height:76%"></span></div><p>Grafische throughput- en latencydata wordt in de volgende dashboard-run aan echte metrics gekoppeld.</p></article>
          <article class="ops-card"><div class="ops-card-head"><div><p class="eyebrow">Sources</p><h3>Connector status</h3></div><a href="/ui/admin-sources">Beheren</a></div><div id="connector-list" class="ops-status-list"><div><span>Loading</span><strong>—</strong></div></div></article>
          <article class="ops-card"><div class="ops-card-head"><div><p class="eyebrow">Quick actions</p><h3>Werkruimtes</h3></div></div><div class="ops-quick-actions"><a href="/#intelligence">Search intelligence <span>→</span></a><a href="/ui/admin-sources">Manage sources <span>→</span></a><a href="/ui/share-approval">Share approval <span>→</span></a><a href="/ui/auditor">Audit evidence <span>→</span></a></div></article>
        </div>
      </section>

      <section id="intelligence" class="ops-panel" aria-label="Intelligence workspace summary"><article class="ops-card ops-empty"><p class="eyebrow">RC10.3</p><h3>Threat Intelligence Workspace</h3><p>Deze tab wordt in een volgende bounded run gekoppeld aan search, related CVE/KEV/vendor context en investigation timelines.</p><a class="button primary" href="/#intelligence">Open huidige intelligence explorer</a></article></section>
      <section id="connectors" class="ops-panel" aria-label="Connector workspace summary"><article class="ops-card ops-empty"><p class="eyebrow">Sources</p><h3>Source & Connector Center</h3><p>Bronbeheer, catalogus en veilige registered-source execution zijn al beschikbaar in de bestaande admin-workspace.</p><a class="button primary" href="/ui/admin-sources">Open Source Registry</a></article></section>
      <section id="governance" class="ops-panel" aria-label="Governance workspace summary"><article class="ops-card ops-empty"><p class="eyebrow">Governance</p><h3>Decision & assurance controls</h3><p>Review, share approval, audit en CISO-controls blijven afzonderlijke server-side geautoriseerde werkstromen.</p><a class="button primary" href="/#governance">Open governance workspace</a></article></section>
    </main>
  </div>
</div>

<dialog id="command-dialog" class="ops-dialog"><div class="ops-dialog-frame"><div class="ops-dialog-head"><div><p class="eyebrow">Command palette</p><h2>Ga naar…</h2></div><button id="close-command" class="ops-icon-button" type="button" aria-label="Sluiten">×</button></div><input id="command-search" placeholder="Zoek workspace of actie…" autocomplete="off"><div id="command-results" class="ops-command-list"></div></div></dialog>
<aside id="notification-drawer" class="ops-drawer" hidden aria-label="Meldingen"><div class="ops-drawer-head"><h2>Operational notifications</h2><button id="close-notifications" class="ops-icon-button" type="button">×</button></div><div id="notification-list"><p class="ops-muted">Geen actieve meldingen.</p></div></aside>
<script src="/ui/operations.js" defer></script>
</body></html>"""

_CSS = """
:root{--ops-bg:#07111c;--ops-panel:#0d1a29;--ops-panel-2:#102238;--ops-line:#20384f;--ops-muted:#8fa5ba;--ops-accent:#55b7ff;--ops-good:#42d49a;--ops-warn:#f2c75c;--ops-bad:#ff7181}body{background:var(--ops-bg)}.ops-shell{min-height:100vh;display:grid;grid-template-columns:260px minmax(0,1fr)}.ops-sidebar{position:sticky;top:0;height:100vh;padding:1.25rem;background:#081522;border-right:1px solid #162b3e;display:flex;flex-direction:column;gap:1.4rem}.ops-brand{display:flex;gap:.75rem;align-items:center}.ops-brand div{display:flex;flex-direction:column}.ops-brand small,.ops-sidebar-group span,.ops-muted{color:var(--ops-muted)}.ops-logo{display:grid;place-items:center;width:38px;height:38px;border-radius:11px;background:#168ee0;color:white;font-weight:800}.ops-nav,.ops-sidebar-group{display:grid;gap:.35rem}.ops-nav-item,.ops-sidebar-group a{padding:.7rem .75rem;border-radius:9px;text-decoration:none;color:#c9d8e6}.ops-nav-item{display:flex;gap:.7rem}.ops-nav-item:hover,.ops-nav-item.active,.ops-sidebar-group a:hover{background:#11263a;color:#fff}.ops-sidebar-group{margin-top:auto}.ops-sidebar-group span{font-size:.72rem;text-transform:uppercase;letter-spacing:.08em;padding:.25rem .75rem}.ops-sidebar-footer{display:flex;align-items:center;gap:.5rem;color:var(--ops-muted);font-size:.82rem}.ops-live-dot,.ops-health-dot{width:9px;height:9px;border-radius:50%;background:var(--ops-warn);box-shadow:0 0 0 4px rgba(242,199,92,.12)}.ops-app{min-width:0}.ops-header{min-height:82px;padding:1rem 1.5rem;border-bottom:1px solid #162b3e;display:flex;justify-content:space-between;gap:1rem;align-items:center;background:rgba(7,17,28,.92);position:sticky;top:0;z-index:20;backdrop-filter:blur(12px)}.ops-header h1{margin:.1rem 0;font-size:1.25rem}.ops-breadcrumb{margin:0;color:var(--ops-muted);font-size:.78rem}.ops-actions{display:flex;align-items:center;gap:.65rem}.ops-command,.ops-icon-button{border:1px solid var(--ops-line);background:#0d1a29;color:#dbe9f5;border-radius:9px}.ops-command{padding:.6rem .8rem}.ops-command span{color:var(--ops-muted);margin-right:.45rem}.ops-icon-button{min-width:38px;height:38px}.ops-workspace{padding:1.5rem;max-width:1600px;margin:0 auto}.ops-hero{display:flex;justify-content:space-between;gap:2rem;align-items:end;margin-bottom:1.25rem}.ops-hero h2{font-size:2rem;margin:.2rem 0}.ops-hero p{max-width:800px;color:var(--ops-muted)}.ops-health{display:flex;gap:.7rem;align-items:center;background:var(--ops-panel);border:1px solid var(--ops-line);border-radius:12px;padding:.75rem 1rem;min-width:180px}.ops-health div{display:flex;flex-direction:column}.ops-health small{color:var(--ops-muted)}.ops-tabs{display:flex;gap:.3rem;border-bottom:1px solid var(--ops-line);margin-bottom:1.25rem}.ops-tab{border:0;background:transparent;color:var(--ops-muted);padding:.75rem 1rem;border-bottom:2px solid transparent}.ops-tab.active{color:#fff;border-color:var(--ops-accent)}.ops-panel{display:none}.ops-panel.active{display:block}.ops-kpi-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:1rem;margin-bottom:1rem}.ops-kpi,.ops-card{background:var(--ops-panel);border:1px solid var(--ops-line);border-radius:14px}.ops-kpi{padding:1rem;display:grid;gap:.3rem}.ops-kpi>span,.ops-kpi small{color:var(--ops-muted)}.ops-kpi strong{font-size:1.3rem}.ops-grid{display:grid;gap:1rem;margin-bottom:1rem}.ops-grid-2{grid-template-columns:1.35fr 1fr}.ops-grid-3{grid-template-columns:1.2fr 1fr 1fr}.ops-card{padding:1rem}.ops-card-head{display:flex;justify-content:space-between;gap:1rem;align-items:start;margin-bottom:1rem}.ops-card-head h3{margin:.15rem 0}.ops-card-head a{color:var(--ops-accent)}.ops-status-list{display:grid;gap:.65rem}.ops-status-list>div{display:flex;justify-content:space-between;gap:1rem;padding:.7rem .75rem;background:#0a1724;border:1px solid #172d42;border-radius:9px}.ops-status-list span{color:var(--ops-muted)}.ops-timeline{display:grid;gap:.9rem}.ops-timeline>div{display:flex;gap:.8rem}.ops-timeline>div>span{display:grid;place-items:center;width:30px;height:30px;border-radius:50%;background:#15314a;color:var(--ops-accent);font-weight:700}.ops-timeline p{display:flex;flex-direction:column;margin:0}.ops-timeline small{color:var(--ops-muted)}.ops-placeholder-chart{height:150px;display:flex;align-items:end;gap:.55rem;padding:.75rem;background:#091622;border-radius:10px}.ops-placeholder-chart span{flex:1;min-height:10%;background:linear-gradient(180deg,#55b7ff,#176ca7);border-radius:5px 5px 2px 2px}.ops-chart-card>p,.ops-empty p{color:var(--ops-muted)}.ops-badge{font-size:.72rem;border:1px solid var(--ops-line);border-radius:999px;padding:.25rem .5rem;color:var(--ops-muted)}.ops-quick-actions{display:grid;gap:.55rem}.ops-quick-actions a{display:flex;justify-content:space-between;text-decoration:none;padding:.75rem;background:#0a1724;border:1px solid #172d42;border-radius:9px}.ops-quick-actions a:hover{border-color:#2d648d}.ops-empty{padding:2rem}.ops-dialog{border:0;padding:0;background:transparent;color:inherit;width:min(620px,92vw)}.ops-dialog::backdrop{background:rgba(0,0,0,.6)}.ops-dialog-frame{background:#0b1928;border:1px solid var(--ops-line);border-radius:16px;padding:1rem;box-shadow:0 25px 80px rgba(0,0,0,.45)}.ops-dialog-head,.ops-drawer-head{display:flex;justify-content:space-between;align-items:start}.ops-dialog input{width:100%;padding:.8rem;border:1px solid var(--ops-line);border-radius:9px;background:#081522;color:#fff}.ops-command-list{display:grid;gap:.35rem;margin-top:.7rem}.ops-command-list a{padding:.75rem;text-decoration:none;border-radius:8px}.ops-command-list a:hover,.ops-command-list a:focus{background:#102b43}.ops-drawer{position:fixed;right:0;top:0;z-index:40;width:min(420px,92vw);height:100vh;background:#0b1928;border-left:1px solid var(--ops-line);padding:1rem;box-shadow:-25px 0 80px rgba(0,0,0,.35)}@media(max-width:1050px){.ops-grid-3{grid-template-columns:1fr 1fr}.ops-kpi-grid{grid-template-columns:1fr 1fr}}@media(max-width:760px){.ops-shell{display:block}.ops-sidebar{position:static;height:auto}.ops-sidebar-group{display:none}.ops-nav{grid-template-columns:repeat(3,1fr)}.ops-nav-item:nth-child(n+4){display:none}.ops-header{position:static;align-items:flex-start}.ops-actions{flex-wrap:wrap;justify-content:flex-end}.ops-command{display:none}.ops-hero{align-items:flex-start;flex-direction:column}.ops-kpi-grid,.ops-grid-2,.ops-grid-3{grid-template-columns:1fr}.ops-tabs{overflow:auto}.ops-workspace{padding:1rem}}@media(prefers-reduced-motion:reduce){*{scroll-behavior:auto!important;transition:none!important}}
"""

_JS = """
const byId=(id)=>document.getElementById(id);
const commands=[['Command center','/ui/operations'],['Intelligence explorer','/#intelligence'],['Source Registry','/ui/admin-sources'],['Share approval','/ui/share-approval'],['Audit evidence','/ui/auditor'],['CISO security','/ui/ciso-security'],['API documentation','/docs']];
function setHealth(ok){const el=byId('overall-health');const dot=el.querySelector('.ops-health-dot');el.querySelector('strong').textContent=ok?'Operational':'Degraded';dot.style.background=ok?'var(--ops-good)':'var(--ops-bad)';byId('sidebar-health').textContent=ok?'Runtime operational':'Runtime degraded';}
function renderCommands(query=''){const q=query.toLowerCase();byId('command-results').innerHTML=commands.filter(([name])=>name.toLowerCase().includes(q)).map(([name,url])=>`<a href="${url}">${name}</a>`).join('')||'<p class="ops-muted">Geen resultaten.</p>';}
async function load(){let notifications=[];try{const health=await fetch('/health',{headers:{Accept:'application/json'}});if(!health.ok)throw new Error(`HTTP ${health.status}`);const data=await health.json();byId('kpi-api').textContent=data.status==='healthy'?'Healthy':data.status;byId('kpi-version').textContent=data.version||'—';byId('kpi-environment').textContent=data.environment||'—';byId('runtime-chip').textContent=data.status||'unknown';byId('runtime-chip').className='status-pill '+(data.status==='healthy'?'success':'error');byId('runtime-list').innerHTML=`<div><span>API</span><strong>${data.status||'—'}</strong></div><div><span>Scheduler</span><strong>${data.scheduler?.running?'Running':'Idle'}</strong></div><div><span>Authentication</span><strong>${data.authentication||'—'}</strong></div>`;setHealth(data.status==='healthy');}catch(error){setHealth(false);notifications.push(`Health endpoint: ${error.message}`);}
try{const response=await fetch('/connectors',{headers:{Accept:'application/json'}});if(!response.ok)throw new Error(`HTTP ${response.status}`);const connectors=await response.json();const enabled=connectors.filter(c=>c.enabled).length;byId('kpi-connectors').textContent=`${enabled}/${connectors.length}`;byId('kpi-connectors-note').textContent='Enabled / known';byId('connector-list').innerHTML=connectors.map(c=>`<div><span>${c.id}</span><strong>${c.enabled?'Enabled':'Disabled'}</strong></div>`).join('')||'<div><span>No connectors</span><strong>—</strong></div>';}catch(error){notifications.push(`Connector endpoint: ${error.message}`);}
byId('notification-count').textContent=String(notifications.length);byId('notification-list').innerHTML=notifications.length?notifications.map(n=>`<p>${n}</p>`).join(''):'<p class="ops-muted">Geen actieve meldingen.</p>';}
document.querySelectorAll('.ops-tab').forEach(button=>button.addEventListener('click',()=>{document.querySelectorAll('.ops-tab').forEach(b=>b.classList.remove('active'));document.querySelectorAll('.ops-panel').forEach(p=>p.classList.remove('active'));button.classList.add('active');byId(button.dataset.panel).classList.add('active');}));
const dialog=byId('command-dialog');byId('command-button').addEventListener('click',()=>{renderCommands();dialog.showModal();byId('command-search').focus();});byId('close-command').addEventListener('click',()=>dialog.close());byId('command-search').addEventListener('input',event=>renderCommands(event.target.value));document.addEventListener('keydown',event=>{if((event.metaKey||event.ctrlKey)&&event.key.toLowerCase()==='k'){event.preventDefault();dialog.open?dialog.close():(renderCommands(),dialog.showModal(),byId('command-search').focus());}});
const drawer=byId('notification-drawer');byId('notifications').addEventListener('click',()=>drawer.hidden=false);byId('close-notifications').addEventListener('click',()=>drawer.hidden=true);byId('refresh').addEventListener('click',load);load();
"""

@router.get('/ui/operations', response_class=HTMLResponse)
def operations_workspace() -> HTMLResponse:
    return HTMLResponse(_PAGE)

@router.get('/ui/operations.css')
def operations_css() -> Response:
    return Response(_CSS, media_type='text/css')

@router.get('/ui/operations.js')
def operations_js() -> Response:
    return Response(_JS, media_type='application/javascript')

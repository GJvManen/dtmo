from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import HTMLResponse, Response

router = APIRouter()

_PAGE = """<!doctype html>
<html lang="nl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light dark">
  <title>DTMO — Threat Monitoring Console</title>
  <link rel="stylesheet" href="/ui/console.css">
</head>
<body>
  <a class="skip-link" href="#main">Ga naar hoofdinhoud</a>
  <header class="topbar">
    <div>
      <p class="eyebrow">Dutch Threat Monitoring for Education</p>
      <h1>DTMO Console</h1>
    </div>
    <div class="status-cluster" aria-label="Platformstatus">
      <span id="health-chip" class="chip" data-state="loading">API controleren…</span>
      <span id="identity-chip" class="chip">Niet aangemeld</span>
    </div>
  </header>

  <main id="main" class="shell">
    <section class="hero panel" aria-labelledby="hero-title">
      <div>
        <p class="eyebrow">Governed cyber threat intelligence</p>
        <h2 id="hero-title">Operationeel overzicht</h2>
        <p>Onderzoek intelligence, controleer bronprovenance, volg connectors en voer uitsluitend geautoriseerde menselijke beslissingen uit. Review en externe share approval blijven strikt gescheiden.</p>
      </div>
      <nav class="quick-links" aria-label="Snelle koppelingen">
        <a href="/docs">API-documentatie</a>
        <a href="/ui/analyst-search">Analyst search</a>
        <a href="/ui/share-approval">Share approval</a>
        <a href="/ui/auditor">Audit evidence</a>
        <a href="/ui/ciso-security">CISO security</a>
      </nav>
    </section>

    <section class="grid grid-4" aria-label="Statussamenvatting">
      <article class="metric panel"><span class="metric-label">API</span><strong id="metric-api">—</strong><small id="metric-version">Version onbekend</small></article>
      <article class="metric panel"><span class="metric-label">Environment</span><strong id="metric-environment">—</strong><small>Runtime context</small></article>
      <article class="metric panel"><span class="metric-label">Connector</span><strong id="metric-connectors">—</strong><small>CISA KEV</small></article>
      <article class="metric panel"><span class="metric-label">Publication gate</span><strong id="metric-publication">—</strong><small>Menselijke approval vereist</small></article>
    </section>

    <section class="grid grid-2">
      <article class="panel" aria-labelledby="identity-title">
        <div class="section-heading"><div><p class="eyebrow">Toegang</p><h2 id="identity-title">Testidentiteit</h2></div><button id="clear-identity" class="button secondary" type="button">Wissen</button></div>
        <p class="help">Alleen voor lokale/dev/staging-validatie. Waarden blijven uitsluitend in deze browsertab via sessionStorage. Productie gebruikt de geconfigureerde bearer-token/identity-provider route.</p>
        <form id="identity-form" class="form-grid">
          <label>Subject<input id="subject" autocomplete="off" value="external-tester"></label>
          <label>Rollen<input id="roles" autocomplete="off" value="analyst" aria-describedby="roles-help"></label>
          <small id="roles-help" class="field-help">Komma-gescheiden, bijvoorbeeld analyst, reviewer, share_approver, auditor, ciso.</small>
          <label>DTMO API key<input id="api-key" type="password" autocomplete="off"></label>
          <button class="button primary" type="submit">Identiteit toepassen</button>
        </form>
        <div id="session-state" class="notice" role="status" aria-live="polite">Nog geen sessie gecontroleerd.</div>
      </article>

      <article class="panel" aria-labelledby="connector-title">
        <div class="section-heading"><div><p class="eyebrow">Provenance</p><h2 id="connector-title">Connectorstatus</h2></div><button id="refresh-connectors" class="button secondary" type="button">Vernieuwen</button></div>
        <div id="connector-list" class="stack" aria-live="polite"><p>Connectorstatus wordt geladen…</p></div>
      </article>
    </section>

    <section class="panel" aria-labelledby="search-title">
      <div class="section-heading"><div><p class="eyebrow">Analyse</p><h2 id="search-title">Intelligence zoeken</h2></div><span id="search-permission" class="chip">Permissie onbekend</span></div>
      <form id="search-form" class="searchbar">
        <label class="sr-only" for="search-query">Zoekterm</label>
        <input id="search-query" minlength="2" required autocomplete="off" placeholder="Zoek op dreiging, kwetsbaarheid, actor of leverancier…">
        <button class="button primary" type="submit">Zoeken</button>
      </form>
      <div id="search-status" class="notice" role="status" aria-live="polite">Voer een zoekterm in.</div>
      <div id="search-results" class="results" aria-live="polite"></div>
    </section>

    <section class="grid grid-2">
      <article class="panel" aria-labelledby="decision-title">
        <p class="eyebrow">Governance</p><h2 id="decision-title">Review & share decision</h2>
        <p class="help">Dezelfde principal mag niet zowel review als share approval voor hetzelfde item uitvoeren.</p>
        <label>Intelligence item ID<input id="decision-item" autocomplete="off"></label>
        <div class="button-row">
          <button id="review-action" class="button secondary" type="button">Mark reviewed</button>
          <button id="share-action" class="button danger" type="button">Approve external sharing</button>
        </div>
        <pre id="decision-result" class="console-output" aria-live="polite">Nog geen beslissing uitgevoerd.</pre>
      </article>

      <article class="panel" aria-labelledby="audit-title">
        <div class="section-heading"><div><p class="eyebrow">Auditability</p><h2 id="audit-title">Read-only audit evidence</h2></div><button id="load-audit" class="button secondary" type="button">Laden</button></div>
        <p class="help">Deze weergave is uitsluitend read-only.</p>
        <div id="audit-status" class="notice" role="status" aria-live="polite">Nog niet geladen.</div>
        <ol id="audit-events" class="audit-list"></ol>
      </article>
    </section>

    <section class="panel" aria-labelledby="security-title">
      <p class="eyebrow">Security operations</p><h2 id="security-title">CISO token revocation</h2>
      <form id="revocation-form" class="form-grid three">
        <label>Token identifier (JTI)<input id="token-jti" autocomplete="off"></label>
        <label>Expiry (ISO 8601)<input id="token-expiry" autocomplete="off" placeholder="2026-08-10T15:00:00Z"></label>
        <label>Reden<input id="revocation-reason" autocomplete="off"></label>
        <button class="button danger" type="submit">Token intrekken</button>
      </form>
      <div id="revocation-status" class="notice" role="status" aria-live="polite">Alleen beschikbaar voor een menselijke principal met revoke:tokens.</div>
    </section>
  </main>

  <footer class="footer">
    <span>DTMO 16.0.0rc5</span>
    <span>RBAC · provenance · privacy · auditability · human share approval</span>
  </footer>
  <script src="/ui/console.js" defer></script>
</body>
</html>
"""

_CSS = """
:root { --bg:#08111f; --panel:#0e1b2e; --panel2:#13233a; --text:#edf4ff; --muted:#9fb1c9; --line:#27405f; --accent:#55b8ff; --accent2:#89d1ff; --good:#6ee7a8; --warn:#ffd166; --bad:#ff7b7b; --focus:#fff3a3; font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; color-scheme:dark; }
* { box-sizing:border-box; }
body { margin:0; background:radial-gradient(circle at top,#102744 0,#08111f 45%); color:var(--text); min-height:100vh; }
a { color:var(--accent2); }
a:focus-visible, button:focus-visible, input:focus-visible { outline:3px solid var(--focus); outline-offset:3px; }
.skip-link { position:absolute; left:-9999px; top:1rem; background:#fff; color:#000; padding:.8rem; z-index:99; }
.skip-link:focus { left:1rem; }
.topbar { display:flex; justify-content:space-between; gap:1rem; align-items:center; padding:1.5rem clamp(1rem,4vw,4rem); border-bottom:1px solid var(--line); background:rgba(8,17,31,.88); backdrop-filter:blur(12px); position:sticky; top:0; z-index:10; }
h1,h2,p { margin-top:0; } h1 { margin-bottom:0; font-size:clamp(1.6rem,4vw,2.3rem); } h2 { font-size:1.25rem; margin-bottom:.75rem; }
.eyebrow { color:var(--accent2); text-transform:uppercase; letter-spacing:.12em; font-size:.72rem; font-weight:800; margin-bottom:.35rem; }
.shell { width:min(1320px,calc(100% - 2rem)); margin:1.5rem auto 3rem; display:grid; gap:1rem; }
.panel { background:linear-gradient(180deg,rgba(19,35,58,.97),rgba(14,27,46,.97)); border:1px solid var(--line); border-radius:16px; padding:1.2rem; box-shadow:0 18px 50px rgba(0,0,0,.18); }
.hero { display:grid; grid-template-columns:minmax(0,2fr) minmax(260px,1fr); gap:1.5rem; align-items:center; }
.hero p { color:var(--muted); max-width:72ch; }
.quick-links { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:.55rem; }
.quick-links a { text-decoration:none; border:1px solid var(--line); background:#0a1728; padding:.7rem; border-radius:10px; font-weight:700; }
.grid { display:grid; gap:1rem; }.grid-4 { grid-template-columns:repeat(4,minmax(0,1fr)); }.grid-2 { grid-template-columns:repeat(2,minmax(0,1fr)); }
.metric { display:grid; gap:.3rem; }.metric strong { font-size:1.45rem; }.metric-label,.metric small,.help,.field-help { color:var(--muted); }
.status-cluster,.button-row,.section-heading { display:flex; gap:.65rem; align-items:center; flex-wrap:wrap; }.section-heading { justify-content:space-between; }
.chip { display:inline-flex; align-items:center; min-height:2rem; padding:.25rem .65rem; border:1px solid var(--line); border-radius:999px; color:var(--muted); font-size:.82rem; font-weight:700; }.chip[data-state="success"]{color:var(--good);border-color:#2b7650}.chip[data-state="error"]{color:var(--bad);border-color:#833f49}.chip[data-state="loading"]{color:var(--warn)}
.form-grid { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:.8rem; }.form-grid.three { grid-template-columns:repeat(3,minmax(0,1fr)); }.form-grid .button,.form-grid .field-help { align-self:end; }
label { display:grid; gap:.35rem; font-weight:700; color:#d8e6f8; } input { width:100%; border:1px solid #365372; border-radius:9px; background:#071321; color:var(--text); padding:.72rem .8rem; font:inherit; }
.button { border:1px solid transparent; border-radius:9px; padding:.7rem .9rem; font:inherit; font-weight:800; cursor:pointer; }.primary { background:var(--accent); color:#06111e; }.secondary { background:#172c46; border-color:#365372; color:var(--text); }.danger { background:#8f3340; color:#fff; }.button:disabled { opacity:.45; cursor:not-allowed; }
.notice { margin-top:.8rem; border-left:4px solid var(--line); background:#081522; padding:.75rem .85rem; color:var(--muted); border-radius:6px; }.notice[data-state="success"]{border-color:var(--good);color:#b9f6d5}.notice[data-state="error"]{border-color:var(--bad);color:#ffc2c2}.notice[data-state="loading"]{border-color:var(--warn)}
.searchbar { display:grid; grid-template-columns:1fr auto; gap:.7rem; }.results { display:grid; gap:.7rem; margin-top:.9rem; }.result-card { border:1px solid var(--line); border-radius:10px; padding:.85rem; background:#0a1728; }.result-card h3 { margin:0 0 .4rem; }.result-meta { display:flex; gap:.5rem; flex-wrap:wrap; color:var(--muted); font-size:.82rem; }
.console-output { min-height:7rem; white-space:pre-wrap; overflow-wrap:anywhere; background:#06101d; border:1px solid var(--line); border-radius:10px; padding:.8rem; color:#cce2ff; }
.audit-list { display:grid; gap:.6rem; padding-left:1.35rem; max-height:22rem; overflow:auto; }.audit-list li { padding:.65rem; border:1px solid var(--line); border-radius:8px; }.audit-list code { overflow-wrap:anywhere; color:var(--muted); }
.stack { display:grid; gap:.6rem; }.stack-row { display:flex; justify-content:space-between; gap:1rem; border-bottom:1px solid var(--line); padding:.55rem 0; }
.footer { display:flex; justify-content:space-between; gap:1rem; flex-wrap:wrap; width:min(1320px,calc(100% - 2rem)); margin:0 auto 2rem; color:var(--muted); font-size:.8rem; }
.sr-only { position:absolute; width:1px; height:1px; padding:0; margin:-1px; overflow:hidden; clip:rect(0,0,0,0); white-space:nowrap; border:0; }
@media (max-width:900px){ .grid-4,.grid-2,.hero,.form-grid,.form-grid.three { grid-template-columns:1fr; }.topbar { position:static; align-items:flex-start; }.quick-links { grid-template-columns:1fr 1fr; } }
@media (max-width:540px){ .quick-links,.searchbar { grid-template-columns:1fr; }.shell { width:min(100% - 1rem,1320px); }.topbar { padding:1rem; } }
@media (prefers-reduced-motion:reduce){ *,*::before,*::after { scroll-behavior:auto!important; transition:none!important; animation:none!important; } }
"""

_SCRIPT = r"""(() => {
  const $ = (id) => document.getElementById(id);
  const storageKey = 'dtmo-console-identity-v1';
  let session = null;

  function identity() {
    try { return JSON.parse(sessionStorage.getItem(storageKey) || '{}'); } catch (_) { return {}; }
  }
  function headers(extra = {}) {
    const value = identity();
    const result = {...extra};
    if (value.subject) result['X-DTMO-Subject'] = value.subject;
    if (value.roles) result['X-DTMO-Roles'] = value.roles;
    if (value.apiKey) result['X-DTMO-API-Key'] = value.apiKey;
    return result;
  }
  async function request(url, options = {}) {
    const response = await fetch(url, {...options, credentials:'same-origin', headers:headers(options.headers || {})});
    let body;
    try { body = await response.json(); } catch (_) { body = null; }
    if (!response.ok) throw new Error((body && body.detail) || `${response.status} ${response.statusText}`);
    return body;
  }
  function state(element, message, status) { element.textContent = message; element.dataset.state = status || ''; }
  function permitted(permission) { return Boolean(session && session.permissions && session.permissions.includes(permission)); }
  function applyPermissions() {
    $('search-permission').textContent = permitted('read:intelligence') ? 'Search toegestaan' : 'Search niet toegestaan';
    $('search-permission').dataset.state = permitted('read:intelligence') ? 'success' : 'error';
    $('review-action').disabled = !permitted('review:intelligence');
    $('share-action').disabled = !permitted('approve:share');
    $('load-audit').disabled = !permitted('read:audit');
    $('revocation-form').querySelector('button').disabled = !(permitted('revoke:tokens') && !session?.service_account);
  }
  async function loadHealth() {
    try {
      const body = await request('/health');
      state($('health-chip'), 'API healthy', 'success');
      $('metric-api').textContent = body.status || 'healthy';
      $('metric-version').textContent = `Version ${body.version || 'onbekend'}`;
      $('metric-environment').textContent = body.environment || 'onbekend';
      $('metric-publication').textContent = body.publication_gate === 'human-approval-required' ? 'Human approval' : String(body.publication_gate || '—');
    } catch (error) {
      state($('health-chip'), `API fout: ${error.message}`, 'error');
      $('metric-api').textContent = 'unavailable';
    }
  }
  async function loadSession() {
    try {
      session = await request('/api/v1/ui/session');
      state($('session-state'), `${session.subject} — ${session.roles.join(', ') || 'geen rollen'}`, 'success');
      $('identity-chip').textContent = session.subject;
      $('identity-chip').dataset.state = 'success';
      applyPermissions();
    } catch (error) {
      session = null;
      state($('session-state'), `Authenticatie mislukt: ${error.message}`, 'error');
      $('identity-chip').textContent = 'Niet aangemeld';
      $('identity-chip').dataset.state = 'error';
      applyPermissions();
    }
  }
  async function loadConnectors() {
    const container = $('connector-list');
    container.textContent = 'Laden…';
    try {
      const items = await request('/connectors');
      container.replaceChildren();
      for (const item of items) {
        const row = document.createElement('div'); row.className = 'stack-row';
        const left = document.createElement('div');
        const title = document.createElement('strong'); title.textContent = item.id;
        const detail = document.createElement('div'); detail.className = 'field-help'; detail.textContent = `${item.reliability} · ${item.schedule_seconds}s`;
        left.append(title, detail);
        const chip = document.createElement('span'); chip.className = 'chip'; chip.textContent = item.enabled ? 'enabled' : 'disabled'; chip.dataset.state = item.enabled ? 'success' : '';
        row.append(left, chip); container.appendChild(row);
      }
      $('metric-connectors').textContent = items.some((item) => item.enabled) ? 'enabled' : 'disabled';
    } catch (error) { container.textContent = `Connectorstatus niet beschikbaar: ${error.message}`; $('metric-connectors').textContent = 'error'; }
  }
  async function search(event) {
    event.preventDefault();
    const query = $('search-query').value.trim();
    if (query.length < 2) return;
    const status = $('search-status'); const results = $('search-results');
    results.replaceChildren(); state(status, 'Zoeken…', 'loading');
    try {
      const body = await request(`/api/v1/intelligence/search?q=${encodeURIComponent(query)}`);
      for (const item of body.results || []) {
        const card = document.createElement('article'); card.className = 'result-card';
        const title = document.createElement('h3'); title.textContent = String(item.title || 'Untitled intelligence');
        const summary = document.createElement('p'); summary.textContent = String(item.summary || 'Geen samenvatting beschikbaar.');
        const meta = document.createElement('div'); meta.className = 'result-meta';
        for (const value of [item.id, item.source, item.confidence].filter(Boolean)) { const span = document.createElement('span'); span.textContent = String(value); meta.appendChild(span); }
        card.append(title, summary, meta); results.appendChild(card);
      }
      state(status, `${body.count || 0} resultaat/resultaten.`, 'success');
    } catch (error) { state(status, `Zoeken mislukt: ${error.message}`, 'error'); }
  }
  async function decision(action) {
    const id = $('decision-item').value.trim(); if (!id) { $('decision-result').textContent = 'Item ID is verplicht.'; return; }
    try {
      const body = await request(`/api/v1/intelligence/${encodeURIComponent(id)}/${action}`, {method:'POST', headers:{'X-Request-ID':crypto.randomUUID()}});
      $('decision-result').textContent = JSON.stringify(body, null, 2);
    } catch (error) { $('decision-result').textContent = `Beslissing mislukt: ${error.message}`; }
  }
  async function loadAudit() {
    const list = $('audit-events'); list.replaceChildren(); state($('audit-status'), 'Audit evidence laden…', 'loading');
    try {
      const body = await request('/api/v1/audit/events?limit=25');
      for (const item of body.events || []) {
        const li = document.createElement('li');
        const strong = document.createElement('strong'); strong.textContent = `${item.action} — ${item.decision}`;
        const detail = document.createElement('div'); detail.textContent = `${item.principal} · ${item.resource}`;
        const hash = document.createElement('code'); hash.textContent = item.event_hash;
        li.append(strong, detail, hash); list.appendChild(li);
      }
      state($('audit-status'), `${body.count || 0} event(s) read-only geladen.`, 'success');
    } catch (error) { state($('audit-status'), `Audit evidence niet beschikbaar: ${error.message}`, 'error'); }
  }
  async function revoke(event) {
    event.preventDefault(); state($('revocation-status'), 'Token intrekken…', 'loading');
    try {
      const body = await request('/api/v1/security/tokens/revoke', {method:'POST', headers:{'Content-Type':'application/json','X-Request-ID':crypto.randomUUID()}, body:JSON.stringify({jti:$('token-jti').value.trim(), expires_at:$('token-expiry').value.trim(), reason:$('revocation-reason').value.trim()})});
      state($('revocation-status'), `Token ingetrokken. Audit event: ${body.audit_event_id}`, 'success');
    } catch (error) { state($('revocation-status'), `Revocation mislukt: ${error.message}`, 'error'); }
  }
  $('identity-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    sessionStorage.setItem(storageKey, JSON.stringify({subject:$('subject').value.trim(), roles:$('roles').value.trim(), apiKey:$('api-key').value}));
    await loadSession();
  });
  $('clear-identity').addEventListener('click', async () => { sessionStorage.removeItem(storageKey); $('api-key').value=''; await loadSession(); });
  $('refresh-connectors').addEventListener('click', () => void loadConnectors());
  $('search-form').addEventListener('submit', (event) => void search(event));
  $('review-action').addEventListener('click', () => void decision('review'));
  $('share-action').addEventListener('click', () => void decision('share-approval'));
  $('load-audit').addEventListener('click', () => void loadAudit());
  $('revocation-form').addEventListener('submit', (event) => void revoke(event));

  const saved = identity(); if (saved.subject) $('subject').value = saved.subject; if (saved.roles) $('roles').value = saved.roles;
  void Promise.all([loadHealth(), loadConnectors(), loadSession()]);
})();
"""


def _headers(content_type: str) -> dict[str, str]:
    return {
        "Cache-Control": "no-store",
        "Content-Type": content_type,
        "Content-Security-Policy": (
            "default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self'; "
            "img-src 'self'; font-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'"
        ),
    }


@router.get("/", response_class=HTMLResponse, include_in_schema=False)
def console_page() -> HTMLResponse:
    return HTMLResponse(_PAGE, headers=_headers("text/html; charset=utf-8"))


@router.get("/ui/console", response_class=HTMLResponse, include_in_schema=False)
def console_alias() -> HTMLResponse:
    return console_page()


@router.get("/ui/console.css", include_in_schema=False)
def console_css() -> Response:
    return Response(_CSS, media_type="text/css", headers={"Cache-Control": "public, max-age=300"})


@router.get("/ui/console.js", include_in_schema=False)
def console_script() -> Response:
    return Response(_SCRIPT, media_type="application/javascript", headers={"Cache-Control": "no-store"})

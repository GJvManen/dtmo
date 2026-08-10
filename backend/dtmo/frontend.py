from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import HTMLResponse, Response

router = APIRouter()

_PAGE = """<!doctype html>
<html lang="nl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="dark light">
  <meta name="theme-color" content="#07111f">
  <title>DTMO — Threat Operations Console</title>
  <link rel="stylesheet" href="/ui/design-system.css">
</head>
<body>
  <a class="skip-link" href="#workspace">Ga naar hoofdinhoud</a>
  <div class="app-shell">
    <aside class="sidebar" aria-label="Hoofdnavigatie">
      <div class="brand">
        <div class="brand-mark" aria-hidden="true">D</div>
        <div><strong>DTMO</strong><span>Threat Operations</span></div>
      </div>
      <nav class="nav-list" aria-label="Console secties">
        <a class="nav-item active" href="#overview" data-section-link="overview"><span class="nav-icon" aria-hidden="true">◫</span><span>Overzicht</span></a>
        <a class="nav-item" href="#intelligence" data-section-link="intelligence"><span class="nav-icon" aria-hidden="true">⌕</span><span>Intelligence</span></a>
        <a class="nav-item" href="#governance" data-section-link="governance"><span class="nav-icon" aria-hidden="true">✓</span><span>Governance</span></a>
        <a class="nav-item" href="#audit" data-section-link="audit"><span class="nav-icon" aria-hidden="true">≡</span><span>Audit</span></a>
        <a class="nav-item" href="#security" data-section-link="security"><span class="nav-icon" aria-hidden="true">◇</span><span>Security</span></a>
      </nav>
      <div class="sidebar-footer">
        <span class="sidebar-label">Gespecialiseerde views</span>
        <a href="/ui/analyst-search">Analyst workspace</a>
        <a href="/ui/share-approval">Share approval</a>
        <a href="/ui/auditor">Auditor view</a>
        <a href="/ui/ciso-security">CISO security</a>
        <a href="/docs">API-documentatie</a>
      </div>
    </aside>

    <div class="app-main">
      <header class="app-header">
        <div>
          <p class="eyebrow">Dutch Threat Monitoring for Education</p>
          <h1>Threat Operations Console</h1>
        </div>
        <div class="header-actions">
          <span id="health-chip" class="status-pill loading"><span class="status-dot"></span>API controleren</span>
          <button id="open-identity" class="profile-button" type="button" aria-haspopup="dialog">
            <span class="avatar" aria-hidden="true">ET</span>
            <span><strong id="identity-name">External tester</strong><small id="identity-role">Niet verbonden</small></span>
          </button>
        </div>
      </header>

      <main id="workspace" class="workspace">
        <section id="overview" class="workspace-section" aria-labelledby="overview-title">
          <div class="page-heading">
            <div><p class="eyebrow">Operationeel beeld</p><h2 id="overview-title">Overzicht</h2><p>Actuele platformstatus, bronbeschikbaarheid en governance-signalen voor de huidige testcontext.</p></div>
            <button id="refresh-overview" class="button secondary" type="button">Alles vernieuwen</button>
          </div>

          <div class="kpi-grid" aria-label="Platform KPI's">
            <article class="kpi-card"><div class="kpi-top"><span class="kpi-icon good" aria-hidden="true">●</span><span class="kpi-label">API status</span></div><strong id="metric-api">Controleren…</strong><small id="metric-version">Versie onbekend</small></article>
            <article class="kpi-card"><div class="kpi-top"><span class="kpi-icon" aria-hidden="true">◆</span><span class="kpi-label">Environment</span></div><strong id="metric-environment">—</strong><small>Runtime context</small></article>
            <article class="kpi-card"><div class="kpi-top"><span class="kpi-icon" aria-hidden="true">↻</span><span class="kpi-label">Connectors</span></div><strong id="metric-connectors">—</strong><small>CISA KEV status</small></article>
            <article class="kpi-card"><div class="kpi-top"><span class="kpi-icon warn" aria-hidden="true">✓</span><span class="kpi-label">Publication gate</span></div><strong id="metric-publication">Human approval</strong><small>Share blijft gescheiden</small></article>
          </div>

          <div class="content-grid two-thirds">
            <article class="surface">
              <div class="surface-header"><div><p class="eyebrow">Bronnen</p><h3>Connector health</h3></div><button id="refresh-connectors" class="icon-button" type="button" aria-label="Connectorstatus vernieuwen">↻</button></div>
              <div id="connector-list" class="connector-list" aria-live="polite"><div class="skeleton-row"></div><div class="skeleton-row"></div></div>
            </article>
            <article class="surface governance-summary">
              <div class="surface-header"><div><p class="eyebrow">Governance</p><h3>Beslisgrenzen</h3></div></div>
              <div class="governance-item"><span class="governance-icon">1</span><div><strong>Review</strong><p>Inhoudelijke beoordeling door geautoriseerde reviewer.</p></div></div>
              <div class="governance-item"><span class="governance-icon">2</span><div><strong>Share approval</strong><p>Aparte menselijke goedkeuring; self-approval blijft verboden.</p></div></div>
              <div class="governance-item"><span class="governance-icon">3</span><div><strong>Audit trail</strong><p>Beslissingen worden herleidbaar en append-only geregistreerd.</p></div></div>
            </article>
          </div>
        </section>

        <section id="intelligence" class="workspace-section" aria-labelledby="intel-title">
          <div class="page-heading"><div><p class="eyebrow">Analyse</p><h2 id="intel-title">Intelligence explorer</h2><p>Doorzoek intelligence op dreiging, kwetsbaarheid, actor, leverancier of gebeurtenis.</p></div><span id="search-permission" class="status-pill neutral">Permissie controleren</span></div>
          <article class="surface search-surface">
            <form id="search-form" class="hero-search">
              <label class="sr-only" for="search-query">Zoek intelligence</label>
              <span class="search-icon" aria-hidden="true">⌕</span>
              <input id="search-query" minlength="2" required autocomplete="off" placeholder="Bijv. ransomware onderwijs, CVE-2026-…, Microsoft 365…">
              <button class="button primary" type="submit">Zoeken</button>
            </form>
            <div id="search-status" class="inline-status" role="status" aria-live="polite">Voer minimaal twee tekens in om te zoeken.</div>
            <div id="search-results" class="intel-results" aria-live="polite"></div>
          </article>
        </section>

        <section id="governance" class="workspace-section" aria-labelledby="governance-title">
          <div class="page-heading"><div><p class="eyebrow">Besluitvorming</p><h2 id="governance-title">Governed decision workspace</h2><p>Review en externe share approval blijven afzonderlijke, autorisatie-gebonden acties.</p></div></div>
          <div class="content-grid equal">
            <article class="surface decision-card">
              <div class="surface-header"><div><span class="step-badge">Stap 1</span><h3>Intelligence review</h3></div><span id="review-permission" class="permission-badge">Onbekend</span></div>
              <p>Leg vast dat een intelligence-item inhoudelijk is beoordeeld. Dit verleent geen publicatierecht.</p>
              <label for="decision-item">Intelligence item ID</label>
              <input id="decision-item" autocomplete="off" placeholder="UUID of canonical item ID">
              <button id="review-action" class="button secondary full" type="button">Markeer als reviewed</button>
            </article>
            <article class="surface decision-card critical">
              <div class="surface-header"><div><span class="step-badge danger">Stap 2</span><h3>External share approval</h3></div><span id="share-permission" class="permission-badge">Onbekend</span></div>
              <p>Geef expliciete menselijke toestemming voor extern delen. De reviewer mag niet dezelfde principal zijn.</p>
              <div class="sod-notice"><strong>Separation of duties</strong><span>Self-approval wordt server-side geblokkeerd.</span></div>
              <button id="share-action" class="button danger full" type="button">Approve external sharing</button>
            </article>
          </div>
          <article class="surface response-surface"><div class="surface-header"><h3>Besluitresultaat</h3><button id="clear-decision-result" class="text-button" type="button">Wissen</button></div><pre id="decision-result" class="console-output" aria-live="polite">Nog geen beslissing uitgevoerd.</pre></article>
        </section>

        <section id="audit" class="workspace-section" aria-labelledby="audit-title">
          <div class="page-heading"><div><p class="eyebrow">Auditability</p><h2 id="audit-title">Audit evidence</h2><p>Read-only weergave van recente audit-events, inclusief principal, decision en event hash.</p></div><button id="load-audit" class="button secondary" type="button">Audit evidence laden</button></div>
          <article class="surface table-surface">
            <div id="audit-status" class="inline-status" role="status" aria-live="polite">Nog niet geladen.</div>
            <div class="table-wrap">
              <table>
                <thead><tr><th scope="col">Actie</th><th scope="col">Principal</th><th scope="col">Decision</th><th scope="col">Resource</th><th scope="col">Hash</th></tr></thead>
                <tbody id="audit-events"><tr><td colspan="5" class="empty-cell">Laad audit evidence om recente events te bekijken.</td></tr></tbody>
              </table>
            </div>
          </article>
        </section>

        <section id="security" class="workspace-section" aria-labelledby="security-title">
          <div class="page-heading"><div><p class="eyebrow">Security operations</p><h2 id="security-title">CISO controls</h2><p>Beveiligingsacties met verhoogde impact worden apart aangeboden en server-side geautoriseerd.</p></div></div>
          <article class="surface security-card">
            <div class="security-heading"><div class="security-symbol">!</div><div><h3>Token revocation</h3><p>Maak een bearer token voortijdig ongeldig. Alleen toegestaan voor een menselijke principal met <code>revoke:tokens</code>.</p></div></div>
            <form id="revocation-form" class="form-grid three">
              <label>Token identifier (JTI)<input id="token-jti" autocomplete="off" placeholder="Token JTI"></label>
              <label>Expiry (ISO 8601)<input id="token-expiry" autocomplete="off" placeholder="2026-08-10T15:00:00Z"></label>
              <label>Reden<input id="revocation-reason" autocomplete="off" placeholder="Waarom wordt dit token ingetrokken?"></label>
              <button class="button danger" type="submit">Token intrekken</button>
            </form>
            <div id="revocation-status" class="inline-status" role="status" aria-live="polite">Wacht op geautoriseerde sessie.</div>
          </article>
        </section>
      </main>
    </div>
  </div>

  <dialog id="identity-dialog" class="modal">
    <form method="dialog" class="modal-frame" id="identity-form">
      <div class="modal-header"><div><p class="eyebrow">Lokale testcontext</p><h2>Testidentiteit configureren</h2></div><button class="icon-button" value="cancel" aria-label="Sluiten">×</button></div>
      <p class="modal-help">Alleen bedoeld voor lokale/dev/staging-validatie. De waarden blijven uitsluitend in deze browsertab via <code>sessionStorage</code>. Productie gebruikt de geconfigureerde bearer-token/identity-provider route.</p>
      <div class="form-grid">
        <label>Subject<input id="subject" autocomplete="off" value="external-tester"></label>
        <label>Rollen<input id="roles" autocomplete="off" value="analyst" aria-describedby="roles-help"><small id="roles-help">Bijv. analyst, reviewer, share_approver, auditor, ciso.</small></label>
        <label class="span-2">DTMO API key<input id="api-key" type="password" autocomplete="off"></label>
      </div>
      <div id="session-state" class="inline-status" role="status" aria-live="polite">Nog geen sessie gecontroleerd.</div>
      <div class="modal-actions"><button id="clear-identity" class="button ghost" type="button">Lokale identiteit wissen</button><div><button class="button ghost" value="cancel">Annuleren</button><button id="save-identity" class="button primary" value="default">Identiteit toepassen</button></div></div>
    </form>
  </dialog>

  <script src="/ui/console.js" defer></script>
</body>
</html>
"""

_CSS = """
:root{--bg:#07111f;--sidebar:#091525;--surface:#0d1b2d;--surface-2:#11233a;--surface-3:#152b47;--line:#213a58;--line-soft:#182d46;--text:#eef5ff;--muted:#91a5bd;--muted-2:#6f849d;--accent:#4eb3ff;--accent-strong:#168ce0;--good:#43d69b;--warn:#f5c85b;--bad:#ff6b7a;--focus:#ffe68a;--shadow:0 18px 55px rgba(0,0,0,.22);font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;color-scheme:dark}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--bg);color:var(--text);min-height:100vh}button,input{font:inherit}a{color:inherit}a:focus-visible,button:focus-visible,input:focus-visible{outline:3px solid var(--focus);outline-offset:3px}.skip-link{position:fixed;left:-9999px;top:1rem;background:white;color:#07111f;padding:.8rem 1rem;border-radius:8px;z-index:100}.skip-link:focus{left:1rem}.app-shell{min-height:100vh;display:grid;grid-template-columns:250px minmax(0,1fr)}.sidebar{position:sticky;top:0;height:100vh;background:linear-gradient(180deg,#091525,#07111f);border-right:1px solid var(--line-soft);padding:1.4rem 1rem;display:flex;flex-direction:column;gap:1.5rem}.brand{display:flex;align-items:center;gap:.8rem;padding:.25rem .4rem}.brand-mark{width:42px;height:42px;border-radius:12px;display:grid;place-items:center;background:linear-gradient(135deg,#2aa7ff,#6b7cff);font-weight:900;font-size:1.2rem;box-shadow:0 8px 24px rgba(42,167,255,.25)}.brand strong{display:block;font-size:1.03rem;letter-spacing:.02em}.brand span{display:block;color:var(--muted);font-size:.75rem;margin-top:.1rem}.nav-list{display:grid;gap:.3rem}.nav-item{display:flex;align-items:center;gap:.8rem;padding:.72rem .8rem;text-decoration:none;border-radius:10px;color:var(--muted);font-weight:700;font-size:.92rem;border:1px solid transparent}.nav-item:hover{background:rgba(255,255,255,.035);color:var(--text)}.nav-item.active{background:linear-gradient(90deg,rgba(78,179,255,.16),rgba(78,179,255,.05));color:#dff2ff;border-color:rgba(78,179,255,.2)}.nav-icon{width:1.25rem;text-align:center;color:var(--accent)}.sidebar-footer{margin-top:auto;display:grid;gap:.55rem;padding:.9rem .55rem;border-top:1px solid var(--line-soft)}.sidebar-footer a{text-decoration:none;color:var(--muted);font-size:.78rem}.sidebar-footer a:hover{color:var(--text)}.sidebar-label{text-transform:uppercase;letter-spacing:.1em;color:var(--muted-2);font-size:.62rem;font-weight:800;margin-bottom:.2rem}.app-main{min-width:0}.app-header{height:86px;position:sticky;top:0;z-index:20;background:rgba(7,17,31,.9);backdrop-filter:blur(18px);border-bottom:1px solid var(--line-soft);padding:0 clamp(1rem,3vw,2.4rem);display:flex;align-items:center;justify-content:space-between;gap:1rem}.app-header h1{margin:.15rem 0 0;font-size:1.35rem}.eyebrow{margin:0;color:var(--accent);font-size:.66rem;letter-spacing:.12em;text-transform:uppercase;font-weight:900}.header-actions{display:flex;align-items:center;gap:.75rem}.status-pill{display:inline-flex;align-items:center;gap:.45rem;border:1px solid var(--line);border-radius:999px;padding:.42rem .7rem;font-size:.75rem;font-weight:800;color:var(--muted);background:rgba(13,27,45,.75)}.status-pill.success{color:#abf1d1;border-color:rgba(67,214,155,.35)}.status-pill.error{color:#ffc1c7;border-color:rgba(255,107,122,.38)}.status-pill.loading{color:#ffe39b}.status-dot{width:7px;height:7px;border-radius:50%;background:currentColor}.profile-button{display:flex;align-items:center;gap:.65rem;background:transparent;color:var(--text);border:1px solid transparent;border-radius:12px;padding:.35rem .45rem;cursor:pointer;text-align:left}.profile-button:hover{background:var(--surface)}.profile-button strong,.profile-button small{display:block}.profile-button small{color:var(--muted);font-size:.7rem;margin-top:.1rem}.avatar{width:36px;height:36px;border-radius:10px;background:var(--surface-3);border:1px solid var(--line);display:grid;place-items:center;font-size:.72rem;font-weight:900;color:#cfeaff}.workspace{width:min(1500px,calc(100% - 3rem));margin:0 auto;padding:2rem 0 4rem}.workspace-section{scroll-margin-top:105px;margin-bottom:3.2rem}.page-heading{display:flex;justify-content:space-between;align-items:flex-end;gap:1rem;margin-bottom:1.25rem}.page-heading h2{font-size:clamp(1.55rem,2.2vw,2.05rem);margin:.2rem 0 .35rem}.page-heading p:not(.eyebrow){margin:0;color:var(--muted);max-width:75ch;font-size:.93rem}.kpi-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:.9rem;margin-bottom:.9rem}.kpi-card,.surface{border:1px solid var(--line-soft);background:linear-gradient(180deg,rgba(17,35,58,.96),rgba(13,27,45,.96));border-radius:14px;box-shadow:var(--shadow)}.kpi-card{padding:1rem 1.05rem;display:grid;gap:.35rem}.kpi-card strong{font-size:1.25rem}.kpi-card small{color:var(--muted);font-size:.75rem}.kpi-top{display:flex;align-items:center;gap:.55rem}.kpi-icon{width:24px;height:24px;border-radius:7px;background:rgba(78,179,255,.12);display:grid;place-items:center;color:var(--accent);font-size:.66rem}.kpi-icon.good{color:var(--good);background:rgba(67,214,155,.12)}.kpi-icon.warn{color:var(--warn);background:rgba(245,200,91,.12)}.kpi-label{font-size:.72rem;color:var(--muted);font-weight:800;text-transform:uppercase;letter-spacing:.05em}.content-grid{display:grid;gap:.9rem}.content-grid.two-thirds{grid-template-columns:minmax(0,1.55fr) minmax(280px,.85fr)}.content-grid.equal{grid-template-columns:repeat(2,minmax(0,1fr))}.surface{padding:1.1rem}.surface-header{display:flex;justify-content:space-between;align-items:center;gap:1rem;margin-bottom:1rem}.surface-header h3{margin:.15rem 0 0;font-size:1rem}.connector-list{display:grid;gap:.5rem}.connector-row{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:1rem;align-items:center;padding:.8rem .85rem;background:rgba(7,17,31,.48);border:1px solid var(--line-soft);border-radius:10px}.connector-row strong{display:block;font-size:.88rem}.connector-row small{display:block;color:var(--muted);margin-top:.2rem;font-size:.74rem}.connector-state{font-size:.72rem;font-weight:900;padding:.28rem .52rem;border-radius:999px;border:1px solid var(--line);color:var(--muted)}.connector-state.enabled{color:#9cecc9;border-color:rgba(67,214,155,.3)}.governance-summary{display:grid;align-content:start}.governance-item{display:grid;grid-template-columns:32px 1fr;gap:.7rem;padding:.7rem 0;border-top:1px solid var(--line-soft)}.governance-item:first-of-type{border-top:0}.governance-icon{width:28px;height:28px;border-radius:50%;display:grid;place-items:center;background:rgba(78,179,255,.12);color:var(--accent);font-size:.72rem;font-weight:900}.governance-item strong{font-size:.86rem}.governance-item p{margin:.15rem 0 0;color:var(--muted);font-size:.75rem;line-height:1.45}.hero-search{display:grid;grid-template-columns:auto minmax(0,1fr) auto;align-items:center;gap:.6rem;background:#071321;border:1px solid #2b486b;border-radius:12px;padding:.45rem}.hero-search:focus-within{border-color:var(--accent);box-shadow:0 0 0 3px rgba(78,179,255,.1)}.search-icon{padding-left:.5rem;color:var(--muted);font-size:1.2rem}.hero-search input{border:0;background:transparent;padding:.7rem;color:var(--text);outline:0;min-width:0}.inline-status{margin-top:.8rem;color:var(--muted);font-size:.78rem;min-height:1.2rem}.inline-status[data-state=success]{color:#a9efd0}.inline-status[data-state=error]{color:#ffb9c0}.inline-status[data-state=loading]{color:#ffe29a}.intel-results{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.7rem;margin-top:.8rem}.intel-card{padding:.9rem;background:#081728;border:1px solid var(--line-soft);border-radius:11px}.intel-card h3{margin:0 0 .4rem;font-size:.92rem}.intel-card p{margin:0 0 .65rem;color:#b4c4d7;font-size:.8rem;line-height:1.5}.intel-meta{display:flex;gap:.45rem;flex-wrap:wrap}.meta-tag{font-size:.68rem;color:var(--muted);border:1px solid var(--line);border-radius:999px;padding:.2rem .42rem}.decision-card{display:flex;flex-direction:column;gap:.8rem}.decision-card p{color:var(--muted);font-size:.82rem;line-height:1.5;margin:0}.decision-card.critical{border-color:rgba(255,107,122,.22)}.step-badge{display:inline-block;color:var(--accent);background:rgba(78,179,255,.1);padding:.22rem .45rem;border-radius:6px;font-size:.65rem;font-weight:900;margin-bottom:.35rem}.step-badge.danger{color:#ffbbc2;background:rgba(255,107,122,.1)}.permission-badge{font-size:.68rem;color:var(--muted);font-weight:800}.sod-notice{display:grid;gap:.15rem;padding:.7rem;border:1px solid rgba(255,107,122,.24);background:rgba(255,107,122,.06);border-radius:9px}.sod-notice strong{font-size:.76rem;color:#ffc1c7}.sod-notice span{font-size:.72rem;color:var(--muted)}.response-surface{margin-top:.9rem}.console-output{margin:0;min-height:6.5rem;max-height:18rem;overflow:auto;white-space:pre-wrap;overflow-wrap:anywhere;background:#050e19;border:1px solid var(--line-soft);border-radius:9px;padding:.85rem;color:#cce5ff;font-size:.74rem;line-height:1.55}.table-surface{padding:0;overflow:hidden}.table-surface .inline-status{padding:0 1rem;margin:1rem 0}.table-wrap{overflow:auto}table{width:100%;border-collapse:collapse;font-size:.78rem}th{text-align:left;color:var(--muted);font-size:.68rem;text-transform:uppercase;letter-spacing:.06em;background:#0a1727}th,td{padding:.72rem .9rem;border-top:1px solid var(--line-soft);vertical-align:top}td code{font-size:.68rem;color:#8fa9c6;overflow-wrap:anywhere}.empty-cell{text-align:center;color:var(--muted);padding:2rem}.security-card{border-color:rgba(255,107,122,.18)}.security-heading{display:grid;grid-template-columns:42px 1fr;gap:.8rem;margin-bottom:1rem}.security-symbol{width:38px;height:38px;border-radius:10px;display:grid;place-items:center;background:rgba(255,107,122,.1);color:var(--bad);font-weight:900}.security-heading h3{margin:0 0 .25rem}.security-heading p{margin:0;color:var(--muted);font-size:.8rem}.form-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.8rem}.form-grid.three{grid-template-columns:repeat(3,minmax(0,1fr))}.span-2{grid-column:span 2}label{display:grid;gap:.35rem;font-size:.76rem;color:#c9d9eb;font-weight:800}label small{color:var(--muted);font-weight:500}input{width:100%;border:1px solid #2a496d;border-radius:9px;background:#071321;color:var(--text);padding:.7rem .75rem}.button{border:1px solid transparent;border-radius:9px;padding:.68rem .9rem;font-weight:850;cursor:pointer}.button.primary{background:linear-gradient(180deg,#57baff,#279be9);color:#04101c}.button.secondary{background:#132944;border-color:#2b486b;color:var(--text)}.button.danger{background:linear-gradient(180deg,#c34c5b,#993745);color:white}.button.ghost{background:transparent;border-color:var(--line);color:var(--muted)}.button.full{width:100%;margin-top:auto}.button:disabled{opacity:.45;cursor:not-allowed}.icon-button{width:34px;height:34px;border:1px solid var(--line);border-radius:9px;background:#0b1c30;color:var(--text);cursor:pointer}.text-button{border:0;background:transparent;color:var(--accent);cursor:pointer;font-weight:800;font-size:.72rem}.skeleton-row{height:58px;border-radius:9px;background:linear-gradient(90deg,#0a1727 25%,#11243b 50%,#0a1727 75%);background-size:200% 100%}.modal{width:min(620px,calc(100% - 2rem));border:1px solid var(--line);border-radius:16px;padding:0;background:var(--surface);color:var(--text);box-shadow:0 30px 100px rgba(0,0,0,.55)}.modal::backdrop{background:rgba(1,7,14,.72);backdrop-filter:blur(4px)}.modal-frame{padding:1.2rem}.modal-header{display:flex;justify-content:space-between;gap:1rem;align-items:start}.modal-header h2{margin:.2rem 0 0;font-size:1.25rem}.modal-help{color:var(--muted);font-size:.78rem;line-height:1.5}.modal-actions{display:flex;justify-content:space-between;gap:.8rem;margin-top:1rem;align-items:center}.modal-actions>div{display:flex;gap:.6rem}.sr-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}@media(max-width:1100px){.app-shell{grid-template-columns:84px minmax(0,1fr)}.brand div:last-child,.nav-item span:last-child,.sidebar-footer{display:none}.brand{justify-content:center}.nav-item{justify-content:center}.kpi-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.content-grid.two-thirds{grid-template-columns:1fr}}@media(max-width:760px){.app-shell{display:block}.sidebar{position:static;height:auto;border-right:0;border-bottom:1px solid var(--line-soft);padding:.7rem}.brand{display:none}.nav-list{display:flex;overflow:auto}.nav-item{white-space:nowrap;padding:.55rem .7rem}.nav-item span:last-child{display:inline}.app-header{position:static;height:auto;padding:1rem;align-items:flex-start}.app-header .eyebrow{display:none}.header-actions{width:100%;justify-content:space-between}.workspace{width:min(100% - 1rem,1500px);padding-top:1rem}.kpi-grid,.content-grid.equal,.intel-results,.form-grid,.form-grid.three{grid-template-columns:1fr}.span-2{grid-column:auto}.page-heading{align-items:flex-start;flex-direction:column}.profile-button span:nth-child(2){display:none}.hero-search{grid-template-columns:auto 1fr}.hero-search .button{grid-column:1/-1}.modal-actions{align-items:stretch;flex-direction:column}.modal-actions>div{display:grid;grid-template-columns:1fr 1fr}.modal-actions>.button{width:100%}}@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}.skeleton-row{background:#0a1727}}
"""

_SCRIPT = r"""(() => {
  const $ = (id) => document.getElementById(id);
  const storageKey = 'dtmo-console-identity-v2';
  let session = null;

  function setStatus(element, message, state = '') {
    element.textContent = message;
    if (state) element.dataset.state = state; else delete element.dataset.state;
  }

  function identity() {
    try { return JSON.parse(sessionStorage.getItem(storageKey) || '{}'); } catch (_) { return {}; }
  }

  function authHeaders(extra = {}) {
    const current = identity();
    const headers = {...extra};
    if (current.subject) headers['X-DTMO-Subject'] = current.subject;
    if (current.roles) headers['X-DTMO-Roles'] = current.roles;
    if (current.apiKey) headers['X-DTMO-API-Key'] = current.apiKey;
    return headers;
  }

  async function jsonFetch(url, options = {}) {
    const response = await fetch(url, {...options, credentials: 'same-origin', headers: authHeaders(options.headers || {})});
    let body;
    try { body = await response.json(); } catch (_) { body = {detail: 'Ongeldige JSON-response'}; }
    if (!response.ok) throw new Error(body.detail || `HTTP ${response.status}`);
    return body;
  }

  function hasPermission(permission) {
    return Boolean(session && session.permissions && session.permissions.includes(permission));
  }

  function syncPermissions() {
    const read = hasPermission('read:intelligence');
    const review = hasPermission('review:intelligence');
    const share = hasPermission('approve:share');
    const audit = hasPermission('read:audit');
    const revoke = hasPermission('revoke:tokens') && !session?.service_account;
    $('search-form').querySelector('button').disabled = !read;
    $('search-permission').textContent = read ? 'Read intelligence' : 'Geen read-permissie';
    $('search-permission').className = `status-pill ${read ? 'success' : 'neutral'}`;
    $('review-action').disabled = !review;
    $('share-action').disabled = !share;
    $('load-audit').disabled = !audit;
    $('revocation-form').querySelector('button').disabled = !revoke;
    $('review-permission').textContent = review ? 'Toegestaan' : 'Niet toegestaan';
    $('share-permission').textContent = share ? 'Toegestaan' : 'Niet toegestaan';
  }

  async function loadHealth() {
    try {
      const body = await jsonFetch('/health');
      $('health-chip').className = 'status-pill success';
      $('health-chip').innerHTML = '<span class="status-dot"></span>API healthy';
      $('metric-api').textContent = 'Healthy';
      $('metric-version').textContent = `DTMO ${body.version}`;
      $('metric-environment').textContent = body.environment || 'unknown';
      $('metric-publication').textContent = body.publication_gate === 'human-approval-required' ? 'Human approval' : body.publication_gate;
    } catch (error) {
      $('health-chip').className = 'status-pill error';
      $('health-chip').innerHTML = '<span class="status-dot"></span>API unavailable';
      $('metric-api').textContent = 'Unavailable';
      $('metric-version').textContent = error.message;
    }
  }

  async function loadSession() {
    try {
      session = await jsonFetch('/api/v1/ui/session');
      $('identity-name').textContent = session.subject;
      $('identity-role').textContent = session.roles.join(', ') || 'Geen rollen';
      const initials = session.subject.split(/[-_. ]+/).slice(0, 2).map((part) => part[0]?.toUpperCase() || '').join('') || 'DT';
      document.querySelector('.avatar').textContent = initials;
      setStatus($('session-state'), `${session.subject} — ${session.roles.join(', ') || 'geen rollen'}`, 'success');
      syncPermissions();
    } catch (error) {
      session = null;
      $('identity-role').textContent = 'Niet verbonden';
      setStatus($('session-state'), `Sessiefout: ${error.message}`, 'error');
      syncPermissions();
    }
  }

  async function loadConnectors() {
    const target = $('connector-list');
    target.innerHTML = '<div class="skeleton-row"></div><div class="skeleton-row"></div>';
    try {
      const items = await jsonFetch('/connectors');
      $('metric-connectors').textContent = `${items.filter((item) => item.enabled).length}/${items.length} actief`;
      target.replaceChildren();
      for (const item of items) {
        const row = document.createElement('div');
        row.className = 'connector-row';
        const info = document.createElement('div');
        const name = document.createElement('strong');
        name.textContent = item.id;
        const meta = document.createElement('small');
        meta.textContent = `${item.reliability || 'unknown'} · poll ${item.schedule_seconds || '—'}s`;
        info.append(name, meta);
        const state = document.createElement('span');
        state.className = `connector-state ${item.enabled ? 'enabled' : ''}`;
        state.textContent = item.enabled ? 'Enabled' : 'Disabled';
        row.append(info, state);
        target.appendChild(row);
      }
      if (!items.length) target.textContent = 'Geen connectors geregistreerd.';
    } catch (error) {
      target.innerHTML = `<div class="inline-status" data-state="error">Connectorstatus niet beschikbaar: ${error.message}</div>`;
      $('metric-connectors').textContent = 'Unavailable';
    }
  }

  function renderResults(items) {
    const target = $('search-results');
    target.replaceChildren();
    for (const item of items) {
      const card = document.createElement('article');
      card.className = 'intel-card';
      const title = document.createElement('h3');
      title.textContent = String(item.title || 'Untitled intelligence');
      const summary = document.createElement('p');
      summary.textContent = String(item.summary || 'Geen samenvatting beschikbaar.');
      const meta = document.createElement('div');
      meta.className = 'intel-meta';
      for (const value of [item.id, item.confidence, item.source]) {
        if (!value) continue;
        const tag = document.createElement('span');
        tag.className = 'meta-tag';
        tag.textContent = String(value);
        meta.appendChild(tag);
      }
      card.append(title, summary, meta);
      target.appendChild(card);
    }
  }

  async function searchIntelligence() {
    const value = $('search-query').value.trim();
    if (value.length < 2) return;
    setStatus($('search-status'), 'Intelligence doorzoeken…', 'loading');
    $('search-results').replaceChildren();
    try {
      const body = await jsonFetch(`/api/v1/intelligence/search?q=${encodeURIComponent(value)}`);
      renderResults(body.results || []);
      setStatus($('search-status'), body.count ? `${body.count} resultaat${body.count === 1 ? '' : 'en'} gevonden.` : 'Geen intelligence gevonden.', body.count ? 'success' : '');
    } catch (error) {
      setStatus($('search-status'), `Zoeken mislukt: ${error.message}`, 'error');
    }
  }

  async function decision(action) {
    const id = $('decision-item').value.trim();
    if (!id) {
      $('decision-result').textContent = 'Vul eerst een intelligence item ID in.';
      $('decision-item').focus();
      return;
    }
    $('decision-result').textContent = 'Beslissing wordt verwerkt…';
    try {
      const body = await jsonFetch(`/api/v1/intelligence/${encodeURIComponent(id)}/${action}`, {method: 'POST', headers: {'X-Request-ID': crypto.randomUUID()}});
      $('decision-result').textContent = JSON.stringify(body, null, 2);
    } catch (error) {
      $('decision-result').textContent = `Beslissing geweigerd/mislukt: ${error.message}`;
    }
  }

  async function loadAudit() {
    const target = $('audit-events');
    target.innerHTML = '<tr><td colspan="5" class="empty-cell">Audit evidence laden…</td></tr>';
    setStatus($('audit-status'), 'Audit evidence laden…', 'loading');
    try {
      const body = await jsonFetch('/api/v1/audit/events?limit=50');
      target.replaceChildren();
      for (const item of body.events || []) {
        const row = document.createElement('tr');
        for (const value of [item.action, item.principal, item.decision, item.resource]) {
          const cell = document.createElement('td');
          cell.textContent = String(value || '—');
          row.appendChild(cell);
        }
        const hashCell = document.createElement('td');
        const code = document.createElement('code');
        code.textContent = String(item.event_hash || '—');
        hashCell.appendChild(code);
        row.appendChild(hashCell);
        target.appendChild(row);
      }
      if (!body.count) target.innerHTML = '<tr><td colspan="5" class="empty-cell">Geen audit events beschikbaar.</td></tr>';
      setStatus($('audit-status'), `${body.count || 0} audit event${body.count === 1 ? '' : 's'} geladen (read-only).`, 'success');
    } catch (error) {
      target.innerHTML = '<tr><td colspan="5" class="empty-cell">Audit evidence niet beschikbaar.</td></tr>';
      setStatus($('audit-status'), `Audit read mislukt: ${error.message}`, 'error');
    }
  }

  async function revokeToken(event) {
    event.preventDefault();
    setStatus($('revocation-status'), 'Token intrekken…', 'loading');
    try {
      const body = await jsonFetch('/api/v1/security/tokens/revoke', {method: 'POST', headers: {'Content-Type': 'application/json', 'X-Request-ID': crypto.randomUUID()}, body: JSON.stringify({jti: $('token-jti').value.trim(), expires_at: $('token-expiry').value.trim(), reason: $('revocation-reason').value.trim()})});
      setStatus($('revocation-status'), `Token ingetrokken. Audit event: ${body.audit_event_id}`, 'success');
    } catch (error) {
      setStatus($('revocation-status'), `Revocation mislukt: ${error.message}`, 'error');
    }
  }

  function loadIdentityForm() {
    const current = identity();
    $('subject').value = current.subject || 'external-tester';
    $('roles').value = current.roles || 'analyst';
    $('api-key').value = current.apiKey || '';
  }

  async function saveIdentity(event) {
    event.preventDefault();
    sessionStorage.setItem(storageKey, JSON.stringify({subject: $('subject').value.trim(), roles: $('roles').value.trim(), apiKey: $('api-key').value}));
    await loadSession();
    if (session) $('identity-dialog').close();
  }

  function observeNavigation() {
    const links = [...document.querySelectorAll('[data-section-link]')];
    const sections = links.map((link) => document.getElementById(link.dataset.sectionLink)).filter(Boolean);
    const observer = new IntersectionObserver((entries) => {
      const visible = entries.filter((entry) => entry.isIntersecting).sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
      if (!visible) return;
      for (const link of links) link.classList.toggle('active', link.dataset.sectionLink === visible.target.id);
    }, {rootMargin: '-20% 0px -65% 0px', threshold: [0, .25, .5]});
    for (const section of sections) observer.observe(section);
  }

  $('open-identity').addEventListener('click', () => { loadIdentityForm(); $('identity-dialog').showModal(); });
  $('identity-form').addEventListener('submit', saveIdentity);
  $('clear-identity').addEventListener('click', async () => { sessionStorage.removeItem(storageKey); loadIdentityForm(); await loadSession(); });
  $('refresh-overview').addEventListener('click', () => void Promise.all([loadHealth(), loadConnectors(), loadSession()]));
  $('refresh-connectors').addEventListener('click', () => void loadConnectors());
  $('search-form').addEventListener('submit', (event) => { event.preventDefault(); void searchIntelligence(); });
  $('review-action').addEventListener('click', () => void decision('review'));
  $('share-action').addEventListener('click', () => void decision('share-approval'));
  $('clear-decision-result').addEventListener('click', () => { $('decision-result').textContent = 'Nog geen beslissing uitgevoerd.'; });
  $('load-audit').addEventListener('click', () => void loadAudit());
  $('revocation-form').addEventListener('submit', revokeToken);

  observeNavigation();
  void Promise.all([loadHealth(), loadConnectors(), loadSession()]);
})();
"""


def _headers() -> dict[str, str]:
    return {
        "Cache-Control": "no-store",
        "Content-Security-Policy": (
            "default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self'; "
            "img-src 'self' data:; font-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'"
        ),
    }


@router.get("/", response_class=HTMLResponse, include_in_schema=False)
@router.get("/ui/console", response_class=HTMLResponse, include_in_schema=False)
def console_page() -> HTMLResponse:
    return HTMLResponse(_PAGE, headers=_headers())


@router.get("/ui/design-system.css", include_in_schema=False)
@router.get("/ui/console.css", include_in_schema=False)
def console_css() -> Response:
    return Response(_CSS, media_type="text/css", headers={"Cache-Control": "no-store"})


@router.get("/ui/console.js", include_in_schema=False)
def console_script() -> Response:
    return Response(_SCRIPT, media_type="application/javascript", headers={"Cache-Control": "no-store"})

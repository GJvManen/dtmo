from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse, Response

from dtmo.auth.dependencies import resolve_principal
from dtmo.auth.policy import Permission, Principal

router = APIRouter()

_PAGE = """<!doctype html>
<html lang="nl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>DTMO — Share approval</title>
  <link rel="stylesheet" href="/ui/design-system.css">
  <link rel="stylesheet" href="/ui/rc9-compat.css">
</head>
<body>
  <a class="skip-link" href="#main">Ga naar hoofdinhoud</a>
  <header class="app-header">
    <div><p class="eyebrow">Governance workspace</p><h1>Share approval</h1></div>
    <div class="header-actions"><a class="button ghost" href="/">Terug naar console</a><span id="principal" data-testid="principal" class="status-pill neutral" role="status" aria-live="polite" aria-atomic="true">Principal bepalen…</span></div>
  </header>
  <main id="main" class="workspace">
    <section class="page-heading"><div><p class="eyebrow">Separation of duties</p><h2>Governed intelligence decision</h2><p>Review en externe share approval zijn twee afzonderlijke menselijke beslissingen. Dezelfde principal mag niet beide stappen voor hetzelfde item uitvoeren.</p></div></section>
    <div class="content-grid equal">
      <article class="surface decision-card">
        <div class="surface-header"><div><span class="step-badge">Stap 1</span><h3>Review vastleggen</h3></div></div>
        <p>Markeer een intelligence-item als inhoudelijk beoordeeld. Dit geeft geen toestemming voor extern delen.</p>
        <label for="item-id">Intelligence item ID<input id="item-id" data-testid="item-id" autocomplete="off" required placeholder="UUID of canonical item ID"></label>
        <button id="review" data-testid="review-button" class="button secondary full" type="button" hidden>Markeer als reviewed</button>
      </article>
      <article class="surface decision-card critical">
        <div class="surface-header"><div><span class="step-badge danger">Stap 2</span><h3>Extern delen goedkeuren</h3></div></div>
        <p>Geef expliciete menselijke toestemming voor externe distributie nadat een onafhankelijke review is vastgelegd.</p>
        <div class="sod-notice"><strong>Menselijke goedkeuring verplicht</strong><span>DTMO blokkeert self-approval server-side en schrijft de beslissing naar de audit trail.</span></div>
        <button id="share" data-testid="share-button" class="button danger full" type="button" hidden>Approve external sharing</button>
      </article>
    </div>
    <article class="surface response-surface"><div class="surface-header"><h3>Besluitresultaat</h3></div><pre id="result" data-testid="result" class="console-output" aria-live="polite">Nog geen beslissing uitgevoerd.</pre></article>
  </main>
  <script src="/ui/share-approval.js" defer></script>
</body>
</html>
"""

_SCRIPT = r"""(() => {
  const principal = document.getElementById('principal');
  const itemId = document.getElementById('item-id');
  const review = document.getElementById('review');
  const share = document.getElementById('share');
  const result = document.getElementById('result');

  async function session() {
    const response = await fetch('/api/v1/ui/session', {credentials: 'same-origin'});
    const body = await response.json();
    if (!response.ok) throw new Error(body.detail || `session failed: ${response.status}`);
    principal.textContent = `${body.subject} · ${body.roles.join(', ') || 'geen rollen'}`;
    principal.className = 'status-pill success';
    review.hidden = !body.permissions.includes('review:intelligence');
    share.hidden = !body.permissions.includes('approve:share');
  }

  async function decision(action) {
    const id = itemId.value.trim();
    if (!id) {
      result.textContent = 'Vul eerst een intelligence item ID in.';
      itemId.focus();
      return;
    }
    result.textContent = 'Beslissing wordt verwerkt…';
    const response = await fetch(`/api/v1/intelligence/${encodeURIComponent(id)}/${action}`, {
      method: 'POST', credentials: 'same-origin', headers: {'X-Request-ID': crypto.randomUUID()},
    });
    let body;
    try { body = await response.json(); } catch (_) { body = {detail: 'invalid response'}; }
    result.textContent = JSON.stringify({status: response.status, ...body}, null, 2);
  }

  review.addEventListener('click', () => decision('review'));
  share.addEventListener('click', () => decision('share-approval'));
  session().catch((error) => {
    principal.textContent = `Sessiefout: ${error.message}`;
    principal.className = 'status-pill error';
  });
})();
"""

_ANALYST_PAGE = """<!doctype html>
<html lang="nl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>DTMO — Analyst workspace</title>
  <link rel="stylesheet" href="/ui/design-system.css">
  <link rel="stylesheet" href="/ui/rc9-compat.css">
</head>
<body>
  <a class="skip-link" href="#main">Ga naar hoofdinhoud</a>
  <header class="app-header">
    <div><p class="eyebrow">Analyst workspace</p><h1>Intelligence explorer</h1></div>
    <div class="header-actions"><a class="button ghost" href="/">Terug naar console</a><span id="analyst-principal" data-testid="analyst-principal" class="status-pill neutral" role="status" aria-live="polite" aria-atomic="true">Principal bepalen…</span></div>
  </header>
  <main id="main" class="workspace">
    <section class="page-heading"><div><p class="eyebrow">Threat intelligence</p><h2>Zoeken en triageren</h2><p>Doorzoek beschikbare intelligence en beoordeel resultaten op relevantie, provenance en confidence.</p></div></section>
    <section id="search-panel" data-testid="search-panel" class="surface search-surface" hidden>
      <form id="search-form" class="hero-search">
        <label class="sr-only" for="query">Zoek intelligence</label><span class="search-icon" aria-hidden="true">⌕</span>
        <input id="query" data-testid="search-query" minlength="2" required autocomplete="off" placeholder="Zoek op dreiging, CVE, actor of leverancier…">
        <button type="submit" data-testid="search-submit" class="button primary">Zoeken</button>
      </form>
      <div id="status" data-testid="search-status" class="inline-status" role="status" aria-live="polite">Klaar om te zoeken.</div>
      <div id="results" data-testid="search-results" class="intel-results"></div>
    </section>
  </main>
  <script src="/ui/analyst-search.js" defer></script>
</body>
</html>
"""

_ANALYST_SCRIPT = r"""(() => {
  const principal = document.getElementById('analyst-principal');
  const panel = document.getElementById('search-panel');
  const form = document.getElementById('search-form');
  const query = document.getElementById('query');
  const status = document.getElementById('status');
  const results = document.getElementById('results');

  function setState(message, state) { status.textContent = message; status.dataset.state = state; }
  function render(items) {
    results.replaceChildren();
    for (const item of items) {
      const row = document.createElement('article'); row.className = 'intel-card';
      const title = document.createElement('h3'); title.textContent = String(item.title || 'Untitled intelligence');
      const summary = document.createElement('p'); summary.textContent = String(item.summary || 'Geen samenvatting beschikbaar.');
      const meta = document.createElement('div'); meta.className = 'intel-meta';
      for (const value of [item.id, item.confidence, item.source]) {
        if (!value) continue; const tag = document.createElement('span'); tag.className = 'meta-tag'; tag.textContent = String(value); meta.appendChild(tag);
      }
      row.append(title, summary, meta); results.appendChild(row);
    }
  }
  async function session() {
    const response = await fetch('/api/v1/ui/session', {credentials: 'same-origin'}); const body = await response.json();
    if (!response.ok) throw new Error(body.detail || `session failed: ${response.status}`);
    principal.textContent = `${body.subject} · ${body.roles.join(', ') || 'geen rollen'}`; principal.className = 'status-pill success';
    const allowed = body.permissions.includes('read:intelligence'); panel.hidden = !allowed;
    if (!allowed) setState('Intelligence search is niet toegestaan voor deze principal.', 'forbidden');
  }
  async function search() {
    const value = query.value.trim(); if (value.length < 2) return; results.replaceChildren(); setState('Intelligence doorzoeken…', 'loading');
    try {
      const response = await fetch(`/api/v1/intelligence/search?q=${encodeURIComponent(value)}`, {credentials: 'same-origin'});
      let body; try { body = await response.json(); } catch (_) { body = {detail: 'invalid response'}; }
      if (!response.ok) throw new Error(body.detail || `search failed: ${response.status}`);
      render(body.results || []); setState(body.count ? `${body.count} resultaat${body.count === 1 ? '' : 'en'} gevonden.` : 'Geen intelligence gevonden.', body.count ? 'success' : 'empty');
    } catch (error) { results.replaceChildren(); setState(`Zoeken niet beschikbaar: ${error.message}`, 'error'); }
  }
  form.addEventListener('submit', (event) => { event.preventDefault(); void search(); });
  session().catch((error) => { principal.textContent = `Sessiefout: ${error.message}`; principal.className = 'status-pill error'; setState('Geen geautoriseerde sessie.', 'error'); });
})();
"""

_RC9_COMPAT_CSS = """
*, *::before, *::after { box-sizing: border-box; min-width: 0; }
html, body { width: 100%; max-width: 100%; overflow-x: hidden; }
.app-header, .workspace, .page-heading, .content-grid, .surface, .header-actions,
.hero-search, .form-grid, .security-heading, .table-wrap, table, pre, code { min-width: 0; max-width: 100%; }
.surface, .surface.critical, .decision-card, .search-surface, .response-surface,
.security-card, .table-surface, .intel-card { background-image: none !important; }
.page-heading h2 { font-size: 2rem !important; }
.sr-only {
  position: absolute !important;
  left: 0 !important;
  top: 0 !important;
  width: 1px !important;
  height: 1px !important;
  padding: 0 !important;
  margin: 0 !important;
  overflow: hidden !important;
  clip: rect(0, 0, 0, 0) !important;
  clip-path: inset(50%) !important;
  white-space: nowrap !important;
  border: 0 !important;
}
.button.primary {
  background-color: #0b4f7a !important;
  background-image: none !important;
  color: #ffffff !important;
  border: 2px solid #57baff !important;
}
.button.danger { background-color: #8f3141 !important; background-image: none !important; color: #ffffff !important; }
.button.ghost, .button.secondary, .button.danger, input, textarea {
  border: 2px solid #eef5ff !important;
}
input, textarea, button, a, pre, code { max-width: 100%; overflow-wrap: anywhere; word-break: break-word; }
input:focus-visible, textarea:focus-visible, button:focus-visible, a:focus-visible {
  outline: 3px solid #f8df6b !important;
  outline-offset: 3px !important;
  box-shadow: 0 0 0 1px #08111f !important;
}
.content-grid.equal { grid-template-columns: repeat(2, minmax(0, 1fr)); }
.hero-search { grid-template-columns: auto minmax(0, 1fr) auto; }
.table-wrap { overflow-x: auto; }
.inline-status[data-state="empty"] { border-color: #60758f; }
.inline-status[data-state="forbidden"] { border-color: #d8a43a; }
@media (max-width: 700px) {
  .app-header, .header-actions { align-items: stretch; }
  .app-header, .content-grid.equal, .form-grid, .form-grid.three { grid-template-columns: 1fr !important; }
  .content-grid.equal { display: grid; }
  .header-actions { width: 100%; }
  .hero-search { grid-template-columns: 1fr; }
  .hero-search .search-icon { display: none; }
  .button, input, textarea { width: 100%; }
}
@media (max-width: 400px) {
  .app-header, .workspace { padding-left: .75rem !important; padding-right: .75rem !important; }
  .surface { padding-left: .8rem !important; padding-right: .8rem !important; }
  .table-wrap { overflow: visible; }
  .table-surface table, .table-surface thead, .table-surface tbody,
  .table-surface tr, .table-surface th, .table-surface td {
    display: block;
    width: 100%;
    max-width: 100%;
  }
  .table-surface th, .table-surface td {
    white-space: normal;
    overflow-wrap: anywhere;
    word-break: break-word;
  }
}
"""


def _page_headers() -> dict[str, str]:
    return {
        "Cache-Control": "no-store",
        "Content-Security-Policy": (
            "default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self'; "
            "img-src 'self' data:; frame-ancestors 'none'; base-uri 'none'; form-action 'self'"
        ),
    }


@router.get("/ui/share-approval", response_class=HTMLResponse, include_in_schema=False)
def share_approval_page() -> HTMLResponse:
    return HTMLResponse(_PAGE, headers=_page_headers())


@router.get("/ui/share-approval.js", include_in_schema=False)
def share_approval_script() -> Response:
    return Response(_SCRIPT, media_type="application/javascript", headers={"Cache-Control": "no-store"})


@router.get("/ui/analyst-search", response_class=HTMLResponse, include_in_schema=False)
def analyst_search_page() -> HTMLResponse:
    return HTMLResponse(_ANALYST_PAGE, headers=_page_headers())


@router.get("/ui/analyst-search.js", include_in_schema=False)
def analyst_search_script() -> Response:
    return Response(_ANALYST_SCRIPT, media_type="application/javascript", headers={"Cache-Control": "no-store"})


@router.get("/ui/rc9-compat.css", include_in_schema=False)
def rc9_compat_css() -> Response:
    return Response(_RC9_COMPAT_CSS, media_type="text/css", headers={"Cache-Control": "no-store"})


@router.get("/api/v1/ui/session")
def ui_session(principal: Annotated[Principal, Depends(resolve_principal)]) -> dict[str, object]:
    permissions = sorted(permission.value for permission in Permission if principal.can(permission))
    return {
        "subject": principal.subject,
        "roles": sorted(role.value for role in principal.roles),
        "permissions": permissions,
        "service_account": principal.is_service_account,
        "publication_requires_separate_human_approval": True,
    }

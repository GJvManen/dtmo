from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse, Response

from dtmo.auth.dependencies import resolve_principal
from dtmo.auth.policy import Permission, Principal

router = APIRouter()

_PAGE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>DTMO governed share approval</title>
  <style>
    body { font-family: system-ui, sans-serif; max-width: 52rem; margin: 2rem auto; padding: 0 1rem; }
    fieldset { display: grid; gap: .75rem; padding: 1rem; }
    label { font-weight: 600; }
    input { padding: .65rem; font: inherit; }
    button { padding: .65rem 1rem; font: inherit; cursor: pointer; }
    .actions { display: flex; gap: .75rem; flex-wrap: wrap; }
    pre { white-space: pre-wrap; overflow-wrap: anywhere; background: #f4f4f4; padding: 1rem; }
  </style>
</head>
<body>
  <main>
    <h1>Governed intelligence decision</h1>
    <p id="principal" data-testid="principal" role="status" aria-live="polite" aria-atomic="true">Resolving authenticated principal…</p>
    <fieldset>
      <legend>Intelligence item</legend>
      <label for="item-id">Item ID</label>
      <input id="item-id" data-testid="item-id" autocomplete="off" required>
      <div class="actions">
        <button id="review" data-testid="review-button" type="button" hidden>Mark reviewed</button>
        <button id="share" data-testid="share-button" type="button" hidden>Approve external sharing</button>
      </div>
    </fieldset>
    <p>Review and share approval are separate governed decisions. A reviewer cannot approve their own review.</p>
    <pre id="result" data-testid="result" aria-live="polite">No decision submitted.</pre>
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
    principal.textContent = `${body.subject} — roles: ${body.roles.join(', ')}`;
    review.hidden = !body.permissions.includes('review:intelligence');
    share.hidden = !body.permissions.includes('approve:share');
  }

  async function decision(action) {
    const id = itemId.value.trim();
    if (!id) {
      result.textContent = 'An intelligence item ID is required.';
      return;
    }
    const response = await fetch(`/api/v1/intelligence/${encodeURIComponent(id)}/${action}`, {
      method: 'POST',
      credentials: 'same-origin',
      headers: {'X-Request-ID': crypto.randomUUID()},
    });
    let body;
    try { body = await response.json(); } catch (_) { body = {detail: 'invalid response'}; }
    result.textContent = JSON.stringify({status: response.status, ...body}, null, 2);
  }

  review.addEventListener('click', () => decision('review'));
  share.addEventListener('click', () => decision('share-approval'));
  session().catch((error) => { result.textContent = `Session error: ${error.message}`; });
})();
"""

_ANALYST_PAGE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>DTMO analyst intelligence search</title>
  <style>
    body { font-family: system-ui, sans-serif; max-width: 60rem; margin: 2rem auto; padding: 0 1rem; }
    form { display: flex; gap: .75rem; align-items: end; flex-wrap: wrap; }
    label { display: grid; gap: .35rem; font-weight: 600; }
    input, button { padding: .65rem; font: inherit; }
    #status { margin: 1rem 0; padding: .75rem; border: 1px solid #bbb; }
    #results { display: grid; gap: .75rem; padding: 0; list-style: none; }
    #results li { border: 1px solid #bbb; padding: .75rem; }
  </style>
</head>
<body>
  <main>
    <h1>Analyst intelligence search</h1>
    <p id="analyst-principal" data-testid="analyst-principal" role="status" aria-live="polite" aria-atomic="true">Resolving authenticated principal…</p>
    <section id="search-panel" data-testid="search-panel" hidden>
      <form id="search-form">
        <label for="query">Search intelligence
          <input id="query" data-testid="search-query" minlength="2" required autocomplete="off">
        </label>
        <button type="submit" data-testid="search-submit">Search</button>
      </form>
      <div id="status" data-testid="search-status" role="status" aria-live="polite">Ready to search.</div>
      <ul id="results" data-testid="search-results"></ul>
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

  function setState(message, state) {
    status.textContent = message;
    status.dataset.state = state;
  }

  function render(items) {
    results.replaceChildren();
    for (const item of items) {
      const row = document.createElement('li');
      const title = document.createElement('strong');
      title.textContent = String(item.title || 'Untitled intelligence');
      row.appendChild(title);
      if (item.summary) {
        const summary = document.createElement('p');
        summary.textContent = String(item.summary);
        row.appendChild(summary);
      }
      results.appendChild(row);
    }
  }

  async function session() {
    const response = await fetch('/api/v1/ui/session', {credentials: 'same-origin'});
    const body = await response.json();
    if (!response.ok) throw new Error(body.detail || `session failed: ${response.status}`);
    principal.textContent = `${body.subject} — roles: ${body.roles.join(', ')}`;
    const allowed = body.permissions.includes('read:intelligence');
    panel.hidden = !allowed;
    if (!allowed) setState('Intelligence search is not permitted for this principal.', 'forbidden');
  }

  async function search() {
    const value = query.value.trim();
    if (value.length < 2) return;
    results.replaceChildren();
    setState('Loading intelligence…', 'loading');
    try {
      const response = await fetch(`/api/v1/intelligence/search?q=${encodeURIComponent(value)}`, {
        credentials: 'same-origin',
      });
      let body;
      try { body = await response.json(); } catch (_) { body = {detail: 'invalid response'}; }
      if (!response.ok) throw new Error(body.detail || `search failed: ${response.status}`);
      render(body.results || []);
      if (body.count === 0) {
        setState('No intelligence matched this search.', 'empty');
      } else {
        setState(`${body.count} intelligence result${body.count === 1 ? '' : 's'} found.`, 'success');
      }
    } catch (error) {
      results.replaceChildren();
      setState(`Search unavailable: ${error.message}`, 'error');
    }
  }

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    void search();
  });
  session().catch((error) => setState(`Session error: ${error.message}`, 'error'));
})();
"""


@router.get("/ui/share-approval", response_class=HTMLResponse, include_in_schema=False)
def share_approval_page() -> HTMLResponse:
    return HTMLResponse(
        _PAGE,
        headers={
            "Cache-Control": "no-store",
            "Content-Security-Policy": (
                "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; "
                "connect-src 'self'; img-src 'self'; frame-ancestors 'none'"
            ),
        },
    )


@router.get("/ui/share-approval.js", include_in_schema=False)
def share_approval_script() -> Response:
    return Response(
        _SCRIPT,
        media_type="application/javascript",
        headers={"Cache-Control": "no-store"},
    )


@router.get("/ui/analyst-search", response_class=HTMLResponse, include_in_schema=False)
def analyst_search_page() -> HTMLResponse:
    return HTMLResponse(
        _ANALYST_PAGE,
        headers={
            "Cache-Control": "no-store",
            "Content-Security-Policy": (
                "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; "
                "connect-src 'self'; img-src 'self'; frame-ancestors 'none'"
            ),
        },
    )


@router.get("/ui/analyst-search.js", include_in_schema=False)
def analyst_search_script() -> Response:
    return Response(
        _ANALYST_SCRIPT,
        media_type="application/javascript",
        headers={"Cache-Control": "no-store"},
    )


@router.get("/api/v1/ui/session")
def ui_session(
    principal: Annotated[Principal, Depends(resolve_principal)],
) -> dict[str, object]:
    permissions = sorted(permission.value for permission in Permission if principal.can(permission))
    return {
        "subject": principal.subject,
        "roles": sorted(role.value for role in principal.roles),
        "permissions": permissions,
        "service_account": principal.is_service_account,
        "publication_requires_separate_human_approval": True,
    }

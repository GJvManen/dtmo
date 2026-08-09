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
    <p id="principal" data-testid="principal">Resolving authenticated principal…</p>
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

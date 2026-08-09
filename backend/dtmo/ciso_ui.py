from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import HTMLResponse, Response

router = APIRouter()

_PAGE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>DTMO CISO token revocation</title>
  <style>
    body { font-family: system-ui, sans-serif; max-width: 56rem; margin: 2rem auto; padding: 0 1rem; }
    form { display: grid; gap: .8rem; }
    label { display: grid; gap: .35rem; font-weight: 600; }
    input, textarea, button { padding: .65rem; font: inherit; }
    textarea { min-height: 6rem; }
    #status { margin-top: 1rem; padding: .8rem; border: 1px solid #bbb; white-space: pre-wrap; }
  </style>
</head>
<body>
  <main>
    <h1>CISO security token revocation</h1>
    <p id="ciso-principal" data-testid="ciso-principal">Resolving authenticated principal…</p>
    <section id="revocation-panel" data-testid="revocation-panel" hidden>
      <form id="revocation-form">
        <label for="jti">Token identifier (JTI)
          <input id="jti" data-testid="token-jti" required autocomplete="off">
        </label>
        <label for="expires-at">Token expiry (ISO 8601)
          <input id="expires-at" data-testid="token-expiry" required autocomplete="off">
        </label>
        <label for="reason">Revocation reason
          <textarea id="reason" data-testid="revocation-reason" required></textarea>
        </label>
        <button type="submit" data-testid="revoke-submit">Revoke token</button>
      </form>
    </section>
    <div id="status" data-testid="revocation-status" role="status" aria-live="polite">Waiting for authorization.</div>
  </main>
  <script src="/ui/ciso-security.js" defer></script>
</body>
</html>
"""

_SCRIPT = r"""(() => {
  const principal = document.getElementById('ciso-principal');
  const panel = document.getElementById('revocation-panel');
  const form = document.getElementById('revocation-form');
  const jti = document.getElementById('jti');
  const expiresAt = document.getElementById('expires-at');
  const reason = document.getElementById('reason');
  const status = document.getElementById('status');

  function setState(message, state) {
    status.textContent = message;
    status.dataset.state = state;
  }

  async function session() {
    const response = await fetch('/api/v1/ui/session', {credentials: 'same-origin'});
    const body = await response.json();
    if (!response.ok) throw new Error(body.detail || `session failed: ${response.status}`);
    principal.textContent = `${body.subject} — roles: ${body.roles.join(', ')}`;
    const allowed = body.permissions.includes('revoke:tokens') && !body.service_account;
    panel.hidden = !allowed;
    setState(
      allowed ? 'Authorized for governed token revocation.' : 'Token revocation is not permitted for this principal.',
      allowed ? 'ready' : 'forbidden'
    );
  }

  async function revoke() {
    setState('Revoking token…', 'loading');
    const response = await fetch('/api/v1/security/tokens/revoke', {
      method: 'POST',
      credentials: 'same-origin',
      headers: {
        'Content-Type': 'application/json',
        'X-Request-ID': crypto.randomUUID(),
      },
      body: JSON.stringify({
        jti: jti.value.trim(),
        expires_at: expiresAt.value.trim(),
        reason: reason.value.trim(),
      }),
    });
    let body;
    try { body = await response.json(); } catch (_) { body = {detail: 'invalid response'}; }
    if (!response.ok) {
      setState(`Revocation failed (${response.status}): ${body.detail || 'unknown error'}`, 'error');
      return;
    }
    setState(`Token revoked. Audit event: ${body.audit_event_id}`, 'success');
  }

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    void revoke();
  });
  session().catch((error) => setState(`Session error: ${error.message}`, 'error'));
})();
"""


def _page_headers() -> dict[str, str]:
    return {
        "Cache-Control": "no-store",
        "Content-Security-Policy": (
            "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; "
            "connect-src 'self'; img-src 'self'; frame-ancestors 'none'"
        ),
    }


@router.get("/ui/ciso-security", response_class=HTMLResponse, include_in_schema=False)
def ciso_security_page() -> HTMLResponse:
    return HTMLResponse(_PAGE, headers=_page_headers())


@router.get("/ui/ciso-security.js", include_in_schema=False)
def ciso_security_script() -> Response:
    return Response(
        _SCRIPT,
        media_type="application/javascript",
        headers={"Cache-Control": "no-store"},
    )

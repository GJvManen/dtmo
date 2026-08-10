from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import HTMLResponse, Response

router = APIRouter()

_PAGE = """<!doctype html>
<html lang="nl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>DTMO — CISO security</title>
  <link rel="stylesheet" href="/ui/design-system.css">
  <link rel="stylesheet" href="/ui/rc9-compat.css">
</head>
<body>
  <a class="skip-link" href="#main">Ga naar hoofdinhoud</a>
  <header class="app-header">
    <div><p class="eyebrow">CISO workspace</p><h1>Security operations</h1></div>
    <div class="header-actions"><a class="button ghost" href="/">Terug naar console</a><span id="ciso-principal" data-testid="ciso-principal" class="status-pill neutral" role="status" aria-live="polite" aria-atomic="true">Principal bepalen…</span></div>
  </header>
  <main id="main" class="workspace">
    <section class="page-heading"><div><p class="eyebrow">Privileged control</p><h2>Token revocation</h2><p>Maak een bearer token voortijdig ongeldig. Deze actie is alleen beschikbaar voor een menselijke principal met expliciete revoke-permissie.</p></div></section>
    <section class="surface security-card">
      <div class="security-heading"><div class="security-symbol">!</div><div><h3>Revoke bearer token</h3><p>Vul de unieke JTI, geldigheidsduur en reden in. De actie wordt auditbaar vastgelegd.</p></div></div>
      <section id="revocation-panel" data-testid="revocation-panel" hidden>
        <form id="revocation-form" class="form-grid three">
          <label for="jti">Token identifier (JTI)<input id="jti" data-testid="token-jti" required autocomplete="off" placeholder="Token JTI"></label>
          <label for="expires-at">Token expiry (ISO 8601)<input id="expires-at" data-testid="token-expiry" required autocomplete="off" placeholder="2026-08-10T15:00:00Z"></label>
          <label for="reason">Revocation reason<textarea id="reason" data-testid="revocation-reason" required rows="4" placeholder="Waarom wordt dit token ingetrokken?"></textarea></label>
          <button type="submit" data-testid="revoke-submit" class="button danger">Token intrekken</button>
        </form>
      </section>
      <div id="status" data-testid="revocation-status" class="inline-status" role="status" aria-live="polite">Wacht op autorisatie.</div>
    </section>
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
  function setState(message, state) { status.textContent = message; status.dataset.state = state; }
  async function session() {
    const response = await fetch('/api/v1/ui/session', {credentials: 'same-origin'}); const body = await response.json();
    if (!response.ok) throw new Error(body.detail || `session failed: ${response.status}`);
    principal.textContent = `${body.subject} · ${body.roles.join(', ') || 'geen rollen'}`; principal.className = 'status-pill success';
    const allowed = body.permissions.includes('revoke:tokens') && !body.service_account; panel.hidden = !allowed;
    setState(allowed ? 'Geautoriseerd voor governed token revocation.' : 'Token revocation is niet toegestaan voor deze principal.', allowed ? 'ready' : 'forbidden');
  }
  async function revoke() {
    setState('Token intrekken…', 'loading');
    const response = await fetch('/api/v1/security/tokens/revoke', {method: 'POST', credentials: 'same-origin', headers: {'Content-Type':'application/json','X-Request-ID':crypto.randomUUID()}, body: JSON.stringify({jti:jti.value.trim(),expires_at:expiresAt.value.trim(),reason:reason.value.trim()})});
    let body; try { body = await response.json(); } catch (_) { body = {detail:'invalid response'}; }
    if (!response.ok) { setState(`Revocation mislukt (${response.status}): ${body.detail || 'unknown error'}`, 'error'); return; }
    setState(`Token revoked. Audit event: ${body.audit_event_id}`, 'success'); form.reset();
  }
  form.addEventListener('submit',(event)=>{event.preventDefault();void revoke();});
  session().catch((error)=>{principal.textContent=`Sessiefout: ${error.message}`;principal.className='status-pill error';setState('Geen geautoriseerde sessie.', 'error');});
})();
"""


def _page_headers() -> dict[str, str]:
    return {
        "Cache-Control": "no-store",
        "Content-Security-Policy": (
            "default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self'; "
            "img-src 'self' data:; frame-ancestors 'none'; base-uri 'none'; form-action 'self'"
        ),
    }


@router.get("/ui/ciso-security", response_class=HTMLResponse, include_in_schema=False)
def ciso_security_page() -> HTMLResponse:
    return HTMLResponse(_PAGE, headers=_page_headers())


@router.get("/ui/ciso-security.js", include_in_schema=False)
def ciso_security_script() -> Response:
    return Response(_SCRIPT, media_type="application/javascript", headers={"Cache-Control": "no-store"})

from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import HTMLResponse, Response

from dtmo.unified_console import _PAGE as BASE_CONSOLE_PAGE

router = APIRouter()

_ADMIN_START = '<section class="view" data-view-panel="administration">'
_GOVERNANCE_START = '<section class="view" data-view-panel="governance">'

_RBAC_PANEL = r'''
<article class="surface" id="rbac-administration" style="grid-column:1/-1">
  <div class="page-heading">
    <div>
      <p class="eyebrow">Governed identity administration</p>
      <h3>Gebruikers & rollen</h3>
      <p>Beheer auditable principal/rol-toewijzingen. DTMO-rollen zijn vaste securityrollen; custom tokenrollen worden niet vanuit de browser aangemaakt.</p>
    </div>
    <button id="rbac-refresh" class="button secondary" type="button">Vernieuwen</button>
  </div>
  <div id="rbac-status" class="status" role="status" aria-live="polite">RBAC-beheer laden…</div>
  <div class="grid">
    <section class="card" aria-labelledby="rbac-create-title">
      <h4 id="rbac-create-title">Principal toevoegen</h4>
      <form id="rbac-create-form">
        <label>Subject<input id="rbac-subject" required maxlength="255" autocomplete="off" placeholder="naam@example.org"></label>
        <label>Weergavenaam<input id="rbac-display-name" maxlength="255" autocomplete="off" placeholder="Naam of functie"></label>
        <label>Principal type
          <select id="rbac-principal-type">
            <option value="human">Human</option>
            <option value="service_account">Service account</option>
          </select>
        </label>
        <fieldset><legend>Rollen</legend><div id="rbac-create-roles" class="cards"></div></fieldset>
        <label><input id="rbac-active" type="checkbox" checked> Actief</label>
        <button class="button" type="submit">Principal aanmaken</button>
      </form>
    </section>
    <section class="card" aria-labelledby="rbac-role-title">
      <h4 id="rbac-role-title">Vaste rolcatalogus</h4>
      <p class="muted">Rollen en permissies komen uit het server-side autorisatiebeleid en zijn hier niet vrij definieerbaar.</p>
      <div id="rbac-role-catalog" class="cards"></div>
    </section>
  </div>
  <section aria-labelledby="rbac-principals-title">
    <div class="page-heading"><div><h4 id="rbac-principals-title">Managed principals</h4><p>Wijzigingen zijn auditbaar. Productie-bearer tokens moeten na een rolwijziging door de identity provider worden gereconcilieerd of opnieuw uitgegeven.</p></div></div>
    <div id="rbac-principals" class="cards"></div>
  </section>
</article>
'''

_SCRIPT_TAG = '<script src="/ui/rc13-administration.js" defer></script>'


def extend_console_page(page: str) -> str:
    admin_start = page.find(_ADMIN_START)
    governance_start = page.find(_GOVERNANCE_START)
    if admin_start < 0 or governance_start < 0 or governance_start <= admin_start:
        raise RuntimeError("canonical Administration section markers not found")
    admin_segment = page[admin_start:governance_start]
    insert_at = admin_segment.rfind("</div></section>")
    if insert_at < 0:
        raise RuntimeError("canonical Administration grid boundary not found")
    extended_admin = admin_segment[:insert_at] + _RBAC_PANEL + admin_segment[insert_at:]
    extended = page[:admin_start] + extended_admin + page[governance_start:]
    if _SCRIPT_TAG not in extended:
        extended = extended.replace("</body>", _SCRIPT_TAG + "</body>")
    return extended


_PAGE = extend_console_page(BASE_CONSOLE_PAGE)


@router.get("/", response_class=HTMLResponse, include_in_schema=False)
@router.get("/ui/console", response_class=HTMLResponse, include_in_schema=False)
def rc13_administration_console() -> HTMLResponse:
    return HTMLResponse(_PAGE, headers={"Cache-Control": "no-store"})


_SCRIPT = r'''
(() => {
  const panel = document.getElementById('rbac-administration');
  if (!panel) return;

  const storage = {
    subject: () => sessionStorage.getItem('dtmo.subject') || 'admin-tester',
    roles: () => sessionStorage.getItem('dtmo.roles') || 'admin',
    apiKey: () => sessionStorage.getItem('dtmo.apiKey') || '',
  };
  const esc = (value) => String(value ?? '').replace(/[&<>"']/g, (char) => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
  const requestId = () => globalThis.crypto?.randomUUID?.() || `dtmo-rbac-${Date.now()}-${Math.random().toString(16).slice(2)}`;
  let roles = [];
  let principals = [];

  async function rbacApi(url, options = {}) {
    const write = Boolean(options.method && options.method !== 'GET');
    const headers = {
      'X-DTMO-Subject': storage.subject(),
      'X-DTMO-Roles': storage.roles(),
      'X-DTMO-API-Key': storage.apiKey(),
      ...(options.headers || {}),
    };
    if (write) headers['X-Request-ID'] = requestId();
    if (options.body) headers['Content-Type'] = 'application/json';
    const response = await fetch(url, {...options, headers});
    let body = {};
    try { body = await response.json(); } catch (_) { body = {}; }
    if (!response.ok) throw new Error(body.detail || `HTTP ${response.status}`);
    return body;
  }

  function eligibleRoles(principalType) {
    return roles.filter((entry) => (entry.eligible_principal_types || []).includes(principalType));
  }

  function roleChoices(principalType, selected = []) {
    const chosen = new Set(selected);
    const available = eligibleRoles(principalType);
    if (!available.length) return '<p class="muted">Geen rollen beschikbaar.</p>';
    return available.map((entry) => `<label><input type="checkbox" data-rbac-role="${esc(entry.role)}" ${chosen.has(entry.role) ? 'checked' : ''}> <strong>${esc(entry.role)}</strong></label>`).join('');
  }

  function renderCreateRoles() {
    const type = document.getElementById('rbac-principal-type').value;
    const selected = [...document.querySelectorAll('#rbac-create-roles [data-rbac-role]:checked')].map((node) => node.dataset.rbacRole);
    document.getElementById('rbac-create-roles').innerHTML = roleChoices(type, selected);
  }

  function renderRoleCatalog() {
    const target = document.getElementById('rbac-role-catalog');
    target.innerHTML = roles.map((entry) => `<article class="card"><strong>${esc(entry.role)}</strong><p>${(entry.permissions || []).map(esc).join(' · ') || 'Geen permissies'}</p><small>${(entry.eligible_principal_types || []).map(esc).join(', ')} · immutable</small></article>`).join('');
  }

  function renderPrincipals() {
    const target = document.getElementById('rbac-principals');
    if (!principals.length) {
      target.innerHTML = '<div class="empty-state"><strong>Nog geen managed principals.</strong><p>Voeg een principal toe om governed roltoewijzingen vast te leggen.</p></div>';
      return;
    }
    const current = storage.subject();
    target.innerHTML = principals.map((principal) => {
      const selfManaged = principal.subject === current;
      const disabled = selfManaged ? 'disabled' : '';
      return `<article class="card" data-rbac-principal="${esc(principal.subject)}">
        <div class="page-heading"><div><strong>${esc(principal.display_name || principal.subject)}</strong><p class="muted-code">${esc(principal.subject)}</p></div><span class="status-pill ${principal.active ? 'good' : 'neutral'}">${principal.active ? 'Actief' : 'Inactief'}</span></div>
        <p>${esc(principal.principal_type)} · token reissue: ${principal.requires_token_reissue ? 'vereist' : 'niet vereist'}</p>
        ${selfManaged ? '<p class="status-pill neutral">Zelfbeheer is server-side geblokkeerd.</p>' : ''}
        <label>Weergavenaam<input data-rbac-display-name value="${esc(principal.display_name || '')}" maxlength="255" ${disabled}></label>
        <label><input type="checkbox" data-rbac-active ${principal.active ? 'checked' : ''} ${disabled}> Actief</label>
        <fieldset ${disabled}><legend>Rollen</legend><div data-rbac-role-list>${roleChoices(principal.principal_type, principal.roles || [])}</div></fieldset>
        <div class="actions"><button class="button secondary" type="button" data-rbac-save="${esc(principal.subject)}" ${disabled}>Opslaan</button></div>
        <div class="diagnostic" data-rbac-result="${esc(principal.subject)}" role="status"></div>
      </article>`;
    }).join('');
  }

  async function loadRbac() {
    const status = document.getElementById('rbac-status');
    status.textContent = 'RBAC-beheer laden…';
    try {
      [roles, principals] = await Promise.all([
        rbacApi('/api/v1/admin/rbac/roles'),
        rbacApi('/api/v1/admin/rbac/principals'),
      ]);
      renderRoleCatalog();
      renderCreateRoles();
      renderPrincipals();
      status.textContent = `${principals.length} managed principals · ${roles.length} vaste rollen.`;
    } catch (error) {
      status.textContent = `RBAC-beheer niet beschikbaar: ${error.message}`;
    }
  }

  async function createPrincipal(event) {
    event.preventDefault();
    const status = document.getElementById('rbac-status');
    const selectedRoles = [...document.querySelectorAll('#rbac-create-roles [data-rbac-role]:checked')].map((node) => node.dataset.rbacRole);
    const payload = {
      subject: document.getElementById('rbac-subject').value.trim(),
      display_name: document.getElementById('rbac-display-name').value.trim() || null,
      principal_type: document.getElementById('rbac-principal-type').value,
      roles: selectedRoles,
      active: document.getElementById('rbac-active').checked,
    };
    status.textContent = 'Principal aanmaken…';
    try {
      await rbacApi('/api/v1/admin/rbac/principals', {method: 'POST', body: JSON.stringify(payload)});
      event.target.reset();
      document.getElementById('rbac-active').checked = true;
      document.getElementById('rbac-principal-type').value = 'human';
      await loadRbac();
      status.textContent = `${payload.subject} aangemaakt. Identity-provider/tokenreconciliatie is vereist voordat productieclaims wijzigen.`;
    } catch (error) {
      status.textContent = `Aanmaken mislukt: ${error.message}`;
    }
  }

  async function updatePrincipal(subject) {
    const card = [...document.querySelectorAll('[data-rbac-principal]')].find((node) => node.dataset.rbacPrincipal === subject);
    if (!card) return;
    const result = card.querySelector('[data-rbac-result]');
    const payload = {
      display_name: card.querySelector('[data-rbac-display-name]').value.trim() || null,
      active: card.querySelector('[data-rbac-active]').checked,
      roles: [...card.querySelectorAll('[data-rbac-role]:checked')].map((node) => node.dataset.rbacRole),
    };
    result.textContent = 'Wijziging opslaan…';
    try {
      await rbacApi(`/api/v1/admin/rbac/principals/${encodeURIComponent(subject)}`, {method: 'PATCH', body: JSON.stringify(payload)});
      await loadRbac();
      const refreshed = [...document.querySelectorAll('[data-rbac-principal]')].find((node) => node.dataset.rbacPrincipal === subject);
      const refreshedResult = refreshed?.querySelector('[data-rbac-result]');
      if (refreshedResult) refreshedResult.textContent = 'Opgeslagen en geaudit; tokenreconciliatie vereist.';
    } catch (error) {
      result.textContent = `Opslaan mislukt: ${error.message}`;
    }
  }

  document.getElementById('rbac-principal-type').addEventListener('change', renderCreateRoles);
  document.getElementById('rbac-create-form').addEventListener('submit', createPrincipal);
  document.getElementById('rbac-refresh').addEventListener('click', () => void loadRbac());
  document.getElementById('rbac-principals').addEventListener('click', (event) => {
    const button = event.target.closest('[data-rbac-save]');
    if (button) void updatePrincipal(button.dataset.rbacSave);
  });
  void loadRbac();
})();
'''


@router.get("/ui/rc13-administration.js", include_in_schema=False)
def rc13_administration_script() -> Response:
    return Response(
        _SCRIPT,
        media_type="application/javascript",
        headers={"Cache-Control": "no-store"},
    )
